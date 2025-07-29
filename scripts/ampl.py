#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AMPL模型求解器与LaTeX报告生成器 (增强版)

本脚本基于AMPL Python API开发。
主要功能:
- 读取AMPL模型文件(.mod)和数据文件(.dat)
- 使用AMPL调用多种求解器求解
- 生成完整的LaTeX格式报告
- 支持智能变量格式化和排序
- 自动识别模型结构并生成专业报告

详细中文注释:
这个脚本是一个用于处理AMPL模型的完整工具。它可以自动读取AMPL格式的数学规划模型，
调用多种求解器（如Gurobi, CPLEX, COPT等）求解这些模型，并生成详细的LaTeX格式报告。
该脚本支持智能变量格式化，可以根据变量数量自动调整显示格式，还能自动识别模型结构，
从而生成结构化的专业报告。适用于研究人员分析和展示优化模型的结果。
"""

import os
import re
import datetime
import sys
import time
import traceback
import numpy as np
from pathlib import Path
from collections import defaultdict

try:
    from amplpy import AMPL, Environment
    AMPL_AVAILABLE = True
except ImportError:
    AMPL_AVAILABLE = False
    print("警告: amplpy未安装。请运行: pip install amplpy")

class AMPLSolver:
    """
    AMPL模型求解器，生成完整且页面友好的LaTeX格式报告
    
    这个类是整个程序的核心，负责处理AMPL模型和数据文件，调用求解器求解问题，
    并生成格式化的LaTeX报告。它实现了多种求解器的自动检测和选择，智能变量格式化，
    以及详细的结果分析和可视化。
    """
    
    def __init__(self, model_filepath, data_filepath=None):
        """
        初始化AMPL求解器对象
        
        参数:
        model_filepath - AMPL模型文件(.mod)的路径
        data_filepath - AMPL数据文件(.dat)的路径，可选
        
        这个初始化方法设置了求解器的基本属性，检查必要的库是否可用，并验证输入文件是否存在。
        它还初始化了存储求解结果、模型信息和格式化设置的多个数据结构。
        """
        if not AMPL_AVAILABLE:
            raise ImportError("amplpy库未安装，无法使用AMPL求解器")
        
        self.model_filepath = model_filepath  # 模型文件路径
        self.data_filepath = data_filepath    # 数据文件路径
        self.ampl = None                      # AMPL环境对象
        self.solve_status = None              # 求解状态
        self.objective_value = None           # 目标函数值
        self.solution = {}                    # 变量解值字典
        self.model_info = {}                  # 模型基本信息
        self.constraints_info = {}            # 约束信息
        self.variables_info = {}              # 变量信息
        self.solve_time = 0                   # 求解时间
        self.solver_name = "auto"             # 求解器名称，默认为自动选择
        self.log_filepath = None              # 日志文件路径
        self.var_prefix_counts = {}           # 存储每个变量前缀的计数信息，用于智能格式化
        
        # 检查文件存在性
        if not os.path.exists(model_filepath):
            raise FileNotFoundError(f"模型文件不存在: {model_filepath}")
        if data_filepath and not os.path.exists(data_filepath):
            raise FileNotFoundError(f"数据文件不存在: {data_filepath}")
    
    def _log_message(self, message):
        """
        记录消息到日志文件
        
        参数:
        message - 要记录的消息文本
        
        这个方法负责将操作和错误信息记录到指定的日志文件中，附加时间戳以便于追踪。
        它使用异常处理确保即使写入失败也不会中断主程序流程。
        """
        if self.log_filepath:
            try:
                with open(self.log_filepath, 'a', encoding='utf-8') as log_file:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    log_file.write(f"[{timestamp}] {message}\n")
            except Exception as e:
                print(f"写入日志失败: {e}")
    
    def _analyze_variable_patterns(self, variables):
        """
        分析变量模式，确定每个前缀的变量数量和所需的零填充位数
        
        参数:
        variables - 变量名列表
        
        这个方法分析所有变量名的模式，识别不同前缀(如x、y)的变量，并确定每种前缀下的最大数值，
        从而决定在LaTeX格式化输出时应使用多少位的零填充。例如，如果x变量超过100个，
        就会使用三位数格式(x_{001}, x_{002}...)，这样在排序和显示时可以保持正确的顺序。
        这是本程序智能格式化功能的核心部分。
        """
        prefix_max_numbers = defaultdict(int)
        
        for var_name in variables:
            # 处理带下标的变量名，如 x[1,2], y[10], z[i,j,k]
            base_match = re.match(r"([a-zA-Z_]+)", var_name)
            if base_match:
                prefix = base_match.group(1)
                
                # 提取所有数字下标
                numbers = re.findall(r'\d+', var_name)
                if numbers:
                    # 使用最大的数字作为参考
                    max_num = max(int(num) for num in numbers)
                    prefix_max_numbers[prefix] = max(prefix_max_numbers[prefix], max_num)
        
        # 确定每个前缀需要的零填充位数
        for prefix, max_num in prefix_max_numbers.items():
            if max_num >= 100:
                padding = 3  # 001, 002, ..., 999 - 三位数填充
            elif max_num >= 10:
                padding = 2  # 01, 02, ..., 99 - 两位数填充
            else:
                padding = 1  # 1, 2, ..., 9 - 无需填充
            
            self.var_prefix_counts[prefix] = {
                'max_number': max_num,
                'padding': padding
            }
    
    def _get_variable_sort_key(self, var_name):
        """
        生成用于排序的键值，确保变量按照前缀和下标正确排序
        
        参数:
        var_name - 变量名
        
        返回:
        排序键 - 用于确定变量排序顺序的元组
        
        这个方法处理各种复杂的变量命名格式，如 x[1,2], y[10], z[i,j] 等，
        通过提取变量前缀和数字下标，生成适合排序的键值。这确保了变量在报告中
        按照逻辑顺序显示，例如 x[1,1], x[1,2], ..., x[2,1] 而不是字典序。
        这对于多维数组变量的可读性至关重要。
        """
        # 提取变量基名
        base_match = re.match(r"([a-zA-Z_]+)", var_name)
        if base_match:
            prefix = base_match.group(1)
            
            # 提取数字下标
            numbers = re.findall(r'\d+', var_name)
            if numbers:
                # 将所有数字转换为整数并作为排序键
                number_tuple = tuple(int(num) for num in numbers)
                return (prefix, number_tuple)
            else:
                # 如果没有数字，按字母顺序排序
                return (prefix, (0,))
        else:
            return (var_name, (0,))
    
    def _get_constraint_sort_key(self, cons_name):
        """
        生成用于约束排序的键值
        
        参数:
        cons_name - 约束名称
        
        返回:
        排序键 - 用于确定约束排序顺序的元组
        
        这个方法与变量排序方法类似，专门用于处理约束名称的排序。
        它确保约束按照有意义的顺序在报告中呈现，如 const1, const2, const10
        而不是 const1, const10, const2，这对于大型模型的可读性非常重要。
        """
        base_match = re.match(r"([a-zA-Z_]+)", cons_name)
        if base_match:
            prefix = base_match.group(1)
            numbers = re.findall(r'\d+', cons_name)
            if numbers:
                number_tuple = tuple(int(num) for num in numbers)
                return (prefix, number_tuple)
            else:
                return (prefix, (0,))
        else:
            return (cons_name, (0,))
    
    def _escape_latex(self, text):
        """
        转义LaTeX特殊字符
        
        参数:
        text - 需要转义的文本
        
        返回:
        转义后的文本，可安全用于LaTeX文档
        
        这个方法处理所有可能在LaTeX中引起解析问题的特殊字符，
        将它们转换为对应的LaTeX转义序列。这是生成稳定、无错误LaTeX报告的基础。
        """
        text = str(text)
        replacements = {
            '\\': r'\textbackslash{}',  # 反斜杠
            '_': r'\_',                 # 下划线(在LaTeX中用于下标)
            '%': r'\%',                 # 百分号(在LaTeX中用于注释)
            '$': r'\$',                 # 美元符号(在LaTeX中用于数学模式)
            '&': r'\&',                 # 与符号(在LaTeX中用于表格列分隔)
            '#': r'\#',                 # 井号(在LaTeX中用于参数)
            '{': r'\{',                 # 左花括号(在LaTeX中用于分组)
            '}': r'\}',                 # 右花括号(在LaTeX中用于分组)
            '^': r'\textasciicircum{}', # 脱字符(在LaTeX中用于上标)
            '~': r'\textasciitilde{}'   # 波浪号(在LaTeX中用于不间断空格)
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text
    
    def _parse_variable_name(self, var_name):
        """
        将AMPL变量名转换为LaTeX格式，使用智能零填充
        
        参数:
        var_name - AMPL变量名
        
        返回:
        格式化后的LaTeX变量名表示
        
        这个方法是智能变量格式化功能的核心实现，它将AMPL中的变量名(如x[1,2], y[10])
        转换为格式化的LaTeX表示(如x_{01,02}, y_{10})。对于数字下标，它应用前面
        分析得出的零填充规则，确保视觉一致性和正确排序。对于符号下标，则保留原样。
        这对于多维索引的变量特别有用，使得最终报告更加专业和易读。
        
        例如:
        - x[1,2] -> x_{01,02}  (当有超过10个但少于100个x变量时)
        - y[10] -> y_{10}      (当y变量不需要零填充时)
        - z[i,j] -> z_{i,j}    (保留符号下标)
        """
        # 提取变量基名
        base_match = re.match(r"([a-zA-Z_]+)", var_name)
        if base_match:
            prefix = base_match.group(1)
            
            # 查找方括号内的内容
            bracket_match = re.search(r'\[([^\]]+)\]', var_name)
            if bracket_match:
                indices = bracket_match.group(1)
                
                # 处理逗号分隔的多个下标
                index_parts = [part.strip() for part in indices.split(',')]
                formatted_indices = []
                
                for part in index_parts:
                    if part.isdigit():
                        # 数字下标，应用智能零填充
                        number = int(part)
                        if prefix in self.var_prefix_counts:
                            padding = self.var_prefix_counts[prefix]['padding']
                            formatted_number = str(number).zfill(padding)
                        else:
                            formatted_number = str(number)
                        formatted_indices.append(formatted_number)
                    else:
                        # 非数字下标（如符号索引），保持原样
                        formatted_indices.append(self._escape_latex(part))
                
                indices_str = ','.join(formatted_indices)
                return f"{self._escape_latex(prefix)}_{{{indices_str}}}"
            else:
                # 没有方括号，可能是简单变量名
                return self._escape_latex(prefix)
        else:
            return self._escape_latex(var_name)
    
    def _detect_available_solvers(self):
        """检测可用的求解器"""
        available_solvers = []
        test_solvers = ['gurobi', 'cplex', 'copt', 'highs', 'cbc', 'ipopt', 'bonmin']
        
        if self.ampl is None:
            return available_solvers
            
        for solver in test_solvers:
            try:
                # 尝试设置求解器，如果可用则不会报错
                original_solver = self.ampl.getOption('solver')
                self.ampl.setOption('solver', solver)
                
                # 检查是否真的设置成功
                current_solver = self.ampl.getOption('solver')
                if current_solver == solver:
                    available_solvers.append(solver)
                
                # 恢复原始设置
                self.ampl.setOption('solver', original_solver)
                
            except Exception:
                continue
                
        return available_solvers
    
    def solve_model(self, solver="auto", options=None):
        """
        求解AMPL模型
        
        参数:
        - solver: 求解器名称 ("gurobi", "cplex", "copt", "auto"等)
        - options: 求解器选项字典
        
        返回:
        布尔值 - 求解是否成功
        
        这是本类的核心方法，负责完成求解过程的全部工作流程：
        1. 初始化AMPL环境并配置许可证
        2. 设置日志文件和路径
        3. 读取模型和数据文件
        4. 提取和分析模型结构信息
        5. 检测和选择合适的求解器
        6. 设置求解器选项并启动求解
        7. 捕获求解结果和状态
        8. 提取变量解值和目标函数值
        
        该方法设计了完善的错误处理和回退策略，确保即使在不理想条件下也能尽可能地完成任务。
        它还实现了多种方法来解析求解器输出，确保能正确获取结果。
        """
        try:
            print("初始化AMPL环境...")
            self.ampl = AMPL()
            self.solver_name = solver
            
            # 配置求解器许可证路径
            try:
                license_dir = os.path.abspath("license")
                if os.path.exists(license_dir):
                    # 设置 Gurobi 许可证
                    gurobi_lic = os.path.join(license_dir, "gurobi.lic")
                    if os.path.exists(gurobi_lic):
                        os.environ['GRB_LICENSE_FILE'] = gurobi_lic
                        print(f"设置 Gurobi 许可证: {gurobi_lic}")
                    
                    # 设置 COPT 许可证
                    copt_lic = os.path.join(license_dir, "license.dat")
                    if os.path.exists(copt_lic):
                        os.environ['COPT_LICENSE_FILE'] = copt_lic
                        print(f"设置 COPT 许可证: {copt_lic}")
                    
                    # 备用 COPT 许可证文件
                    copt_key = os.path.join(license_dir, "license.key")
                    if os.path.exists(copt_key):
                        os.environ['COPT_LICENSE_KEY'] = copt_key
                        print(f"设置 COPT 许可证密钥: {copt_key}")
                        
            except Exception as e:
                print(f"配置许可证时出错: {e}")
            
            # 设置日志文件
            log_dir = "ampl_logs"
            os.makedirs(log_dir, exist_ok=True)
            model_base_name = os.path.splitext(os.path.basename(self.model_filepath))[0]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Include data file name in log filename if data file exists
            if self.data_filepath:
                data_base_name = os.path.splitext(os.path.basename(self.data_filepath))[0]
                log_name = f"{model_base_name}_{data_base_name}_ampl_log_{timestamp}.log"
            else:
                log_name = f"{model_base_name}_ampl_log_{timestamp}.log"
            
            self.log_filepath = os.path.join(log_dir, log_name)
            
            # 初始化日志文件 (使用英文以避免编码问题)
            try:
                with open(self.log_filepath, 'w', encoding='utf-8') as log_file:
                    log_file.write(f"AMPL Solving Log - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write(f"Model File: {self.model_filepath}\n")
                    if self.data_filepath:
                        log_file.write(f"Data File: {self.data_filepath}\n")
                    log_file.write(f"Solver: {solver}\n")
                    log_file.write("=" * 60 + "\n\n")
                print(f"日志将保存到: {self.log_filepath}")
            except Exception as e:
                print(f"创建日志文件时出错: {e}")
            
            print(f"读取模型文件: {self.model_filepath}")
            self._log_message(f"Reading model file: {self.model_filepath}")
            self.ampl.read(self.model_filepath)
            self._log_message("Model file loaded successfully")
            
            # 如果有数据文件，读取数据
            if self.data_filepath:
                print(f"读取数据文件: {self.data_filepath}")
                self._log_message(f"Reading data file: {self.data_filepath}")
                self.ampl.readData(self.data_filepath)
                self._log_message("Data file loaded successfully")
            
            # 提取模型信息
            self._log_message("Starting model information extraction")
            self._extract_model_info()
            self._log_message(f"Model info extracted - Variables: {len(self.variables_info)}, Constraints: {len(self.constraints_info)}")
            
            # 分析变量模式
            variables = list(self.variables_info.keys())
            print("分析变量命名模式...")
            self._log_message("Analyzing variable naming patterns")
            self._analyze_variable_patterns(variables)
            
            # 检测可用求解器
            available_solvers = self._detect_available_solvers()
            print(f"检测到可用求解器: {available_solvers if available_solvers else '无'}")
            self._log_message(f"Available solvers detected: {available_solvers}")
            
            # 设置求解器
            if solver == "auto":
                if available_solvers:
                    # 按优先级选择求解器 - 优先使用商业求解器（现在有许可证了）
                    priority_solvers = ['gurobi', 'copt', 'cplex', 'highs', 'cbc']
                    chosen_solver = None
                    for pref_solver in priority_solvers:
                        if pref_solver in available_solvers:
                            chosen_solver = pref_solver
                            break
                    
                    if chosen_solver:
                        self.ampl.setOption('solver', chosen_solver)
                        self.solver_name = chosen_solver
                        print(f"自动选择求解器: {chosen_solver}")
                        self._log_message(f"Auto-selected solver: {chosen_solver}")
                    else:
                        # 使用第一个可用的求解器
                        chosen_solver = available_solvers[0]
                        self.ampl.setOption('solver', chosen_solver)
                        self.solver_name = chosen_solver
                        print(f"使用可用求解器: {chosen_solver}")
                        self._log_message(f"Using available solver: {chosen_solver}")
                else:
                    print("错误: 未检测到任何可用的求解器!")
                    self._log_message("Error: No available solvers detected!")
                    print("\n解决方案:")
                    print("1. 安装求解器 (如 Gurobi, CPLEX, COPT, HiGHS)")
                    print("2. 确保求解器在 AMPL 中正确配置")
                    print("3. 重新运行并手动指定求解器名称")
                    print("\n免费求解器安装:")
                    print("   pip install highs")
                    print("   或下载 HiGHS solver for AMPL")
                    return False
            else:
                if solver in available_solvers:
                    self.ampl.setOption('solver', solver)
                    print(f"使用指定求解器: {solver}")
                else:
                    print(f"警告: 求解器 '{solver}' 可能不可用，尝试使用...")
                    try:
                        self.ampl.setOption('solver', solver)
                        print(f"成功设置求解器: {solver}")
                    except Exception as e:
                        print(f"无法设置求解器 '{solver}': {e}")
                        if available_solvers:
                            fallback = available_solvers[0]
                            print(f"回退到可用求解器: {fallback}")
                            self.ampl.setOption('solver', fallback)
                            self.solver_name = fallback
                        else:
                            print("没有可用的求解器!")
                            return False
            
            # 设置求解器选项
            if options:
                for option, value in options.items():
                    self.ampl.setOption(option, value)
                    print(f"设置选项: {option} = {value}")
                    self._log_message(f"设置求解器选项: {option} = {value}")
            
            # 记录求解时间
            import time
            start_time = time.time()
            
            print("开始求解模型...")
            self._log_message(f"Starting model solving with solver: {self.solver_name}")
            
            # 捕获求解器输出以解析目标函数值
            import io
            import contextlib
            
            # 创建一个StringIO对象来捕获输出
            solver_output = io.StringIO()
            
            # 使用contextlib重定向标准输出
            with contextlib.redirect_stdout(solver_output):
                self.ampl.solve()
            
            # 获取求解器输出
            output_text = solver_output.getvalue()
            print(output_text)  # 仍然打印到控制台
            self._log_message(f"Solver output: {output_text.strip()}")
            
            # 尝试从求解器输出中解析真实的目标函数值
            real_objective_value = None
            try:
                # 解析Gurobi输出: "optimal solution; objective -464.7531429"
                import re
                gurobi_match = re.search(r'optimal solution;\s*objective\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', output_text)
                if gurobi_match:
                    real_objective_value = float(gurobi_match.group(1))
                    print(f"从Gurobi输出解析得到目标函数值: {real_objective_value}")
                    self._log_message(f"Parsed objective value from Gurobi output: {real_objective_value}")
                
                # 解析COPT输出: "optimal solution; objective -464.7531429"
                if not real_objective_value:
                    copt_match = re.search(r'optimal solution;\s*objective\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', output_text)
                    if copt_match:
                        real_objective_value = float(copt_match.group(1))
                        print(f"从COPT输出解析得到目标函数值: {real_objective_value}")
                        self._log_message(f"Parsed objective value from COPT output: {real_objective_value}")
                
                # 解析HiGHS输出: "optimal solution; objective -464.7531429"
                if not real_objective_value:
                    highs_match = re.search(r'optimal solution;\s*objective\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', output_text)
                    if highs_match:
                        real_objective_value = float(highs_match.group(1))
                        print(f"从HiGHS输出解析得到目标函数值: {real_objective_value}")
                        self._log_message(f"Parsed objective value from HiGHS output: {real_objective_value}")
                        
            except Exception as e:
                print(f"解析求解器输出时出错: {e}")
                self._log_message(f"Error parsing solver output: {e}")
            
            self.solve_time = time.time() - start_time
            self._log_message(f"Solving completed, time elapsed: {self.solve_time:.3f} seconds")
            
            # 获取求解状态
            try:
                solve_result = self.ampl.getValue("solve_result")
                solve_result_num = self.ampl.getValue("solve_result_num")
                self._log_message(f"Solve status: {solve_result} (code: {solve_result_num})")
            except Exception as e:
                print(f"获取求解状态时出错: {e}")
                self._log_message(f"Error getting solve status: {e}")
                solve_result = "unknown"
                solve_result_num = -1
            
            print(f"求解完成，状态: {solve_result}")
            print(f"求解时间: {self.solve_time:.3f} 秒")
            
            # 提取解
            if solve_result in ["solved", "optimal"]:
                self.solve_status = "optimal"
                self._log_message("Solving successful, starting solution extraction")
                
                # 获取目标函数值
                # 优先使用从求解器输出解析的值
                if real_objective_value is not None:
                    self.objective_value = real_objective_value
                    print(f"使用解析的目标函数值: {self.objective_value}")
                    self._log_message(f"Using parsed objective value: {self.objective_value}")
                else:
                    # 回退到API方法
                    try:
                        self.objective_value = self.ampl.getValue("_objective")
                        print(f"目标函数值 (_objective): {self.objective_value}")
                        self._log_message(f"目标函数值: {self.objective_value}")
                    except Exception as e1:
                        print(f"获取 _objective 失败: {e1}")
                        self._log_message(f"Failed to get _objective: {e1}")
                        try:
                            # 尝试其他方式获取目标值
                            objectives = self.ampl.getObjectives()
                            if objectives:
                                obj_name, obj = next(iter(objectives))
                                
                                # 检查目标函数是否是索引化的
                                if obj.numInstances() > 1:
                                    print(f"发现索引化目标函数 {obj_name}，实例数: {obj.numInstances()}")
                                    self._log_message(f"发现索引化目标函数 {obj_name}，实例数: {obj.numInstances()}")
                                    
                                    # 尝试获取第一个实例的值
                                    try:
                                        obj_df = obj.getValues()
                                        if hasattr(obj_df, 'toDict'):
                                            obj_dict = obj_df.toDict()
                                            if obj_dict:
                                                first_key = next(iter(obj_dict))
                                                self.objective_value = obj_dict[first_key]
                                                print(f"目标函数值 ({obj_name}[{first_key}]): {self.objective_value}")
                                                self._log_message(f"目标函数值 ({obj_name}[{first_key}]): {self.objective_value}")
                                            else:
                                                print(f"目标函数 {obj_name} 的字典为空")
                                                self._log_message(f"目标函数 {obj_name} 的字典为空")
                                                self.objective_value = None
                                        else:
                                            # 尝试直接从DataFrame获取第一行
                                            try:
                                                for row in obj_df:
                                                    if hasattr(row, '__len__') and len(row) >= 2:
                                                        key = row[0]
                                                        value = row[1]
                                                        self.objective_value = float(value)
                                                        print(f"目标函数值 ({obj_name}[{key}]): {self.objective_value}")
                                                        self._log_message(f"目标函数值 ({obj_name}[{key}]): {self.objective_value}")
                                                        break
                                                else:
                                                    self.objective_value = None
                                                    print(f"无法从DataFrame提取目标函数值")
                                                    self._log_message(f"无法从DataFrame提取目标函数值")
                                            except Exception as e3:
                                                print(f"从DataFrame提取目标函数值失败: {e3}")
                                                self._log_message(f"从DataFrame提取目标函数值失败: {e3}")
                                                self.objective_value = None
                                    except Exception as e3:
                                        print(f"获取索引化目标函数值失败: {e3}")
                                        self._log_message(f"获取索引化目标函数值失败: {e3}")
                                        self.objective_value = None
                                else:
                                    # 单个目标函数实例
                                    api_value = obj.value()
                                    print(f"API目标函数值 ({obj_name}): {api_value}")
                                    self._log_message(f"API目标函数值 ({obj_name}): {api_value}")
                                    
                                    # 如果API值看起来不合理（接近零），则设为None
                                    if abs(api_value) < 1e-100:
                                        print(f"API目标函数值太小，可能不正确")
                                        self._log_message(f"API目标函数值太小，可能不正确")
                                        self.objective_value = None
                                    else:
                                        self.objective_value = api_value
                            else:
                                print("没有找到目标函数")
                                self._log_message("没有找到目标函数")
                                self.objective_value = None
                        except Exception as e2:
                            print(f"获取目标函数值失败: {e2}")
                            self._log_message(f"获取目标函数值失败: {e2}")
                            self.objective_value = None
                
                # 检查求解状态
                try:
                    solve_status_num = self.ampl.getValue("solve_result_num")
                    print(f"数值求解状态: {solve_status_num}")
                except:
                    pass
                
                # 获取变量值 - 使用正确的AMPL API
                print("提取变量值...")
                for var_name in self.variables_info.keys():
                    try:
                        var = self.ampl.getVariable(var_name)
                        if var is not None:
                            print(f"  处理变量: {var_name} (实例数: {var.numInstances()})")
                            
                            if var.numInstances() == 0:
                                print(f"    警告: 变量 {var_name} 没有实例")
                                continue
                            elif var.numInstances() == 1:
                                # 标量变量
                                try:
                                    value = var.value()
                                    self.solution[var_name] = float(value)
                                    print(f"    标量变量 {var_name} = {value}")
                                except Exception as e:
                                    print(f"    标量变量获取失败: {e}")
                            else:
                                # 数组变量 - 使用正确的AMPL API
                                try:
                                    # 方法1：使用getValues()返回的DataFrame，然后转换为dict
                                    var_df = var.getValues()
                                    print(f"    获取到DataFrame类型: {type(var_df)}")
                                    
                                    # 正确遍历DataFrame
                                    if hasattr(var_df, 'toDict'):
                                        # 如果有toDict方法
                                        values_dict = var_df.toDict()
                                        for key, value in values_dict.items():
                                            full_name = f"{var_name}[{key}]"
                                            self.solution[full_name] = float(value)
                                            print(f"    Dict变量 {full_name} = {value}")
                                    elif hasattr(var_df, 'toPandas'):
                                        # 如果有toPandas方法
                                        pandas_df = var_df.toPandas()
                                        print(f"    转换为Pandas: {pandas_df}")
                                        for index, row in pandas_df.iterrows():
                                            if len(pandas_df.columns) >= 2:
                                                key = row.iloc[0]  # 第一列是索引
                                                value = row.iloc[1]  # 第二列是值
                                                full_name = f"{var_name}[{key}]"
                                                self.solution[full_name] = float(value)
                                                print(f"    Pandas变量 {full_name} = {value}")
                                    else:
                                        # 直接遍历DataFrame
                                        print(f"    尝试直接遍历DataFrame...")
                                        for row in var_df:
                                            print(f"    DataFrame行: {row}, 类型: {type(row)}")
                                            if hasattr(row, '__len__') and len(row) >= 2:
                                                key = row[0]
                                                value = row[1]
                                                full_name = f"{var_name}[{key}]"
                                                self.solution[full_name] = float(value)
                                                print(f"    Row变量 {full_name} = {value}")
                                        
                                except Exception as e1:
                                    print(f"    DataFrame方法失败: {e1}")
                                    try:
                                        # 方法2：通过索引集合逐个获取值
                                        print(f"    尝试通过集合获取索引...")
                                        
                                        # 获取所有集合
                                        sets = self.ampl.getSets()
                                        print(f"    可用集合: {list(sets.keys())}")
                                        
                                        # 查找变量对应的索引集合
                                        index_set = None
                                        for set_name, set_obj in sets.items():
                                            if set_name in ['PRODUCTS', 'ITEMS', 'FACTORIES', 'MARKETS', 'J', 'I']:
                                                index_set = set_obj
                                                set_name_used = set_name
                                                break
                                        
                                        if index_set is not None:
                                            print(f"    使用集合: {set_name_used}")
                                            set_values = list(index_set.getValues())
                                            print(f"    集合值: {set_values}")
                                            
                                            for index_value in set_values:
                                                try:
                                                    # 使用get方法获取特定索引的值
                                                    var_instance = var.get(index_value)
                                                    if var_instance is not None:
                                                        value = var_instance.value()
                                                        full_name = f"{var_name}[{index_value}]"
                                                        self.solution[full_name] = float(value)
                                                        print(f"    集合变量 {full_name} = {value}")
                                                    else:
                                                        print(f"    无法获取变量实例: {var_name}[{index_value}]")
                                                except Exception as e:
                                                    print(f"    获取索引 {index_value} 失败: {e}")
                                        else:
                                            print(f"    未找到合适的索引集合")
                                            
                                    except Exception as e2:
                                        print(f"    集合方法也失败: {e2}")
                                        
                                        # 方法3：使用AMPL命令直接查询
                                        try:
                                            print(f"    尝试使用AMPL命令直接查询...")
                                            
                                            # 使用display命令显示变量
                                            self.ampl.eval(f"display {var_name};")
                                            
                                            # 尝试使用getValue获取具体值
                                            # 首先获取索引范围
                                            sets = self.ampl.getSets()
                                            for set_name in ['PRODUCTS', 'ITEMS', 'FACTORIES', 'MARKETS']:
                                                if set_name in sets:
                                                    index_set = sets[set_name]
                                                    for index_val in index_set.getValues():
                                                        try:
                                                            # 直接查询变量值
                                                            query = f"{var_name}['{index_val}']"
                                                            value = self.ampl.getValue(query)
                                                            full_name = f"{var_name}[{index_val}]"
                                                            self.solution[full_name] = float(value)
                                                            print(f"    查询变量 {full_name} = {value}")
                                                        except Exception as e:
                                                            print(f"    查询 {query} 失败: {e}")
                                                    break
                                            
                                        except Exception as e3:
                                            print(f"    AMPL命令方法也失败: {e3}")
                                            
                                            # 方法4：使用官方文档建议的方式
                                            try:
                                                print(f"    尝试官方API方式...")
                                                # 获取solve_result确认求解成功
                                                if hasattr(self.ampl, 'solve_result'):
                                                    solve_result = self.ampl.solve_result
                                                    print(f"    求解结果: {solve_result}")
                                                
                                                # 使用get_value方法获取变量
                                                sets = self.ampl.getSets()
                                                for set_name in ['PRODUCTS', 'ITEMS', 'FACTORIES', 'MARKETS']:
                                                    if set_name in sets:
                                                        index_set = sets[set_name]
                                                        for index_val in index_set.getValues():
                                                            try:
                                                                # 使用官方API方式
                                                                value = self.ampl.get_value(f"{var_name}['{index_val}']")
                                                                full_name = f"{var_name}[{index_val}]"
                                                                self.solution[full_name] = float(value)
                                                                print(f"    官方API变量 {full_name} = {value}")
                                                            except Exception as e:
                                                                print(f"    官方API获取 {index_val} 失败: {e}")
                                                        break
                                                        
                                            except Exception as e4:
                                                print(f"    官方API方法也失败: {e4}")
                                        
                    except Exception as e:
                        print(f"获取变量 {var_name} 时出错: {e}")
                        continue
                
                print(f"最优目标值: {self.objective_value}")
                
                # 安全地处理变量值统计
                try:
                    # 确保所有值都是数字类型
                    valid_solution = {}
                    for k, v in self.solution.items():
                        try:
                            if isinstance(v, (int, float)):
                                valid_solution[k] = float(v)
                            elif hasattr(v, 'value'):
                                # 如果是AMPL对象，获取其值
                                valid_solution[k] = float(v.value())
                            else:
                                # 尝试转换为float
                                valid_solution[k] = float(v)
                        except (ValueError, TypeError, AttributeError):
                            print(f"    警告: 跳过无效变量值 {k} = {v} (类型: {type(v)})")
                            continue
                    
                    # 更新solution字典
                    self.solution = valid_solution
                    
                    nonzero_vars = {k: v for k, v in self.solution.items() if abs(v) > 1e-12}
                    print(f"非零变量: {len(nonzero_vars)}/{len(self.solution)}")
                    
                    if nonzero_vars:
                        print("非零变量列表:")
                        for var_name, value in sorted(nonzero_vars.items()):
                            print(f"   {var_name} = {value}")
                    else:
                        if len(self.solution) > 0:
                            print("所有变量值都接近零")
                        else:
                            print("没有成功提取到任何变量值")
                            
                except Exception as e:
                    print(f"处理变量值时出错: {e}")
                    print(f"    Solution内容: {self.solution}")
                
                return True
            else:
                self.solve_status = solve_result
                print(f"求解失败: {solve_result}")
                self._log_message(f"求解失败: {solve_result}")
                return False
                
        except Exception as e:
            print(f"求解过程发生错误: {e}")
            self._log_message(f"求解过程发生错误: {e}")
            import traceback
            traceback.print_exc()
            self._log_message(f"错误堆栈: {traceback.format_exc()}")
            return False
    
    def _extract_model_info(self):
        """提取模型结构信息"""
        try:
            # 获取变量信息
            variables = self.ampl.getVariables()
            for var_name, var in variables:
                var_info = {
                    'type': 'continuous',  # AMPL默认
                    'bounds': {},
                    'instances': var.numInstances()
                }
                self.variables_info[var_name] = var_info
            
            # 获取约束信息
            constraints = self.ampl.getConstraints()
            for cons_name, cons in constraints:
                cons_info = {
                    'type': 'constraint',
                    'instances': cons.numInstances()
                }
                self.constraints_info[cons_name] = cons_info
            
            # 获取目标函数信息
            objectives = self.ampl.getObjectives()
            obj_info = {}
            for obj_name, obj in objectives:
                obj_info[obj_name] = {
                    'sense': 'minimize',  # 默认值，可能需要进一步检测
                }
            self.model_info['objectives'] = obj_info
            
            print(f"模型信息提取完成:")
            print(f"  变量: {len(self.variables_info)}")
            print(f"  约束: {len(self.constraints_info)}")
            print(f"  目标函数: {len(obj_info)}")
            
        except Exception as e:
            print(f"提取模型信息时出错: {e}")
    
    def _build_model_summary_latex(self):
        """构建模型摘要的LaTeX"""
        latex = "\\section{模型摘要}\n\n"
        
        # 统计信息
        total_vars = sum(info['instances'] for info in self.variables_info.values())
        total_constraints = sum(info['instances'] for info in self.constraints_info.values())
        
        latex += "\\subsection{基本统计}\n"
        latex += "\\begin{table}[h!]\n\\centering\n"
        latex += "\\begin{tabular}{ll}\n\\toprule\n"
        latex += "\\textbf{属性} & \\textbf{数量} \\\\\n\\midrule\n"
        latex += f"变量类型数 & {len(self.variables_info)} \\\\\n"
        latex += f"变量实例总数 & {total_vars} \\\\\n"
        latex += f"约束类型数 & {len(self.constraints_info)} \\\\\n"
        latex += f"约束实例总数 & {total_constraints} \\\\\n"
        latex += f"目标函数数 & {len(self.model_info.get('objectives', {}))} \\\\\n"
        latex += "\\bottomrule\n\\end{tabular}\n"
        latex += "\\caption{模型规模统计}\n\\end{table}\n\n"
        
        # 变量详情
        if self.variables_info:
            latex += "\\subsection{变量详情}\n"
            latex += "\\begin{table}[h!]\n\\centering\n"
            latex += "\\begin{tabular}{lll}\n\\toprule\n"
            latex += "\\textbf{变量名} & \\textbf{实例数} & \\textbf{类型} \\\\\n\\midrule\n"
            
            # 按变量名排序
            sorted_vars = sorted(self.variables_info.items(), key=lambda x: self._get_variable_sort_key(x[0]))
            for var_name, info in sorted_vars:
                escaped_name = self._escape_latex(var_name)
                latex += f"\\texttt{{{escaped_name}}} & {info['instances']} & {info['type']} \\\\\n"
            
            latex += "\\bottomrule\n\\end{tabular}\n"
            latex += "\\caption{变量类型与实例}\n\\end{table}\n\n"
        
        # 约束详情
        if self.constraints_info:
            latex += "\\subsection{约束详情}\n"
            latex += "\\begin{table}[h!]\n\\centering\n"
            latex += "\\begin{tabular}{ll}\n\\toprule\n"
            latex += "\\textbf{约束名} & \\textbf{实例数} \\\\\n\\midrule\n"
            
            # 按约束名排序
            sorted_constraints = sorted(self.constraints_info.items(), key=lambda x: self._get_constraint_sort_key(x[0]))
            for cons_name, info in sorted_constraints:
                escaped_name = self._escape_latex(cons_name)
                latex += f"\\texttt{{{escaped_name}}} & {info['instances']} \\\\\n"
            
            latex += "\\bottomrule\n\\end{tabular}\n"
            latex += "\\caption{约束类型与实例}\n\\end{table}\n\n"
        
        return latex
    
    def _analyze_solution_structure(self):
        """分析解的结构"""
        if not self.solution:
            return "\\subsection{解的统计特征}\n解信息未成功提取，可能是变量值获取过程中出现问题。\n\n"
        
        analysis = ""
        
        # 安全地处理变量值，确保都是数字
        try:
            numeric_values = []
            for v in self.solution.values():
                try:
                    if isinstance(v, (int, float)):
                        numeric_values.append(float(v))
                    elif hasattr(v, 'value'):
                        numeric_values.append(float(v.value()))
                    else:
                        numeric_values.append(float(v))
                except (ValueError, TypeError, AttributeError):
                    continue
            
            nonzero_values = [v for v in numeric_values if abs(v) > 1e-12]
            
        except Exception as e:
            return f"\\subsection{{解的统计特征}}\n处理解数据时出错: {self._escape_latex(str(e))}。\n\n"
        
        if nonzero_values:
            analysis += "\\subsection{解的统计特征}\n"
            analysis += "\\begin{itemize}\n"
            analysis += f"\\item 总变量数量: {len(numeric_values)}\n"
            analysis += f"\\item 非零变量数量: {len(nonzero_values)}\n"
            analysis += f"\\item 非零变量比例: {len(nonzero_values)/len(numeric_values)*100:.1f}\\%\n"
            analysis += f"\\item 非零变量平均值: {np.mean(nonzero_values):.6g}\n"
            analysis += f"\\item 非零变量标准差: {np.std(nonzero_values):.6g}\n"
            analysis += f"\\item 最大变量值: {max(nonzero_values):.6g}\n"
            analysis += f"\\item 最小非零变量值: {min(nonzero_values):.6g}\n"
            analysis += "\\end{itemize}\n\n"
            
            # 按变量前缀分组统计
            prefix_stats = defaultdict(list)
            for var_name, value in self.solution.items():
                try:
                    if isinstance(value, (int, float)):
                        numeric_value = float(value)
                    elif hasattr(value, 'value'):
                        numeric_value = float(value.value())
                    else:
                        numeric_value = float(value)
                    
                    if abs(numeric_value) > 1e-12:
                        base_match = re.match(r"([a-zA-Z_]+)", var_name)
                        if base_match:
                            prefix = base_match.group(1)
                            prefix_stats[prefix].append(numeric_value)
                            
                except (ValueError, TypeError, AttributeError):
                    continue
            
            if len(prefix_stats) > 1:
                analysis += "\\subsection{按变量类型统计}\n"
                analysis += "\\begin{table}[h!]\n\\centering\n"
                analysis += "\\begin{tabular}{llll}\n\\toprule\n"
                analysis += "\\textbf{变量类型} & \\textbf{非零数量} & \\textbf{平均值} & \\textbf{标准差} \\\\\n\\midrule\n"
                
                for prefix in sorted(prefix_stats.keys()):
                    values = prefix_stats[prefix]
                    escaped_prefix = self._escape_latex(prefix)
                    analysis += f"\\texttt{{{escaped_prefix}}} & {len(values)} & {np.mean(values):.4g} & {np.std(values):.4g} \\\\\n"
                
                analysis += "\\bottomrule\n\\end{tabular}\n"
                analysis += "\\caption{按变量类型的解统计}\n\\end{table}\n\n"
        else:
            analysis += "\\subsection{解的统计特征}\n"
            analysis += f"检测到 {len(numeric_values)} 个变量，但所有变量值都接近零（< 1e-12）。\n\n"
        
        return analysis
    
    def generate_latex_report(self, output_filepath=None):
        """
        生成LaTeX报告
        
        参数:
        output_filepath - 输出文件路径，如不指定则自动生成
        
        返回:
        生成的报告文件路径
        
        这个方法将求解结果和模型信息整合为格式化的LaTeX报告。报告包含：
        1. 基本问题信息和文件源
        2. 模型摘要和统计信息
        3. 求解状态和结果分析
        4. 变量值表格(使用智能格式化)
        5. 原始模型代码摘要
        
        报告采用专业的排版和格式，支持中文，可直接编译为PDF。
        报告的设计考虑了学术研究和专业展示的需求，包含丰富的元信息和格式化说明。
        """
        if output_filepath is None:
            tex_reports_dir = "ampl_reports"
            os.makedirs(tex_reports_dir, exist_ok=True)
            model_base_name = os.path.splitext(os.path.basename(self.model_filepath))[0]
            
            # Include data file name in report filename if data file exists
            if self.data_filepath:
                data_base_name = os.path.splitext(os.path.basename(self.data_filepath))[0]
                report_name = f"{model_base_name}_{data_base_name}_AMPL_REPORT.tex"
            else:
                report_name = f"{model_base_name}_AMPL_REPORT.tex"
            
            output_filepath = os.path.join(tex_reports_dir, report_name)
        
        current_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        model_name = os.path.splitext(os.path.basename(self.model_filepath))[0]
        
        # Include data file info in title if present
        if self.data_filepath:
            data_name = os.path.splitext(os.path.basename(self.data_filepath))[0]
            title_suffix = f" + {data_name}"
        else:
            title_suffix = ""
        
        latex_content = f"""\\documentclass[a4paper,11pt]{{article}}
