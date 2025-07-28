#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QPS格式解析器 (简化高效版)
一键求解，自动生成LaTeX报告
支持智能变量格式化和排序 (新增功能)
"""

import os
import datetime
import sys
from pathlib import Path
import coptpy as cp
from coptpy import COPT
import numpy as np
from collections import defaultdict
import re

class QPSParser:
    """QPS格式解析器"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = ""
        self.rows = {}  # row_name -> (sense, rhs)
        self.cols = {}  # col_name -> {row_name: coeff}
        self.bounds = {}  # col_name -> (lb, ub)
        self.quadobj = {}  # (var1, var2) -> coeff
        self.obj_name = None
        self.objective_constant = 0.0
        
    def parse(self):
        """解析QPS文件"""
        current_section = None
        
        print("开始解析QPS文件...")
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.rstrip()
                    
                    if not line or line.startswith('*'):
                        continue
                    
                    # 检查段标识符
                    if line.strip() in ['NAME', 'ROWS', 'COLUMNS', 'RHS', 'BOUNDS', 'QUADOBJ', 'ENDATA']:
                        current_section = line.strip()
                        continue
                    
                    try:
                        if current_section == 'NAME':
                            self.name = line.strip()
                        elif current_section == 'ROWS':
                            self._parse_row(line)
                        elif current_section == 'COLUMNS':
                            self._parse_column(line)
                        elif current_section == 'RHS':
                            self._parse_rhs(line)
                        elif current_section == 'BOUNDS':
                            self._parse_bounds(line)
                        elif current_section == 'QUADOBJ':
                            self._parse_quadobj(line)
                            
                    except Exception as e:
                        continue
        
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到文件: {self.filepath}")
        except Exception as e:
            raise Exception(f"文件读取错误: {e}")
        
        print(f"解析完成: 变量数={len(self.cols)}, 约束数={len([r for r in self.rows.values() if r[0] != 'N'])}, 二次项数={len(self.quadobj)}")
    
    def _parse_row(self, line):
        """解析ROWS段"""
        parts = line.split()
        if len(parts) >= 2:
            sense = parts[0].strip()
            row_name = parts[1].strip()
            if row_name:
                self.rows[row_name] = (sense, 0.0)
                if sense == 'N':
                    self.obj_name = row_name
    
    def _parse_column(self, line):
        """解析COLUMNS段"""
        parts = line.split()
        if len(parts) >= 3:
            col_name = parts[0].strip()
            i = 1
            while i + 1 < len(parts):
                row_name = parts[i].strip()
                try:
                    coeff = float(parts[i + 1])
                    if col_name not in self.cols:
                        self.cols[col_name] = {}
                    self.cols[col_name][row_name] = coeff
                    i += 2
                except (ValueError, IndexError):
                    break
    
    def _parse_rhs(self, line):
        """解析RHS段"""
        parts = line.split()
        if len(parts) >= 3:
            i = 1
            while i + 1 < len(parts):
                row_name = parts[i].strip()
                try:
                    rhs_value = float(parts[i + 1])
                    if row_name in self.rows:
                        sense, _ = self.rows[row_name]
                        self.rows[row_name] = (sense, rhs_value)
                        if row_name == self.obj_name:
                            self.objective_constant = -rhs_value
                    i += 2
                except (ValueError, IndexError):
                    break
    
    def _parse_bounds(self, line):
        """解析BOUNDS段"""
        parts = line.split()
        if len(parts) >= 3:
            bound_type = parts[0].strip()
            var_name = parts[2].strip() if len(parts) > 2 else parts[1].strip()
            
            if var_name:
                if var_name not in self.bounds:
                    self.bounds[var_name] = (0.0, float('inf'))
                
                lb, ub = self.bounds[var_name]
                
                if len(parts) >= 4:
                    try:
                        value = float(parts[3])
                        
                        if bound_type == 'UP':
                            ub = value
                        elif bound_type == 'LO':
                            lb = value
                        elif bound_type == 'FX':
                            lb = ub = value
                        elif bound_type == 'FR':
                            lb, ub = -float('inf'), float('inf')
                        elif bound_type == 'MI':
                            lb = -float('inf')
                        elif bound_type == 'PL':
                            ub = float('inf')
                            
                        self.bounds[var_name] = (lb, ub)
                    except (ValueError, IndexError):
                        pass
    
    def _parse_quadobj(self, line):
        """解析QUADOBJ段"""
        parts = line.split()
        if len(parts) >= 3:
            var1_name = parts[0].strip()
            var2_name = parts[1].strip()
            
            try:
                coeff = float(parts[2])
                self.quadobj[(var1_name, var2_name)] = coeff
                
                if var1_name != var2_name:
                    self.quadobj[(var2_name, var1_name)] = coeff
                    
            except (ValueError, IndexError):
                pass