\\usepackage[UTF8]{{ctex}}
\\usepackage{{amsmath, amssymb, booktabs, geometry, longtable, xcolor, fancyhdr, array}}
\\usepackage{{listings}}  % 用于代码显示
\\geometry{{a4paper, left=1.5cm, right=1.5cm, top=2.5cm, bottom=2.5cm}}

% 允许公式跨页
\\allowdisplaybreaks[4]

% 代码格式设置
\\lstset{{
    basicstyle=\\ttfamily\\small,
    breaklines=true,
    frame=single,
    language=C,
    showstringspaces=false
}}

\\title{{AMPL模型求解分析报告\\\\{{\\large {model_name}{title_suffix}}}}}
\\author{{AMPL求解器 (Enhanced Version)}}
\\date{{{current_time}}}

\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{AMPL分析报告}}
\\fancyhead[R]{{{model_name}{title_suffix}}}
\\fancyfoot[C]{{\\thepage}}

\\begin{{document}}
\\maketitle
\\tableofcontents
\\newpage

\\section{{问题概述}}
\\subsection{{文件信息}}
\\begin{{table}}[h!]
\\centering
\\begin{{tabular}}{{ll}}
\\toprule
\\textbf{{属性}} & \\textbf{{值}} \\\\
\\midrule
模型文件 & \\texttt{{{self._escape_latex(os.path.basename(self.model_filepath))}}} \\\\
"""
        
        if self.data_filepath:
            latex_content += f"数据文件 & \\texttt{{{self._escape_latex(os.path.basename(self.data_filepath))}}} \\\\\n"
        
        latex_content += f"""求解器 & {self._escape_latex(self.solver_name)} \\\\
建模语言 & AMPL \\\\
\\bottomrule
\\end{{tabular}}
\\caption{{文件基本信息}}
\\end{{table}}

\\textbf{{格式化和排序说明:}} 本报告采用以下规范以提高可读性：
\\begin{{itemize}}
    \\item \\textbf{{变量命名:}} 采用智能零填充格式，根据各变量前缀的数量自动调整。例如，若存在超过99个x变量，则格式化为$x_{{001}}, x_{{002}}, \\ldots$；若变量数量在10-99之间，则格式化为$x_{{01}}, x_{{02}}, \\ldots$。
    \\item \\textbf{{排序规则:}} 变量和约束条件均按前缀字母顺序，然后按数字下标进行排序，确保逻辑顺序（如$x_{{1,1}}, x_{{1,2}}, \\ldots, x_{{2,1}}$）。
    \\item \\textbf{{数组处理:}} AMPL数组变量（如$x[i,j]$）按下标组合排序，多维下标按词典序排列。
\\end{{itemize}}

"""
        
        # 添加模型摘要
        latex_content += self._build_model_summary_latex()
        
        # 求解结果
        latex_content += "\\section{求解结果}\n\n"
        
        if self.solve_status == "optimal":
            latex_content += f"""\\subsection{{最优解}}
\\begin{{itemize}}
\\item \\textbf{{求解状态:}} \\textcolor{{green}}{{最优解}}
\\item \\textbf{{求解器:}} {self._escape_latex(self.solver_name)}
\\item \\textbf{{求解时间:}} {self.solve_time:.3f} 秒
"""
            
            if self.objective_value is not None:
                latex_content += f"\\item \\textbf{{目标函数值:}} ${self.objective_value:.12g}$\n"
            
            # 安全地处理变量值
            try:
                # 确保所有值都是数字类型
                valid_solution = {}
                for k, v in self.solution.items():
                    try:
                        if isinstance(v, (int, float)):
                            valid_solution[k] = float(v)
                        elif hasattr(v, 'value'):
                            valid_solution[k] = float(v.value())
                        else:
                            valid_solution[k] = float(v)
                    except (ValueError, TypeError, AttributeError):
                        continue
                
                nonzero_solution = {k: v for k, v in valid_solution.items() if abs(v) > 1e-12}
                
            except Exception as e:
                print(f"LaTeX生成时处理变量值出错: {e}")
                valid_solution = {}
                nonzero_solution = {}
            
            latex_content += f"\\item \\textbf{{总变量数:}} {len(valid_solution)}\n"
            latex_content += f"\\item \\textbf{{非零变量:}} {len(nonzero_solution)}\n"
            latex_content += "\\end{itemize}\n\n"
            
            # 解的分析
            # 临时更新solution用于分析
            original_solution = self.solution
            self.solution = valid_solution
            solution_analysis = self._analyze_solution_structure()
            self.solution = original_solution
            latex_content += solution_analysis
            
            # 变量值表格
            if nonzero_solution:
                latex_content += """\\subsection{非零变量值}