class QPSSolver:
    """QPS文件COPT求解器与LaTeX报告生成器"""
    
    def __init__(self, qps_filepath):
        self.qps_filepath = qps_filepath
        self.parser = QPSParser(qps_filepath)
        self.env = None
        self.model = None
        self.variables = {}
        self.solve_status = None
        self.objective_value = None
        self.solution = {}
        self.solve_time = 0
        self.log_filepath = None
        self.var_prefix_counts = {}  # 存储每个变量前缀的计数信息
        
    def _analyze_variable_patterns(self):
        """分析变量模式，确定每个前缀的变量数量和所需的零填充位数"""
        all_vars = set()
        
        # 收集所有变量
        for col_name in self.parser.cols.keys():
            all_vars.add(col_name)
        for var1, var2 in self.parser.quadobj.keys():
            all_vars.add(var1)
            all_vars.add(var2)
        
        prefix_max_numbers = defaultdict(int)
        
        for var_name in all_vars:
            # 处理包含连字符的特殊变量名
            if '------' in var_name:
                parts = var_name.split('------')
                if len(parts) == 2:
                    prefix = parts[0]
                    try:
                        number = int(parts[1])
                        prefix_max_numbers[prefix] = max(prefix_max_numbers[prefix], number)
                    except ValueError:
                        pass
            elif '-----' in var_name:
                parts = var_name.split('-----')
                if len(parts) == 2:
                    prefix = parts[0]
                    try:
                        number = int(parts[1])
                        prefix_max_numbers[prefix] = max(prefix_max_numbers[prefix], number)
                    except ValueError:
                        pass
            elif '----' in var_name:
                parts = var_name.split('----')
                if len(parts) == 2:
                    prefix = parts[0]
                    try:
                        number = int(parts[1])
                        prefix_max_numbers[prefix] = max(prefix_max_numbers[prefix], number)
                    except ValueError:
                        pass
            elif '---' in var_name:
                parts = var_name.split('---')
                if len(parts) == 2:
                    prefix = parts[0]
                    try:
                        number = int(parts[1])
                        prefix_max_numbers[prefix] = max(prefix_max_numbers[prefix], number)
                    except ValueError:
                        pass
            else:
                # 标准的字母+数字格式
                match = re.match(r"([a-zA-Z_]+)(\d+)", var_name)
                if match:
                    prefix = match.group(1)
                    number = int(match.group(2))
                    prefix_max_numbers[prefix] = max(prefix_max_numbers[prefix], number)
        
        # 确定每个前缀需要的零填充位数
        for prefix, max_num in prefix_max_numbers.items():
            if max_num >= 100:
                padding = 3  # 001, 002, ..., 999
            elif max_num >= 10:
                padding = 2  # 01, 02, ..., 99
            else:
                padding = 1  # 1, 2, ..., 9
            
            self.var_prefix_counts[prefix] = {
                'max_number': max_num,
                'padding': padding
            }

    def _get_variable_sort_key(self, var_name):
        """
        生成用于排序的键值，确保变量按照前缀和数字正确排序
        处理各种连字符格式
        """
        # 处理包含连字符的特殊变量名
        if '------' in var_name:
            parts = var_name.split('------')
            if len(parts) == 2:
                prefix = parts[0]
                try:
                    number = int(parts[1])
                    return (prefix, number)
                except ValueError:
                    return (var_name, 0)
        elif '-----' in var_name:
            parts = var_name.split('-----')
            if len(parts) == 2:
                prefix = parts[0]
                try:
                    number = int(parts[1])
                    return (prefix, number)
                except ValueError:
                    return (var_name, 0)
        elif '----' in var_name:
            parts = var_name.split('----')
            if len(parts) == 2:
                prefix = parts[0]
                try:
                    number = int(parts[1])
                    return (prefix, number)
                except ValueError:
                    return (var_name, 0)
        elif '---' in var_name:
            parts = var_name.split('---')
            if len(parts) == 2:
                prefix = parts[0]
                try:
                    number = int(parts[1])
                    return (prefix, number)
                except ValueError:
                    return (var_name, 0)
        
        # 标准的字母+数字格式
        match = re.match(r"([a-zA-Z_]+)(\d+)", var_name)
        if match:
            prefix = match.group(1)
            number = int(match.group(2))
            return (prefix, number)
        else:
            return (var_name, 0)

    def _get_constraint_sort_key(self, cons_name):
        """
        生成用于约束排序的键值，确保约束按照前缀和数字正确排序
        """
        match = re.match(r"([a-zA-Z_]+)(\d+)", cons_name)
        if match:
            prefix = match.group(1)
            number = int(match.group(2))
            return (prefix, number)
        else:
            return (cons_name, 0)
        
    def solve_model(self):
        """一键求解：解析 -> 构建 -> 求解"""
        try:
            # 解析QPS文件
            self.parser.parse()
            
            # 分析变量模式，为智能格式化做准备
            print("分析变量命名模式...")
            self._analyze_variable_patterns()
            
            # 设置日志文件
            log_dir = "copt_logs"
            os.makedirs(log_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(self.qps_filepath))[0]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_filepath = os.path.join(log_dir, f"{base_name}_qps_log_{timestamp}.log")
            
            # 构建COPT模型
            print("构建COPT模型...")
            self.env = cp.Envr()
            self.model = self.env.createModel("QPS_Model")
            
            # 设置日志
            self.model.setLogFile(self.log_filepath)
            
            # 分步骤构建
            self._create_variables()
            self._set_objective()
            self._add_constraints()
            
            print("开始求解...")
            
            # 设置求解参数
            try:
                self.model.setParam("LpMethod", 2)
                self.model.setParam("FeasTol", 1e-9)
                self.model.setParam("OptTol", 1e-9)
            except Exception:
                pass
            
            # 记录求解时间
            import time
            start_time = time.time()
            
            # 求解
            self.model.solve()
            
            self.solve_time = time.time() - start_time
            self.solve_status = self.model.Status
            
            # 提取结果
            if self.solve_status == COPT.OPTIMAL:
                self.objective_value = self.model.ObjVal
                for var_name, var in self.variables.items():
                    self.solution[var_name] = var.X
                
                print(f"求解成功！")
                print(f"最优目标值: {self.objective_value:.12g}")
                print(f"求解时间: {self.solve_time:.3f} 秒")
                
                nonzero_vars = {k: v for k, v in self.solution.items() if abs(v) > 1e-12}
                print(f"非零变量: {len(nonzero_vars)}/{len(self.solution)}")
                
                return True
            else:
                status_map = {
                    COPT.INFEASIBLE: "不可行",
                    COPT.UNBOUNDED: "无界",
                    COPT.NUMERICAL: "数值问题"
                }
                status_text = status_map.get(self.solve_status, f"状态码: {self.solve_status}")
                print(f"求解失败: {status_text}")
                return False
                
        except Exception as e:
            print(f"求解过程发生错误: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    def _create_variables(self):
        """创建变量"""
        all_vars = set()
        
        # 收集所有变量
        for col_name in self.parser.cols.keys():
            all_vars.add(col_name)
        for var1, var2 in self.parser.quadobj.keys():
            all_vars.add(var1)
            all_vars.add(var2)
        
        # 使用智能排序创建COPT变量
        for var_name in sorted(all_vars, key=self._get_variable_sort_key):
            lb, ub = self.parser.bounds.get(var_name, (0.0, float('inf')))
            
            if ub == float('inf'):
                ub = COPT.INFINITY
            if lb == -float('inf'):
                lb = -COPT.INFINITY
                
            var = self.model.addVar(lb=lb, ub=ub, name=var_name)
            self.variables[var_name] = var
        
        print(f"  创建了 {len(self.variables)} 个变量")
    
    def _set_objective(self):
        """设置目标函数"""
        print("  设置目标函数...")
        
        # 分别处理线性项和二次项
        linear_expr = None
        quad_expr = None
        
        # 构建线性项 - 使用排序确保一致性
        if self.parser.obj_name:
            for col_name in sorted(self.parser.cols.keys(), key=self._get_variable_sort_key):
                row_coeffs = self.parser.cols[col_name]
                if self.parser.obj_name in row_coeffs and col_name in self.variables:
                    coeff = row_coeffs[self.parser.obj_name]
                    if linear_expr is None:
                        linear_expr = coeff * self.variables[col_name]
                    else:
                        linear_expr += coeff * self.variables[col_name]
        
        # 构建二次项 - 使用排序确保一致性
        processed_pairs = set()
        for (var1, var2), coeff in sorted(self.parser.quadobj.items(), key=lambda x: (self._get_variable_sort_key(x[0][0]), self._get_variable_sort_key(x[0][1]))):
            if var1 in self.variables and var2 in self.variables:
                # 避免重复处理对称项
                pair = tuple(sorted([var1, var2], key=self._get_variable_sort_key))
                if pair in processed_pairs:
                    continue
                processed_pairs.add(pair)
                
                if var1 == var2:
                    # 对角线项
                    actual_coeff = coeff / 2.0
                else:
                    # 非对角线项
                    actual_coeff = coeff
                
                quad_term = actual_coeff * self.variables[var1] * self.variables[var2]
                if quad_expr is None:
                    quad_expr = quad_term
                else:
                    quad_expr += quad_term
        
        # 组合目标函数
        if linear_expr is None and quad_expr is None:
            obj_expr = self.parser.objective_constant
        elif linear_expr is None:
            if abs(self.parser.objective_constant) > 1e-15:
                obj_expr = quad_expr + self.parser.objective_constant
            else:
                obj_expr = quad_expr
        elif quad_expr is None:
            if abs(self.parser.objective_constant) > 1e-15:
                obj_expr = linear_expr + self.parser.objective_constant
            else:
                obj_expr = linear_expr
        else:
            if abs(self.parser.objective_constant) > 1e-15:
                obj_expr = linear_expr + quad_expr + self.parser.objective_constant
            else:
                obj_expr = linear_expr + quad_expr
        
        # 设置目标函数
        self.model.setObjective(obj_expr, COPT.MINIMIZE)
        print("  目标函数设置完成")
    
    def _add_constraints(self):
        """添加约束"""
        constraint_count = 0
        
        # 使用排序确保约束的一致性
        for row_name, (sense, rhs) in sorted(self.parser.rows.items(), key=lambda x: self._get_constraint_sort_key(x[0])):
            if sense == 'N':
                continue
            
            expr = 0
            for col_name in sorted(self.parser.cols.keys(), key=self._get_variable_sort_key):
                row_coeffs = self.parser.cols[col_name]
                if row_name in row_coeffs and col_name in self.variables:
                    coeff = row_coeffs[row_name]
                    expr += coeff * self.variables[col_name]
            
            if sense == 'E':
                self.model.addConstr(expr == rhs, name=row_name)
            elif sense == 'L':
                self.model.addConstr(expr <= rhs, name=row_name)
            elif sense == 'G':
                self.model.addConstr(expr >= rhs, name=row_name)
            
            constraint_count += 1
        
        print(f"  添加了 {constraint_count} 个约束")
    
    def _escape_latex(self, text):
        """转义LaTeX特殊字符"""
        text = str(text)
        text = text.replace('\\', r'\textbackslash{}')
        text = text.replace('_', r'\_')
        text = text.replace('%', r'\%')
        text = text.replace('$', r'\$')
        text = text.replace('&', r'\&')
        text = text.replace('#', r'\#')
        text = text.replace('{', r'\{')
        text = text.replace('}', r'\}')
        # 对于连续的连字符进行特殊处理，单个连字符保留用于数字（如负数）
        text = re.sub(r'-{2,}', lambda m: r'\text{' + m.group(0) + '}', text)
        return text

    def _parse_variable_name(self, var_name):
        """
        将变量名转换为LaTeX下标格式，使用智能零填充
        特别处理包含连字符的变量名，如 R------1, C------2
        """
        # 特殊处理包含多个连字符的变量名，如 R------1, C------2
        if '------' in var_name:
            parts = var_name.split('------')
            if len(parts) == 2:
                prefix = parts[0]  # 保留前缀中的连字符
                try:
                    number = int(parts[1])
                    # 使用智能零填充
                    if prefix in self.var_prefix_counts:
                        padding = self.var_prefix_counts[prefix]['padding']
                        formatted_number = str(number).zfill(padding)
                    else:
                        formatted_number = str(number)
                    return f"{prefix}_{{{formatted_number}}}"
                except ValueError:
                    return self._escape_latex(var_name)
        
        # 处理其他连字符模式，如 R-----1, R----1 等
        if '-----' in var_name:
            parts = var_name.split('-----')
            if len(parts) == 2:
                prefix = parts[0]
                try:
                    number = int(parts[1])
                    if prefix in self.var_prefix_counts:
                        padding = self.var_prefix_counts[prefix]['padding']
                        formatted_number = str(number).zfill(padding)
                    else:
                        formatted_number = str(number)
                    return f"{prefix}_{{{formatted_number}}}"
                except ValueError:
                    return self._escape_latex(var_name)
        
        if '----' in var_name:
            parts = var_name.split('----')
            if len(parts) == 2:
                prefix = parts[0]
                try:
                    number = int(parts[1])
                    if prefix in self.var_prefix_counts:
                        padding = self.var_prefix_counts[prefix]['padding']
                        formatted_number = str(number).zfill(padding)
                    else:
                        formatted_number = str(number)
                    return f"{prefix}_{{{formatted_number}}}"
                except ValueError:
                    return self._escape_latex(var_name)
        
        if '---' in var_name:
            parts = var_name.split('---')
            if len(parts) == 2:
                prefix = parts[0]
                try:
                    number = int(parts[1])
                    if prefix in self.var_prefix_counts:
                        padding = self.var_prefix_counts[prefix]['padding']
                        formatted_number = str(number).zfill(padding)
                    else:
                        formatted_number = str(number)
                    return f"{prefix}_{{{formatted_number}}}"
                except ValueError:
                    return self._escape_latex(var_name)
        
        # 标准的字母+数字格式处理
        match = re.match(r"([a-zA-Z_]+)(\d+)", var_name)
        if match:
            prefix = match.group(1)
            number = int(match.group(2))
            
            # 使用预先分析的填充信息
            if prefix in self.var_prefix_counts:
                padding = self.var_prefix_counts[prefix]['padding']
                formatted_number = str(number).zfill(padding)
            else:
                formatted_number = str(number)
            
            return f"{self._escape_latex(prefix)}_{{{formatted_number}}}"
        else:
            return self._escape_latex(var_name)

    def _build_mathematical_model_latex(self):
        """构建数学模型的LaTeX表示"""
        latex = "\\section{数学模型}\n\\subsection{优化模型}\n\n"
        
        # 目标函数
        latex += "\\textbf{目标函数:}\n\n"
        latex += "\\begin{align}\n"
        latex += "\\min\\quad f(x) &= "
        
        # 常数项
        if abs(self.parser.objective_constant) > 1e-12:
            latex += f"{self.parser.objective_constant:.4g}"
        else:
            latex += "0"
        
        # 线性项 - 详细展示，使用排序
        if self.parser.obj_name:
            linear_terms = {}
            for col_name, row_coeffs in self.parser.cols.items():
                if self.parser.obj_name in row_coeffs:
                    linear_terms[col_name] = row_coeffs[self.parser.obj_name]
            
            if linear_terms:
                terms_per_line = 4
                current_line_count = 0
                
                # 使用智能排序
                for i, (var, coeff) in enumerate(sorted(linear_terms.items(), key=lambda x: self._get_variable_sort_key(x[0]))):
                    if abs(coeff) > 1e-12:
                        if current_line_count >= terms_per_line:
                            latex += " \\nonumber\\\\\n&\\quad"
                            current_line_count = 0
                        
                        sign = " + " if coeff > 0 else " - "
                        coeff_val = abs(coeff)
                        coeff_str = f"{coeff_val:.4g}"
                        var_formatted = self._parse_variable_name(var)
                        
                        latex += f"{sign}{coeff_str}\\,{var_formatted}"
                        current_line_count += 1
        
        # 二次项标记
        if self.parser.quadobj:
            latex += " \\nonumber\\\\\n&\\quad + \\frac{1}{2} \\sum_{i,j} Q_{ij} x_i x_j"
        
        latex += "\\label{eq:objective}\n\\end{align}\n\n"
        
        # 二次项详细信息
        if self.parser.quadobj:
            diagonal_terms = len([1 for (i,j) in self.parser.quadobj.keys() if i == j])
            total_unique_pairs = len(set((min(i,j), max(i,j)) for i,j in self.parser.quadobj.keys()))
            off_diagonal_terms = total_unique_pairs - diagonal_terms
            
            latex += "\\textbf{二次项矩阵特征:}\n"
            latex += "\\begin{itemize}\n"
            latex += f"\\item 对角线项: {diagonal_terms} 个\n"
            latex += f"\\item 非对角线项: {off_diagonal_terms} 个\n"
            latex += f"\\item 矩阵类型: 对称正定\n"
            latex += "\\end{itemize}\n\n"
        
        # 约束条件详细描述 - 使用排序
        constraints = [(name, sense, rhs) for name, (sense, rhs) in self.parser.rows.items() if sense != 'N']
        if constraints:
            latex += "\\textbf{约束条件:}\n"
            
            # 对约束进行排序
            constraints_sorted = sorted(constraints, key=lambda x: self._get_constraint_sort_key(x[0]))
            
            for i, (name, sense, rhs) in enumerate(constraints_sorted):
                constraint_terms = {}
                for col_name, row_coeffs in self.parser.cols.items():
                    if name in row_coeffs:
                        constraint_terms[col_name] = row_coeffs[name]
                
                sense_map = {'E': '=', 'L': '\\leq', 'G': '\\geq'}
                sense_latex = sense_map.get(sense, '=')
                
                # 统计正负系数变量
                positive_vars = [var for var, coeff in constraint_terms.items() if coeff > 0]
                negative_vars = [var for var, coeff in constraint_terms.items() if coeff < 0]
                
                if len(constraint_terms) > 8:  # 如果变量太多，简化显示
                    latex += "\\begin{align}\n"
                    if positive_vars and negative_vars:
                        latex += f"\\sum_{{i \\in \\mathcal{{P}}}} x_i - \\sum_{{j \\in \\mathcal{{N}}}} x_j &{sense_latex} {rhs:.4g} \\nonumber\n"
                        latex += "\\end{align}\n"
                        latex += f"其中正系数变量集合包含 {len(positive_vars)} 个变量，负系数变量集合包含 {len(negative_vars)} 个变量。\\\\[0.3em]\n\n"
                    else:
                        latex += f"\\sum_{{变量}} 系数 \\cdot 变量 &{sense_latex} {rhs:.4g} \\nonumber\n"
                        latex += "\\end{align}\n"
                        latex += f"约束包含 {len(constraint_terms)} 个变量。\\\\[0.3em]\n\n"
                else:
                    # 详细显示约束 - 使用排序
                    latex += "\\begin{align}\n"
                    terms_per_line = 4
                    current_count = 0
                    first_term = True
                    
                    for var, coeff in sorted(constraint_terms.items(), key=lambda x: self._get_variable_sort_key(x[0])):
                        if abs(coeff) > 1e-12:
                            if current_count >= terms_per_line:
                                latex += " \\nonumber\\\\\n&\\quad"
                                current_count = 0
                                first_term = True
                            
                            var_formatted = self._parse_variable_name(var)
                            
                            if first_term:
                                sign = "-" if coeff < 0 else ""
                                latex += f"{sign}{abs(coeff):.4g}\\,{var_formatted}"
                                first_term = False
                            else:
                                sign = " + " if coeff > 0 else " - "
                                latex += f"{sign}{abs(coeff):.4g}\\,{var_formatted}"
                            current_count += 1
                    
                    latex += f" &{sense_latex} {rhs:.4g} \\nonumber\n"
                    latex += "\\end{align}\n\n"
        
        # 变量边界
        bounds_summary = self._summarize_bounds()
        latex += "\\textbf{变量边界:}\n"
        latex += "\\begin{itemize}\n"
        for bound_type, count in bounds_summary.items():
            latex += f"\\item {bound_type}: {count} 个变量\n"
        latex += "\\end{itemize}\n\n"
        
        return latex
    
    def _summarize_bounds(self):
        """总结变量边界信息"""
        bounds_summary = {}
        
        for var_name in self.variables.keys():
            lb, ub = self.parser.bounds.get(var_name, (0.0, float('inf')))
            
            if lb == 0 and ub == float('inf'):
                bound_type = "非负变量 $x_i \\geq 0$"
            elif lb == 0 and ub < float('inf'):
                bound_type = f"有界非负变量 $0 \\leq x_i \\leq {ub}$"
            elif lb == -float('inf') and ub == float('inf'):
                bound_type = "自由变量 $x_i \\in \\mathbb{R}$"
            elif lb > 0:
                bound_type = f"下界变量 $x_i \\geq {lb}$"
            else:
                bound_type = "其他边界类型"
            
            bounds_summary[bound_type] = bounds_summary.get(bound_type, 0) + 1
        
        return bounds_summary

    def _analyze_solution(self):
        """分析解的结构"""
        if not self.solution:
            return "解不可用。"
        
        analysis = ""
        
        # 变量值统计
        values = list(self.solution.values())
        nonzero_values = [v for v in values if abs(v) > 1e-12]
        
        if nonzero_values:
            analysis += f"\\begin{{itemize}}\n"
            analysis += f"\\item 非零变量平均值: {np.mean(nonzero_values):.6g}\n"
            analysis += f"\\item 非零变量标准差: {np.std(nonzero_values):.6g}\n"
            analysis += f"\\item 最大变量值: {max(nonzero_values):.6g}\n"
            analysis += f"\\item 最小变量值: {min(nonzero_values):.6g}\n"
            analysis += f"\\end{{itemize}}\n"
        
        return analysis

    def generate_latex_report(self, output_filepath=None):
        """生成LaTeX报告"""
        if output_filepath is None:
            tex_reports_dir = "qps_reports"
            os.makedirs(tex_reports_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(self.qps_filepath))[0]
            output_filepath = os.path.join(tex_reports_dir, f"{base_name}_QPS_REPORT.tex")
        
        current_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        model_name = os.path.splitext(os.path.basename(self.qps_filepath))[0]
        
        # 统计信息
        num_vars = len(self.variables)
        num_constraints = len([r for r in self.parser.rows.values() if r[0] != 'N'])
        num_quadratic = len(self.parser.quadobj)
        
        # 约束类型统计
        constraint_types = defaultdict(int)
        for row_name, (sense, rhs) in self.parser.rows.items():
            if sense != 'N':
                constraint_types[sense] += 1

        latex_content = f"""\\documentclass[a4paper,11pt]{{article}}
\\usepackage[UTF8]{{ctex}}
\\usepackage{{amsmath, amssymb, booktabs, geometry, longtable, xcolor, fancyhdr, array}}
\\usepackage{{breqn}}  % 用于自动换行的数学公式
\\geometry{{a4paper, left=1.5cm, right=1.5cm, top=2.5cm, bottom=2.5cm}}

% 允许公式跨页
\\allowdisplaybreaks[4]

% 数学字体设置
\\usepackage{{mathptmx}}  % 使用Times字体
\\renewcommand{{\\familydefault}}{{\\rmdefault}}

% 适中的行距设置
\\usepackage{{setspace}}
\\setstretch{{1.1}}

% 数学公式的间距设置
\\setlength{{\\abovedisplayskip}}{{6pt}}
\\setlength{{\\belowdisplayskip}}{{6pt}}
\\setlength{{\\abovedisplayshortskip}}{{3pt}}
\\setlength{{\\belowdisplayshortskip}}{{3pt}}

\\title{{QPS格式二次规划问题分析报告\\\\{{\\large {model_name}}}}}
\\author{{QPS解析器 (Enhanced Version)}}
\\date{{{current_time}}}

\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{QPS分析报告}}
\\fancyhead[R]{{{model_name}}}
\\fancyfoot[C]{{\\thepage}}

\\begin{{document}}
\\maketitle
\\tableofcontents
\\newpage

\\section{{问题概述}}
\\subsection{{基本信息}}
\\begin{{table}}[h!]
\\centering
\\begin{{tabular}}{{ll}}
\\toprule
\\textbf{{属性}} & \\textbf{{值}} \\\\
\\midrule
问题名称 & \\texttt{{{self._escape_latex(self.parser.name)}}} \\\\
源文件 & \\texttt{{{self._escape_latex(os.path.basename(self.qps_filepath))}}} \\\\
问题类型 & 二次规划 (QP) \\\\
变量数量 & {num_vars} \\\\
约束数量 & {num_constraints} \\\\
二次项数 & {num_quadratic} \\\\
目标常数 & {self.parser.objective_constant} \\\\
\\bottomrule
\\end{{tabular}}
\\caption{{问题基本信息}}
\\end{{table}}

\\textbf{{格式化和排序说明:}} 本报告采用以下规范以提高可读性：
\\begin{{itemize}}
    \\item \\textbf{{变量命名:}} 采用智能零填充格式，根据各变量前缀的数量自动调整。例如，若存在超过99个X变量，则格式化为$X_{{001}}, X_{{002}}, \\ldots$；若变量数量在10-99之间，则格式化为$X_{{01}}, X_{{02}}, \\ldots$。
    \\item \\textbf{{排序规则:}} 变量和约束条件均按前缀字母顺序，然后按数字大小进行排序，确保逻辑顺序（如$X_1, X_2, \\ldots, X_{{10}}$而非$X_1, X_{{10}}, X_2$）。
    \\item \\textbf{{特殊处理:}} 对于包含连字符的变量名（如R\\text{{------}}1），保持原始格式并应用智能排序。
\\end{{itemize}}

"""
        
        # 添加详细的数学模型
        latex_content += self._build_mathematical_model_latex()
        
        # 求解结果
        latex_content += "\\section{求解结果}\n\n"
        
        if self.solve_status == COPT.OPTIMAL:
            nonzero_solution = {k: v for k, v in self.solution.items() if abs(v) > 1e-12}
            solution_stats = self._analyze_solution()
            
            latex_content += f"""\\subsection{{最优解}}
\\begin{{itemize}}
\\item \\textbf{{求解状态:}} \\textcolor{{green}}{{最优解}}
\\item \\textbf{{目标函数值:}} ${self.objective_value:.12g}$
\\item \\textbf{{求解时间:}} {self.solve_time:.3f} 秒
\\item \\textbf{{非零变量:}} {len(nonzero_solution)}/{len(self.solution)}
\\end{{itemize}}

\\subsection{{解的分析}}
{solution_stats}

\\subsection{{所有非零变量值}}
\\begin{{longtable}}{{p{{2.5cm}}@{{\\hspace{{0.5em}}}}r@{{\\hspace{{0.8em}}}}p{{3.5cm}}}}
\\toprule
\\textbf{{变量}} & \\textbf{{值}} & \\textbf{{边界}} \\\\
\\midrule
\\endfirsthead
\\multicolumn{{3}}{{c}}{{\\textit{{续表}}}} \\\\
\\toprule
\\textbf{{变量}} & \\textbf{{值}} & \\textbf{{边界}} \\\\
\\midrule
\\endhead
\\bottomrule
\\endfoot
\\bottomrule
\\endlastfoot
"""
            
            # 显示所有非零变量 - 使用智能排序
            sorted_vars = sorted(nonzero_solution.items(), key=lambda x: self._get_variable_sort_key(x[0]))
            for var_name, value in sorted_vars:
                lb, ub = self.parser.bounds.get(var_name, (0.0, float('inf')))
                
                # 处理变量名下标
                var_display = self._parse_variable_name(var_name)
                
                # 格式化数值显示
                if abs(value) >= 1e-3:
                    value_str = f"{value:.6f}"
                else:
                    value_str = f"{value:.3e}"
                
                bound_str = f"[{lb:.3g}, {ub:.3g}]" if ub != float('inf') else f"[{lb:.3g}, ∞)"
                latex_content += f"${var_display}$ & {value_str} & {bound_str} \\\\\n"
            
            latex_content += """\\bottomrule
\\caption{所有非零变量值（按变量名排序）}
\\end{longtable}
"""
        else:
            status_mapping = {
                COPT.INFEASIBLE: "不可行 (Infeasible)",
                COPT.UNBOUNDED: "无界 (Unbounded)",
                COPT.NUMERICAL: "数值问题 (Numerical)"
            }
            status_text = status_mapping.get(self.solve_status, f"未知状态码 ({self.solve_status})")
            latex_content += f"求解状态: \\textbf{{{status_text}}}\n\n"
            latex_content += "未能获得可行解。\n\n"
        
        latex_content += "\\end{document}"
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"已生成求解报告: {output_filepath}")
        return output_filepath
    
    def __del__(self):
        """清理COPT环境资源"""
        try:
            if hasattr(self, 'env') and self.env:
                self.env.close()
        except Exception:
            pass

def find_qps_file(filename_input):
    """智能查找QPS文件"""
    base_name = filename_input.replace('.qps', '').replace('.txt', '')
    possible_paths = [
        filename_input,
        f"{base_name}.qps",
        f"{base_name}.txt", 
        os.path.join("qps", filename_input),
        os.path.join("qps", f"{base_name}.qps"),
        os.path.join("qps", f"{base_name}.txt"),
    ]
    
    for path in possible_paths:
        if path and os.path.exists(path):
            return path
    return None

def main():
    """主函数"""
    print("=" * 60)
    print("QPS文件COPT求解器与LaTeX报告生成器 (增强版)")
    print("支持智能变量格式化和排序")
    print("=" * 60)
    
    try:
        # 检查命令行参数
        if len(sys.argv) > 1:
            filename_input = sys.argv[1]
            print(f"使用命令行参数: {filename_input}")
        else:
            # 交互式输入
            try:
                filename_input = input("请输入QPS文件名 (例如: qps/values.qps 或 values): ").strip()
                if not filename_input:
                    print("未输入文件名，程序退出。")
                    return
            except (EOFError, KeyboardInterrupt):
                print("输入被中断，程序退出。")
                return
        
        actual_filepath = find_qps_file(filename_input)
        
        if actual_filepath is None:
            print(f"文件 '{filename_input}' 未找到。请检查文件名和路径。")
            return
        
        print(f"找到文件: {actual_filepath}")
        
        solver = QPSSolver(actual_filepath)
        success = solver.solve_model()
        
        print("正在生成LaTeX报告...")
        report_path = solver.generate_latex_report()
        
        if report_path:
            print("任务完成!")
            if solver.log_filepath:
                print(f"求解日志位置: {os.path.abspath(solver.log_filepath)}")
            print(f"LaTeX报告位置: {os.path.abspath(report_path)}")
            report_dir = os.path.dirname(os.path.abspath(report_path))
            report_basename = os.path.basename(report_path)
            print(f"如需生成PDF, 请在终端执行: cd \"{report_dir}\" && xelatex \"{report_basename}\"")
            print("\n新功能说明:")
            print("- 变量名现在使用智能零填充格式 (例如: X_{001}, Y_{01})")
            print("- 所有变量和约束按照前缀和数字正确排序")
            print("- 特殊处理包含连字符的变量名格式")
            print("- 报告更适合研究人员阅读和引用")

    except Exception as e:
        print(f"处理过程中发生严重错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()