\\begin{longtable}{p{3.5cm}@{\\hspace{0.5em}}r@{\\hspace{0.8em}}p{2.5cm}}
\\toprule
\\textbf{变量} & \\textbf{值} & \\textbf{类型} \\\\
\\midrule
\\endfirsthead
\\multicolumn{3}{c}{\\textit{续表}} \\\\
\\toprule
\\textbf{变量} & \\textbf{值} & \\textbf{类型} \\\\
\\midrule
\\endhead
\\bottomrule
\\endfoot
\\bottomrule
\\endlastfoot
"""
                
                # 使用智能排序显示变量
                sorted_vars = sorted(nonzero_solution.items(), key=lambda x: self._get_variable_sort_key(x[0]))
                
                for var_name, value in sorted_vars:
                    # 格式化变量名
                    var_display = self._parse_variable_name(var_name)
                    
                    # 格式化数值
                    try:
                        if abs(float(value)) >= 1e-3:
                            value_str = f"{float(value):.6f}"
                        else:
                            value_str = f"{float(value):.3e}"
                    except (ValueError, TypeError):
                        value_str = str(value)
                    
                    # 确定变量类型
                    base_match = re.match(r"([a-zA-Z_]+)", var_name)
                    var_type = base_match.group(1) if base_match else "未知"
                    var_type_escaped = self._escape_latex(var_type)
                    
                    latex_content += f"${var_display}$ & {value_str} & \\texttt{{{var_type_escaped}}} \\\\\n"
                
                latex_content += """\\bottomrule
\\caption{所有非零变量值（按变量名逻辑排序）}
\\end{longtable}
"""
            else:
                latex_content += "\\subsection{变量值}\n\n"
                if len(valid_solution) > 0:
                    latex_content += f"模型包含 {len(valid_solution)} 个变量，但所有变量值都接近零（< 1e-12）。\n\n"
                    latex_content += "\\textbf{可能原因:}\n"
                    latex_content += "\\begin{itemize}\n"
                    latex_content += "\\item 最优解中所有变量值确实为零\n"
                    latex_content += "\\item 变量值在数值精度范围内为零\n"
                    latex_content += "\\end{itemize}\n\n"
                else:
                    latex_content += "未能提取到任何有效的变量值。\n\n"
                    latex_content += "\\textbf{可能原因:}\n"
                    latex_content += "\\begin{itemize}\n"
                    latex_content += "\\item AMPL变量值提取过程中出现问题\n"
                    latex_content += "\\item 变量索引格式不匹配\n"
                    latex_content += "\\item API调用方式不正确\n"
                    latex_content += "\\end{itemize}\n\n"
        else:
            status_text = self._escape_latex(str(self.solve_status))
            latex_content += f"\\textbf{{求解状态:}} \\textcolor{{red}}{{{status_text}}}\n\n"
            latex_content += "模型求解失败或未找到最优解。\n\n"
        
        # 模型文件内容（可选）
        latex_content += "\\section{模型文件内容}\n\n"
        latex_content += "\\subsection{模型定义}\n"
        
        try:
            with open(self.model_filepath, 'r', encoding='utf-8') as f:
                model_content = f.read()
            
            # 只显示前50行，避免报告过长
            lines = model_content.split('\n')
            if len(lines) > 50:
                content_to_show = '\n'.join(lines[:50])
                content_to_show += "\n\n# ... (内容截断，完整内容请查看原始文件)"
            else:
                content_to_show = model_content
            
            latex_content += "\\begin{lstlisting}\n"
            latex_content += content_to_show
            latex_content += "\n\\end{lstlisting}\n\n"
            
        except Exception as e:
            latex_content += f"无法读取模型文件内容: {self._escape_latex(str(e))}\n\n"
        
        latex_content += "\\end{document}"
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"已生成求解报告: {output_filepath}")
        return output_filepath
    
    def __del__(self):
        """清理AMPL资源"""
        try:
            if hasattr(self, 'ampl') and self.ampl is not None:
                self.ampl.close()
        except Exception:
            pass

def find_ampl_files(model_input, data_input=None):
    """
    智能查找AMPL文件
    
    参数:
    model_input - 模型文件名或路径
    data_input - 可选的数据文件名或路径
    
    返回:
    (mod_file, dat_file) - 找到的模型文件和数据文件路径
    
    这个函数实现了智能文件查找功能，可以根据用户提供的简略名称，
    在多个可能的目录中定位AMPL模型文件(.mod)和数据文件(.dat)。
    它考虑了多种可能的文件命名和目录结构情况，使用户可以用简单的
    命令行参数就能找到正确的文件，而不需要提供完整路径。
    """
    # 处理模型文件
    model_base_name = model_input.replace('.mod', '').replace('.dat', '')
    
    # 如果用户输入了.dat文件，提取基名并查找对应的.mod文件
    if model_input.endswith('.dat'):
        print(f"检测到数据文件输入: {model_input}")
        print(f"尝试查找对应的模型文件: {model_base_name}.mod")
    
    # 可能的模型文件路径
    possible_mod_paths = [
        model_input if model_input.endswith('.mod') else f"{model_input}.mod",
        f"{model_base_name}.mod",
        os.path.join("ampl", f"{model_base_name}.mod"),
        os.path.join("models", f"{model_base_name}.mod"),
        os.path.join("ampl", model_input) if model_input.endswith('.mod') else None,
        os.path.join("models", model_input) if model_input.endswith('.mod') else None,
    ]
    
    # 处理数据文件
    if data_input:
        # 如果指定了数据文件参数，优先查找该文件
        data_base_name = data_input.replace('.dat', '')
        possible_dat_paths = [
            data_input if data_input.endswith('.dat') else f"{data_input}.dat",
            f"{data_base_name}.dat",
            os.path.join("ampl", f"{data_base_name}.dat"),
            os.path.join("models", f"{data_base_name}.dat"),
            os.path.join("data", f"{data_base_name}.dat"),
            os.path.join("ampl", data_input) if data_input.endswith('.dat') else None,
        ]
    else:
        # 如果没有指定数据文件，查找与模型文件同名的数据文件
        possible_dat_paths = [
            model_input if model_input.endswith('.dat') else f"{model_input}.dat",
            f"{model_base_name}.dat",
            os.path.join("ampl", f"{model_base_name}.dat"),
            os.path.join("models", f"{model_base_name}.dat"),
            os.path.join("data", f"{model_base_name}.dat"),
            os.path.join("ampl", model_input) if model_input.endswith('.dat') else None,
        ]
    
    mod_file = None
    dat_file = None
    
    # 查找模型文件
    print("查找模型文件:")
    for path in possible_mod_paths:
        if path and os.path.exists(path):
            print(f"  找到: {path}")
            mod_file = path
            break
        elif path:
            print(f"  未找到: {path}")
    
    # 查找数据文件（可选）
    print("查找数据文件:")
    for path in possible_dat_paths:
        if path and os.path.exists(path):
            print(f"  找到: {path}")
            dat_file = path
            break
        elif path:
            print(f"  未找到: {path}")
    
    return mod_file, dat_file

def list_ampl_files():
    """
    列出可用的AMPL文件
    
    返回:
    (mod_files, dat_files) - 找到的模型文件列表和数据文件列表
    
    这个函数扫描多个常见目录，查找所有可用的AMPL模型文件(.mod)和数据文件(.dat)，
    帮助用户了解有哪些文件可供使用。这在用户不确定系统中有哪些模型可用时特别有用。
    结果按字母顺序排序，方便查找。
    """
    mod_files = []
    dat_files = []
    search_dirs = [".", "ampl", "models", "data"]
    
    for directory in search_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file) if directory != "." else file
                full_path = os.path.join(directory, file)
                
                if file.endswith('.mod') and os.path.isfile(full_path):
                    mod_files.append(file_path)
                elif file.endswith('.dat') and os.path.isfile(full_path):
                    dat_files.append(file_path)
    
    return sorted(mod_files), sorted(dat_files)

def main():
    """
    主函数 - 程序的入口点
    
    这个函数实现了完整的用户交互流程，包括：
    1. 显示程序介绍和使用说明
    2. 检查命令行参数或提供交互式选择界面
    3. 智能查找所需的文件
    4. 选择适当的求解器
    5. 初始化求解器对象并执行求解
    6. 生成LaTeX报告
    7. 提供后续步骤的指导(如生成PDF的命令)
    
    整个过程设计了完善的错误处理和用户友好的提示，
    即使对于不熟悉AMPL或命令行的用户也能轻松操作。
    """
    print("=" * 60)
    print("AMPL模型求解器与LaTeX报告生成器 (增强版)")
    print("支持智能变量格式化和排序")
    print("=" * 60)
    print("\n交互流程:")
    print("  第一步: 选择模型文件 (.mod)")
    print("  第二步: 选择数据文件 (.dat，可选)")
    print("  第三步: 选择求解器")
    print("=" * 60)
    
    if not AMPL_AVAILABLE:
        print("错误: amplpy库未安装")
        print("请运行: pip install amplpy")
        return
    
    # 显示使用方法
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("\n使用方法:")
        print("  python ampl.py model_name")
        print("  python ampl.py model_name data_file.dat") 
        print("  python ampl.py model.mod data.dat")
        print("  python ampl.py model.mod --data data.dat")
        print("\n示例:")
        print("  python ampl.py mps")
        print("  python ampl.py mps ampl/bgprtr.dat        # 推荐用法")
        print("  python ampl.py ampl/mps.mod ampl/bgprtr.dat")
        print("  python ampl.py mps --data ampl/bgprtr.dat")
        print("\n提示:")
        print("  - 第一个参数是模型文件(.mod)")
        print("  - 第二个参数是数据文件(.dat)，可选")
        print("  - 不提供数据文件时，使用模型中的默认数据")
        return
    
    try:
        # 显示可用文件
        available_mod_files, available_dat_files = list_ampl_files()
        
        if available_mod_files:
            print(f"\n发现 {len(available_mod_files)} 个AMPL模型文件:")
            for i, file in enumerate(available_mod_files[:10], 1):
                try:
                    size = os.path.getsize(file)
                    print(f"  {i}. {file} ({size} 字节)")
                except:
                    print(f"  {i}. {file}")
            if len(available_mod_files) > 10:
                print(f"  ...及其他 {len(available_mod_files) - 10} 个文件")
        else:
            print("\n未找到AMPL模型文件 (.mod)")
        
        if available_dat_files:
            print(f"\n发现 {len(available_dat_files)} 个AMPL数据文件:")
            for i, file in enumerate(available_dat_files[:5], 1):  # 只显示前5个
                try:
                    size = os.path.getsize(file)
                    print(f"  {i}. {file} ({size} 字节)")
                except:
                    print(f"  {i}. {file}")
            if len(available_dat_files) > 5:
                print(f"  ...及其他 {len(available_dat_files) - 5} 个文件")
            print("\n使用特定数据文件的方法:")
            if available_mod_files:
                example_mod = available_mod_files[0].replace('.mod', '').split('/')[-1]
                example_dat = available_dat_files[0]
                print(f"   python {os.path.basename(sys.argv[0])} {example_mod} {example_dat}")
                print(f"   python {os.path.basename(sys.argv[0])} {example_mod} --data {example_dat}")
            print("   或者直接运行程序，按提示逐步选择文件")
        else:
            print("\n提示: 请准备好模型文件(.mod)，数据文件(.dat)可选")
        
        print()
        
        # 检查命令行参数
        if len(sys.argv) > 1:
            filename_input = sys.argv[1]
            specific_data_file = None
            
            # 检查是否有第二个参数作为数据文件
            if len(sys.argv) > 2:
                second_arg = sys.argv[2]
                if second_arg.startswith('--data='):
                    specific_data_file = second_arg.split('=', 1)[1]
                elif second_arg == '--data' and len(sys.argv) > 3:
                    specific_data_file = sys.argv[3]
                else:
                    # 将第二个参数视为数据文件名（不要求文件必须存在）
                    specific_data_file = second_arg
                    print(f"检测到数据文件参数: {specific_data_file}")
            
            print(f"使用命令行参数: {filename_input}")
            if specific_data_file:
                print(f"指定数据文件: {specific_data_file}")
        else:
            # 交互式输入 - 分步进行
            try:
                # 第一步：选择模型文件
                print("\n第一步：选择模型文件")
                print("=" * 40)
                
                if available_mod_files:
                    print("可用的模型文件:")
                    for i, mod_file in enumerate(available_mod_files, 1):
                        base_name = mod_file.replace('.mod', '').split('/')[-1]
                        print(f"  {i}. {mod_file} (输入: {base_name})")
                    print()
                    
                    model_input = input("请选择模型文件 (输入编号或文件名): ").strip()
                    
                    # 处理用户输入
                    if model_input.isdigit() and 1 <= int(model_input) <= len(available_mod_files):
                        filename_input = available_mod_files[int(model_input) - 1]
                        print(f"选择了模型文件: {filename_input}")
                    else:
                        filename_input = model_input
                        print(f"输入的模型文件: {filename_input}")
                else:
                    filename_input = input("请输入AMPL模型文件名: ").strip()
                
                if not filename_input:
                    print("未输入文件名，程序退出。")
                    return
                
                # 第二步：选择数据文件
                print("\n第二步：选择数据文件")
                print("=" * 40)
                
                specific_data_file = None
                
                if available_dat_files:
                    print("可用的数据文件:")
                    for i, dat_file in enumerate(available_dat_files[:15], 1):  # 显示前15个
                        print(f"  {i}. {dat_file}")
                    if len(available_dat_files) > 15:
                        print(f"  ... 及其他 {len(available_dat_files) - 15} 个文件")
                    print("  0. 不使用数据文件 (使用模型中的默认数据)")
                    print()
                    
                    data_input = input("请选择数据文件 (输入编号、文件名，或回车跳过): ").strip()
                    
                    if data_input == "0":
                        print("将使用模型中的默认数据")
                        specific_data_file = None
                    elif data_input.isdigit() and 1 <= int(data_input) <= min(15, len(available_dat_files)):
                        specific_data_file = available_dat_files[int(data_input) - 1]
                        print(f"选择了数据文件: {specific_data_file}")
                    elif data_input:
                        specific_data_file = data_input
                        print(f"输入的数据文件: {specific_data_file}")
                    else:
                        print("未选择数据文件，将使用模型中的默认数据")
                else:
                    data_input = input("请输入数据文件路径 (可选，回车跳过): ").strip()
                    if data_input:
                        specific_data_file = data_input
                        print(f"输入的数据文件: {specific_data_file}")
                    else:
                        print("未指定数据文件，将使用模型中的默认数据")
                        
            except (EOFError, KeyboardInterrupt):
                print("输入被中断，程序退出。")
                return
        
        # 查找文件
        if specific_data_file:
            # 如果指定了数据文件，使用新的查找函数
            mod_file, dat_file = find_ampl_files(filename_input, specific_data_file)
            if dat_file:
                print(f"使用指定的数据文件: {dat_file}")
            else:
                print(f"指定的数据文件不存在: {specific_data_file}")
                print("尝试查找的路径:")
                data_base_name = specific_data_file.replace('.dat', '')
                possible_dat_paths = [
                    specific_data_file if specific_data_file.endswith('.dat') else f"{specific_data_file}.dat",
                    f"{data_base_name}.dat",
                    os.path.join("ampl", f"{data_base_name}.dat"),
                    os.path.join("models", f"{data_base_name}.dat"),
                    os.path.join("data", f"{data_base_name}.dat"),
                ]
                for path in possible_dat_paths:
                    print(f"  - {path}")
        else:
            mod_file, dat_file = find_ampl_files(filename_input)
        
        if mod_file is None:
            print(f"\n模型文件未找到!")
            print(f"输入: '{filename_input}'")
            print("\n提示:")
            print("- AMPL需要模型文件(.mod)作为主文件")
            if filename_input.endswith('.dat'):
                base_name = filename_input.replace('.dat', '').split('/')[-1]
                print(f"- 您输入了数据文件，请尝试: {base_name} 或 {base_name}.mod")
            print("- 检查文件路径是否正确")
            print("- 确保文件扩展名为 .mod")
            
            if available_mod_files:
                print(f"\n可用的模型文件:")
                for file in available_mod_files[:5]:
                    base_name = file.replace('.mod', '').split('/')[-1]
                    print(f"  - {file} (可以输入: {base_name})")
                    
                # 特别检查是否有对应的模型文件
                if filename_input.endswith('.dat'):
                    input_base = filename_input.replace('.dat', '').split('/')[-1]
                    matching_mods = [f for f in available_mod_files if input_base in f]
                    if matching_mods:
                        print(f"\n找到可能匹配的模型文件:")
                        for mod_file in matching_mods:
                            mod_base = mod_file.replace('.mod', '').split('/')[-1]
                            print(f"  ➤ 尝试运行: python {sys.argv[0]} {mod_base}")
                    else:
                        # 如果没有找到匹配的模型文件，但有数据文件，建议使用通用模型
                        if filename_input in [f for f in available_dat_files if available_dat_files]:
                            print(f"\n发现您要使用的数据文件存在，但没有对应的模型文件")
                            print(f"建议尝试使用通用模型文件:")
                            for mod_file in available_mod_files:
                                mod_base = mod_file.replace('.mod', '').split('/')[-1]
                                dat_name = filename_input.split('/')[-1]
                                print(f"  ➤ python {sys.argv[0]} {mod_base} {filename_input}")
                                print(f"     (使用模型 {mod_file} + 数据 {filename_input})")
                                break
                            
            # 如果没有指定数据文件但用户可能想要使用特定数据文件
            if not specific_data_file and available_dat_files:
                print(f"\n如果您想使用特定的数据文件，请运行:")
                example_dat = available_dat_files[0] if available_dat_files else "data.dat"
                print(f"   python {sys.argv[0]} {filename_input} {example_dat}")
                print(f"   python {sys.argv[0]} -h  # 查看更多用法")
            
            return
        
        print(f"\n找到模型文件: {mod_file}")
        if dat_file:
            print(f"找到数据文件: {dat_file}")
        else:
            print("未找到对应的数据文件，将使用模型文件中的默认数据")
        
        # 询问求解器选择
        print("\n第三步：选择求解器")
        print("=" * 40)
        print("常用求解器:")
        print("  • gurobi   - 商业求解器 (高性能)")
        print("  • cplex    - 商业求解器 (IBM)")
        print("  • copt     - 商业求解器 (Cardinal Optimizer)")
        print("  • highs    - 开源求解器 (推荐)")
        print("  • cbc      - 开源求解器")
        print("  • auto     - 自动检测最佳可用求解器")
        print()
        
        solver_choice = input("请选择求解器 (默认auto): ").strip().lower()
        if not solver_choice:
            solver_choice = "auto"
        
        print(f"选择了求解器: {solver_choice}")
        
        print(f"\n开始处理...")
        print("=" * 40)
        print(f"   模型文件: {os.path.basename(mod_file)}")
        if dat_file:
            print(f"   数据文件: {os.path.basename(dat_file)}")
        else:
            print(f"   数据来源: 模型文件中的默认数据")
        print(f"   求解器: {solver_choice}")
        print("=" * 40)
        
        # 创建求解器并求解
        solver = AMPLSolver(mod_file, dat_file)
        success = solver.solve_model(solver=solver_choice)
        
        print("\n正在生成LaTeX报告...")
        report_path = solver.generate_latex_report()
        
        if report_path:
            print("\n" + "=" * 20)
            print("任务完成!")
            print("=" * 20)
            if solver.log_filepath:
                print(f"求解日志: {os.path.abspath(solver.log_filepath)}")
            print(f"LaTeX报告: {os.path.abspath(report_path)}")
            
            report_dir = os.path.dirname(os.path.abspath(report_path))
            report_basename = os.path.basename(report_path)
            print(f"\n生成PDF命令:")
            print(f"   cd \"{report_dir}\" && xelatex \"{report_basename}\"")
            
            print("\n增强功能:")
            print("   • 智能变量名格式化 (零填充)")
            print("   • 逻辑排序 (前缀+下标)")
            print("   • 多维数组支持")
            print("   • 详细解结构分析")
            print("   • 数据文件名区分")
            print("   • 适合学术研究文档")

    except Exception as e:
        print(f"处理过程中发生严重错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()