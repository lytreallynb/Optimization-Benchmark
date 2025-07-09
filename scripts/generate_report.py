# MPS文件COPT求解器与LaTeX报告生成器
# 导入必要的模块
import coptpy as cp
from coptpy import COPT
import os
import re
import datetime

class MPSCOPTSolver:
    """
    MPS文件COPT求解器，生成完整且页面友好的LaTeX格式报告
    """
    def __init__(self, mps_filepath):
        if not os.path.exists(mps_filepath):
            raise FileNotFoundError(f"错误: 文件 '{mps_filepath}' 不存在。")
        self.mps_filepath = mps_filepath
        self.env = cp.Envr()
        self.model = self.env.createModel("MPS_Solver")
        self.solve_status = None
        self.objective_value = None
        self.solution = {}

    def _escape_latex(self, text):
        """转义 LaTeX 特殊字符"""
        return str(text).replace('_', r'\_').replace('%', r'\%').replace('$', r'\$').replace('&', r'\&')

    def _parse_variable_name(self, var_name):
        """将变量名转换为LaTeX下标格式"""
        match = re.match(r"([a-zA-Z_]+)(\d+)", var_name)
        if match:
            return f"{match.group(1)}_{{{match.group(2)}}}"
        else:
            return var_name

    def _format_objective_function(self, obj_string, sense):
        """格式化目标函数 - 确保数学表达式正确"""
        obj_string = obj_string.strip().replace("Obj:", "").strip()
        terms = re.findall(r'([+\-]?)\s*([\d\.]+)\s+([a-zA-Z0-9_]+)', obj_string)
        
        sense_text = "\\min" if sense.lower() == "minimize" else "\\max"
        
        latex_obj = "\\section{目标函数}\n\n"
        
        # 分离Y变量和X变量，进行实际统计
        y_terms = [t for t in terms if t[2].startswith('Y')]
        x_terms = [t for t in terms if t[2].startswith('X')]
        
        # 只有当确实存在Y和X变量时才显示摘要
        if y_terms and x_terms:
            latex_obj += "\\textbf{目标函数摘要:}\n"
            latex_obj += f"\\begin{{equation}}\n"
            latex_obj += f"{sense_text} \\quad Z = \\sum_{{i}} c_i Y_i + \\sum_{{j}} d_j X_j\n"
            latex_obj += f"\\end{{equation}}\n\n"
            
            # 实际计算的系数统计
            y_coeffs = [float(coeff) for _, coeff, _ in y_terms]
            x_coeffs = [float(coeff) for _, coeff, _ in x_terms]
            
            latex_obj += f"Y变量: {len(y_terms)}个，系数范围 [{min(y_coeffs):g}, {max(y_coeffs):g}] \\\\\n"
            latex_obj += f"X变量: {len(x_terms)}个，系数范围 [{min(x_coeffs):g}, {max(x_coeffs):g}]\n\n"
        elif y_terms:
            # 只有Y变量
            latex_obj += "\\textbf{目标函数摘要:}\n"
            latex_obj += f"\\begin{{equation}}\n"
            latex_obj += f"{sense_text} \\quad Z = \\sum_{{i}} c_i Y_i\n"
            latex_obj += f"\\end{{equation}}\n\n"
            
            y_coeffs = [float(coeff) for _, coeff, _ in y_terms]
            latex_obj += f"Y变量: {len(y_terms)}个，系数范围 [{min(y_coeffs):g}, {max(y_coeffs):g}]\n\n"
        elif x_terms:
            # 只有X变量
            latex_obj += "\\textbf{目标函数摘要:}\n"
            latex_obj += f"\\begin{{equation}}\n"
            latex_obj += f"{sense_text} \\quad Z = \\sum_{{j}} d_j X_j\n"
            latex_obj += f"\\end{{equation}}\n\n"
            
            x_coeffs = [float(coeff) for _, coeff, _ in x_terms]
            latex_obj += f"X变量: {len(x_terms)}个，系数范围 [{min(x_coeffs):g}, {max(x_coeffs):g}]\n\n"
        
        # 完整的目标函数
        latex_obj += "\\textbf{完整目标函数:}\n\n"
        latex_obj += "\\allowdisplaybreaks\n"
        latex_obj += "{\\small\n"
        latex_obj += "\\begin{align}\n"
        latex_obj += f"{sense_text} \\quad Z = &\\; "
        
        # 每行显示3项
        terms_per_line = 3
        
        for i, (sign, coeff, var_name) in enumerate(terms):
            var_latex = self._parse_variable_name(var_name)
            
            if i == 0:
                # 移除第一个元素的加号
                term = f"{'-' if sign == '-' else ''}{coeff} {var_latex}"
            else:
                term = f" {sign if sign else '+'} {coeff} {var_latex}"
            
            latex_obj += term
            
            # 每3项或每30项后允许分页
            if (i + 1) % terms_per_line == 0 and (i + 1) < len(terms):
                if (i + 1) % 30 == 0:  # 每30项后强制允许分页
                    latex_obj += " \\\\[0.5ex]\\allowbreak\n&\\; "
                else:
                    latex_obj += " \\\\[0.3ex]\n&\\; "
        
        latex_obj += "\\nonumber\n\\end{align}\n}\n\n"
        return latex_obj

    def _format_constraints(self, constraints_string):
        """格式化约束条件 - 允许分页"""
        lines = constraints_string.strip().split('\n')
        
        equality_constraints = []
        inequality_constraints = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if '=' in line and '<=' not in line and '>=' not in line:
                equality_constraints.append(line)
            else:
                inequality_constraints.append(line)
        
        latex_constraints = "\\section{约束条件}\n\n"
        
        # 等式约束
        if equality_constraints:
            latex_constraints += f"\\subsection{{等式约束 ({len(equality_constraints)}个)}}\n\n"
            latex_constraints += "\\allowdisplaybreaks\n"
            latex_constraints += "{\\small\n"
            latex_constraints += "\\begin{align}\n"
            
            for i, constraint in enumerate(equality_constraints):
                if ':' in constraint:
                    name, expression = constraint.split(':', 1)
                    name = name.strip()
                    expression = expression.strip()
                else:
                    name = f"C_{i+1}"
                    expression = constraint
                
                if '=' in expression:
                    left, right = expression.split('=')
                    left = left.strip()
                    right = right.strip()
                    
                    # 解析变量项
                    terms = re.findall(r'([+\-]?)\s*(\d*\.?\d*)\s*([a-zA-Z0-9_]+)', left)
                    
                    # 如果变量太多，分多行显示
                    formatted_left = ""
                    for j, (sign, coeff, var_name) in enumerate(terms):
                        var_latex = self._parse_variable_name(var_name)
                        
                        coeff_str = ""
                        if coeff:
                            if float(coeff) == 1:
                                coeff_str = ""
                            elif float(coeff) == -1:
                                coeff_str = "-"
                            else:
                                coeff_str = coeff
                        
                        if j == 0:
                            formatted_left += f"{'-' if sign == '-' else ''}{coeff_str}{var_latex}"
                        else:
                            formatted_left += f" {sign if sign else '+'} {coeff_str}{var_latex}"
                        
                        # 每6个变量换行
                        if (j + 1) % 6 == 0 and (j + 1) < len(terms):
                            formatted_left += " \\\\[0.1ex]\n&\\quad "
                    
                    latex_constraints += f"{formatted_left} &= {right} && \\text{{({self._escape_latex(name)})}} \\\\\n"

                # 每5个约束后插入一个分页点
                if (i + 1) % 5 == 0 and i + 1 < len(equality_constraints):
                    latex_constraints += "\\allowbreak\n"
            
            latex_constraints += "\\end{align}\n}\n\n"
        
        # 不等式约束
        if inequality_constraints:
            latex_constraints += f"\\subsection{{不等式约束 ({len(inequality_constraints)}个)}}\n\n"
            latex_constraints += "\\allowdisplaybreaks\n"
            latex_constraints += "{\\small\n"
            latex_constraints += "\\begin{align}\n"
            
            for i, constraint in enumerate(inequality_constraints):
                if ':' in constraint:
                    name, expression = constraint.split(':', 1)
                    name = name.strip()
                    expression = expression.strip()
                else:
                    name = f"G_{i}"
                    expression = constraint

                formatted_left = ""
                # 公共的左侧格式化逻辑
                def format_lhs(lhs_text):
                    terms = re.findall(r'([+\-]?)\s*(\d*\.?\d*)\s*([a-zA-Z0-9_]+)', lhs_text)
                    lhs_formatted = ""
                    for j, (sign, coeff, var_name) in enumerate(terms):
                        var_latex = self._parse_variable_name(var_name)
                        coeff_str = ""
                        if coeff:
                            if float(coeff) == 1:
                                coeff_str = ""
                            elif float(coeff) == -1:
                                coeff_str = "-"
                            else:
                                coeff_str = coeff

                        if j == 0:
                            lhs_formatted += f"{'-' if sign == '-' else ''}{coeff_str}{var_latex}"
                        else:
                            lhs_formatted += f" {sign if sign else '+'} {coeff_str}{var_latex}"
                    return lhs_formatted

                if '<=' in expression:
                    left, right = expression.split('<=')
                    formatted_left = format_lhs(left.strip())
                    latex_constraints += f"{formatted_left} &\\leq {right.strip()} && \\text{{({self._escape_latex(name)})}} \\\\\n"
                
                elif '>=' in expression:
                    left, right = expression.split('>=')
                    formatted_left = format_lhs(left.strip())
                    latex_constraints += f"{formatted_left} &\\geq {right.strip()} && \\text{{({self._escape_latex(name)})}} \\\\\n"
                
                # 每10个不等式约束后插入分页点
                if (i + 1) % 10 == 0 and i + 1 < len(inequality_constraints):
                    latex_constraints += "\\allowbreak\n"
            
            latex_constraints += "\\end{align}\n}\n\n"
        
        return latex_constraints

    def _format_variables(self, bounds_string, binaries_string):
        """格式化变量信息 - 修复大数据集显示问题"""
        latex_vars = "\\section{变量定义}\n\n"
        
        binary_vars = []
        if binaries_string:
            binary_vars = binaries_string.strip().split()
        
        # 二元变量
        if binary_vars:
            latex_vars += f"\\subsection{{二元变量 ({len(binary_vars)}个)}}\n\n"
            # 尝试找到Y变量的最大索引
            y_indices = [int(re.search(r'\d+', var).group()) for var in binary_vars if var.startswith('Y') and re.search(r'\d+', var)]
            max_y_index = max(y_indices) if y_indices else len(binary_vars) - 1
            
            latex_vars += f"\\begin{{equation}}\n"
            latex_vars += f"Y_i \\in \\{{0,1\\}}, \\quad i \\in \\{{0, 1, 2, \\ldots, {max_y_index}\\}}\n"
            latex_vars += f"\\end{{equation}}\n\n"
            
            # 对于大数据集，只显示前50个变量作为示例
            if len(binary_vars) > 50:
                latex_vars += f"\\textbf{{二元变量示例}} (显示前50个，共{len(binary_vars)}个):\n\n"
                sample_vars = binary_vars[:50]
            else:
                latex_vars += "\\textbf{所有二元变量:}\n\n"
                sample_vars = binary_vars
            
            latex_vars += "{\\small\n"
            formatted_vars = [self._parse_variable_name(var) for var in sample_vars]
            
            # 每行10个变量
            vars_per_line = 10
            for i in range(0, len(formatted_vars), vars_per_line):
                chunk = formatted_vars[i:i + vars_per_line]
                latex_vars += "$" + "$, $".join(chunk) + "$"
                
                if i + vars_per_line < len(formatted_vars):
                    latex_vars += ", \\\\\n"
                else:
                    latex_vars += "\n"
            
            if len(binary_vars) > 50:
                latex_vars += f"\n\\textit{{...还有{len(binary_vars) - 50}个二元变量}}\n"
            
            latex_vars += "}\n\n"
        
        # 连续变量信息
        total_vars = self.model.getAttr('Cols')
        continuous_count = total_vars - len(binary_vars)
        
        if continuous_count > 0:
            latex_vars += f"\\subsection{{连续变量 ({continuous_count}个)}}\n\n"
            # 尝试找到X变量的最大索引 - 使用正确的 COPT API
            all_vars = [var.name for var in self.model.getVars()]
            x_vars = [v for v in all_vars if v.startswith('X')]
            x_indices = [int(re.search(r'\d+', var).group()) for var in x_vars if re.search(r'\d+', var)]
            max_x_index = max(x_indices) if x_indices else continuous_count - 1

            latex_vars += "所有连续变量均为非负实数:\n"
            latex_vars += f"\\begin{{equation}}\n"
            latex_vars += f"X_j \\geq 0, \\quad j \\in \\{{0, 1, 2, \\ldots, {max_x_index}\\}}\n"
            latex_vars += f"\\end{{equation}}\n\n"
            
            latex_vars += f"\\textbf{{连续变量说明:}} 模型包含{continuous_count}个连续决策变量，"
            latex_vars += "所有变量的取值范围均为非负实数域。\n\n"
        
        return latex_vars

    def _format_solution_table(self):
        """格式化求解结果表格"""
        if not self.solution:
            return "\\section{求解结果}\n\n\\textbf{注意:} 模型未求解或求解失败。\n\n"
        
        latex_solution = "\\section{求解结果}\n\n"
        
        # 最优目标值
        latex_solution += "\\subsection{最优目标值}\n\n"
        if self.objective_value is not None:
            latex_solution += f"最优目标值为: $\\mathbf{{{self.objective_value:.6g}}}$\n\n"
        else:
            latex_solution += "最优目标值: 未获得\n\n"
        
        # 求解状态
        latex_solution += "\\subsection{求解状态}\n\n"
        status_mapping = {
            COPT.OPTIMAL: "最优解",
            COPT.INFEASIBLE: "不可行",
            COPT.UNBOUNDED: "无界",
            COPT.INF_OR_UNB: "不可行或无界",
            COPT.NODELIMIT: "节点数限制",
            COPT.TIMEOUT: "时间限制",
            COPT.UNSTARTED: "未开始",
            COPT.INTERRUPTED: "中断"
        }
        status_text = status_mapping.get(self.solve_status, f"未知状态({self.solve_status})")
        latex_solution += f"求解状态: \\textbf{{{status_text}}}\n\n"
        
        # 最优解表格
        if self.solution:
            latex_solution += "\\subsection{最优解}\n\n"
            latex_solution += "各决策变量的最优取值如下：\n\n"
            
            # 分离二元变量和连续变量
            binary_vars = [(k, v) for k, v in self.solution.items() if k.startswith('Y')]
            continuous_vars = [(k, v) for k, v in self.solution.items() if k.startswith('X')]
            
            # 对变量进行排序
            binary_vars.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()) if re.search(r'\d+', x[0]) else 0)
            continuous_vars.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()) if re.search(r'\d+', x[0]) else 0)
            
            # 使用longtable处理大表格
            latex_solution += "\\begin{center}\n"
            latex_solution += "\\begin{longtable}{cc}\n"
            latex_solution += "\\toprule\n"
            latex_solution += "\\textbf{变量名} & \\textbf{最优值} \\\\\n"
            latex_solution += "\\midrule\n"
            latex_solution += "\\endfirsthead\n"
            latex_solution += "\\multicolumn{2}{c}{\\textit{续表}} \\\\\n"
            latex_solution += "\\toprule\n"
            latex_solution += "\\textbf{变量名} & \\textbf{最优值} \\\\\n"
            latex_solution += "\\midrule\n"
            latex_solution += "\\endhead\n"
            latex_solution += "\\bottomrule\n"
            latex_solution += "\\endfoot\n"
            latex_solution += "\\bottomrule\n"
            latex_solution += "\\endlastfoot\n"
            
            # 添加二元变量
            if binary_vars:
                latex_solution += "\\multicolumn{2}{c}{\\textbf{二元变量}} \\\\\n"
                latex_solution += "\\midrule\n"
                for var_name, var_value in binary_vars:
                    var_latex = f"${self._parse_variable_name(var_name)}$"
                    latex_solution += f"{var_latex} & {int(var_value)} \\\\\n"
            
            # 添加连续变量
            if continuous_vars:
                if binary_vars:  # 如果前面有二元变量，添加分隔
                    latex_solution += "\\midrule\n"
                latex_solution += "\\multicolumn{2}{c}{\\textbf{连续变量}} \\\\\n"
                latex_solution += "\\midrule\n"
                for var_name, var_value in continuous_vars:
                    var_latex = f"${self._parse_variable_name(var_name)}$"
                    # 格式化数值，避免科学计数法对于小数
                    if abs(var_value) < 1e-6:
                        formatted_value = "0"
                    elif abs(var_value) < 1000:
                        formatted_value = f"{var_value:.6g}"
                    else:
                        formatted_value = f"{var_value:.3e}"
                    latex_solution += f"{var_latex} & {formatted_value} \\\\\n"
            
            latex_solution += "\\end{longtable}\n"
            latex_solution += "\\end{center}\n\n"
        
        return latex_solution

    def solve_model(self):
        """求解模型"""
        try:
            print("🚀 开始读取MPS文件...")
            self.model.read(self.mps_filepath)
            
            print("⚙️ 开始求解模型...")
            self.model.solve()
            
            # 获取求解状态 - 使用字符串访问属性
            self.solve_status = self.model.status
            
            if self.solve_status == COPT.OPTIMAL:
                print("✅ 模型求解成功，找到最优解")
                # 获取目标值 - 使用简单属性访问
                self.objective_value = self.model.objval
                
                # 获取所有变量的解 - 使用正确的 COPT API
                for var in self.model.getVars():
                    # COPT 中使用 .name 属性获取变量名，getInfo(COPT.Info.Value) 获取解值
                    var_name = var.name
                    var_value = var.getInfo(COPT.Info.Value)
                    self.solution[var_name] = var_value
                
                print(f"📊 最优目标值: {self.objective_value:.6g}")
                print(f"📈 变量数量: {len(self.solution)}")
                
            else:
                print(f"⚠️ 模型求解状态: {self.solve_status}")
                self.objective_value = None
                
        except Exception as e:
            print(f"❌ 求解过程中发生错误: {e}")
            self.solve_status = None
            self.objective_value = None

    def extract_to_latex(self, output_filepath=None):
        """提取MPS文件内容并生成完整且页面友好的LaTeX格式报告"""
        if output_filepath is None:
            # 确保 tex_reports 目录存在
            tex_reports_dir = "tex_reports"
            if not os.path.exists(tex_reports_dir):
                os.makedirs(tex_reports_dir)
                print(f"📁 创建目录: {tex_reports_dir}")
            
            base_name = os.path.splitext(os.path.basename(self.mps_filepath))[0]
            output_filepath = os.path.join(tex_reports_dir, f"{base_name}_COPT_REPORT.tex")
        
        # 生成LP格式以便解析结构
        temp_lp_file = "temp_model.lp"
        self.model.write(temp_lp_file)
        
        with open(temp_lp_file, 'r', encoding='utf-8') as f:
            lp_content = f.read()
        
        # 清理临时文件
        if os.path.exists(temp_lp_file):
            os.remove(temp_lp_file)
        
        # 解析各部分
        obj_match = re.search(r'(Minimize|Maximize)\n(.*?)\nSubject to', lp_content, re.DOTALL | re.IGNORECASE)
        cons_match = re.search(r'Subject to\n(.*?)\n(Bounds|End)', lp_content, re.DOTALL | re.IGNORECASE)
        bounds_match = re.search(r'Bounds\n(.*?)\n(Binaries|Generals|End)', lp_content, re.DOTALL | re.IGNORECASE)
        binaries_match = re.search(r'Binaries\n(.*?)\n(Generals|End)', lp_content, re.DOTALL | re.IGNORECASE)
        
        # 获取当前时间
        current_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        # 生成LaTeX文档
        latex_content = r"""
\documentclass[a4paper,10pt]{article}
\usepackage[UTF8]{ctex}
\usepackage{amsmath}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{a4paper, left=1.5cm, right=1.5cm, top=2cm, bottom=2cm}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{MPS文件数学优化模型求解报告}
\fancyfoot[C]{\thepage}

% 允许数学环境跨页
\allowdisplaybreaks[4]
% 减小数学环境的间距
\setlength{\abovedisplayskip}{6pt}
\setlength{\belowdisplayskip}{6pt}
\setlength{\abovedisplayshortskip}{3pt}
\setlength{\belowdisplayshortskip}{3pt}

\title{数学优化模型求解报告\\{\large """ + self._escape_latex(os.path.basename(self.mps_filepath)) + r"""}}
\author{COPT求解器}
\date{求解时间: """ + current_time + r"""}

\begin{document}
\maketitle
\tableofcontents
\newpage

\section{模型概览}

"""
        
        # 模型基本信息
        latex_content += f"\\textbf{{文件名:}} \\texttt{{{self._escape_latex(os.path.basename(self.mps_filepath))}}} \\\\\n"
        
        # 获取模型名称 - 直接使用字符串访问
        try:
            model_name = self.model.getAttr("ModelName")
        except:
            model_name = "未知模型"
        
        latex_content += f"\\textbf{{模型名:}} {self._escape_latex(model_name)} \\\\\n"
        latex_content += f"\\textbf{{变量总数:}} {self.model.getAttr('Cols')} \\\\\n"
        latex_content += f"\\textbf{{约束总数:}} {self.model.getAttr('Rows')} \\\\\n"
        latex_content += f"\\textbf{{求解时间:}} {current_time} \\\\\n"
        if obj_match:
            latex_content += f"\\textbf{{优化方向:}} {obj_match.group(1)} \\\\\n\n"
        
        # 模型类型判断
        has_binary = binaries_match and binaries_match.group(1).strip()
        has_integer = False  # COPT需要额外检查整数变量
        if has_binary or has_integer:
            latex_content += "\\textbf{模型类型:} 混合整数规划 (MIP)\n\n"
        else:
            latex_content += "\\textbf{模型类型:} 线性规划 (LP)\n\n"
        
        # 目标函数
        if obj_match:
            latex_content += self._format_objective_function(obj_match.group(2), obj_match.group(1))
        
        # 约束条件
        if cons_match:
            latex_content += self._format_constraints(cons_match.group(1))
        
        # 变量定义
        bounds_content = bounds_match.group(1) if bounds_match else ""
        binaries_content = binaries_match.group(1) if binaries_match else ""
        latex_content += self._format_variables(bounds_content, binaries_content)
        
        # 求解结果
        latex_content += self._format_solution_table()
        
        # 求解信息汇总
        latex_content += "\\section{求解信息汇总}\n\n"
        latex_content += f"\\textbf{{求解器:}} COPT \\\\\n"
        latex_content += f"\\textbf{{求解时间:}} {current_time} \\\\\n"
        latex_content += f"\\textbf{{模型规模:}} {self.model.getAttr('Cols')}个变量, {self.model.getAttr('Rows')}个约束 \\\\\n"
        
        if self.solve_status is not None:
            status_mapping = {
                COPT.OPTIMAL: "最优解",
                COPT.INFEASIBLE: "不可行",
                COPT.UNBOUNDED: "无界",
                COPT.INF_OR_UNB: "不可行或无界",
                COPT.NODELIMIT: "节点数限制",
                COPT.TIMEOUT: "时间限制",
                COPT.UNSTARTED: "未开始",
                COPT.INTERRUPTED: "中断"
            }
            status_text = status_mapping.get(self.solve_status, f"未知状态({self.solve_status})")
            latex_content += f"\\textbf{{最终状态:}} {status_text} \\\\\n"
        
        if self.objective_value is not None:
            latex_content += f"\\textbf{{最优目标值:}} {self.objective_value:.6g}\n\n"
        
        latex_content += "\\end{document}"
        
        # 写入文件
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"✅ 已生成完整的求解报告: {output_filepath}")
        print(f"📊 模型规模: {self.model.getAttr('Cols')}个变量, {self.model.getAttr('Rows')}个约束")
        print("📄 包含: 模型结构 + 完整求解结果 + 最优解表格")
        
        return output_filepath

    def __del__(self):
        """清理资源"""
        try:
            if hasattr(self, 'env'):
                self.env.close()
        except:
            pass


def find_mps_file(filename_input):
    """
    智能查找 MPS 文件，支持多种输入格式：
    - 完整路径: mps/bk4x3.mps
    - 相对路径: bk4x3.mps  
    - 仅文件名: bk4x3
    """
    # 可能的路径组合
    possible_paths = []
    
    # 如果用户输入已经包含路径，直接使用
    if '/' in filename_input:
        possible_paths.append(filename_input)
        # 如果没有扩展名，添加 .mps
        if not filename_input.endswith('.mps'):
            possible_paths.append(filename_input + '.mps')
    else:
        # 仅文件名的情况，尝试多种组合
        base_name = filename_input.replace('.mps', '')  # 移除可能的 .mps 扩展名
        
        # 优先在 mps/ 目录中查找
        possible_paths.extend([
            f"mps/{base_name}.mps",
            f"mps/{base_name}",
            f"{base_name}.mps",
            f"{base_name}"
        ])
    
    # 按优先级查找文件
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # 如果都没找到，返回 None
    return None


def main():
    """主函数"""
    print("=" * 60)
    print("🔧 MPS文件COPT求解器与LaTeX报告生成器")
    print("=" * 60)
    
    try:
        # 使用 input() 来接收用户输入
        filename_input = input("请输入MPS文件名 (例如: bk4x3): ").strip()
        
        if not filename_input:
            print("❌ 未输入文件名，程序退出。")
            return
        
        # 智能查找文件
        actual_filepath = find_mps_file(filename_input)
        
        if actual_filepath is None:
            print(f"❌ 文件未找到。尝试了以下路径:")
            # 显示尝试的路径
            if '/' in filename_input:
                possible_paths = [filename_input]
                if not filename_input.endswith('.mps'):
                    possible_paths.append(filename_input + '.mps')
            else:
                base_name = filename_input.replace('.mps', '')
                possible_paths = [
                    f"mps/{base_name}.mps",
                    f"mps/{base_name}",
                    f"{base_name}.mps",
                    f"{base_name}"
                ]
            
            for path in possible_paths:
                print(f"   • {path}")
            print("\n💡 提示: 请确保文件存在于当前目录或 mps/ 目录中")
            return
        
        print(f"🔍 找到文件: {actual_filepath}")
        
        # 创建求解器实例
        solver = MPSCOPTSolver(actual_filepath)
        
        # 求解模型
        solver.solve_model()
        
        # 生成LaTeX报告
        base_name = os.path.splitext(os.path.basename(actual_filepath))[0]
        
        # 确保 tex_reports 目录存在
        tex_reports_dir = "tex_reports"
        if not os.path.exists(tex_reports_dir):
            os.makedirs(tex_reports_dir)
            print(f"📁 创建目录: {tex_reports_dir}")
        
        output_name = os.path.join(tex_reports_dir, f"{base_name}_COPT_REPORT.tex")
        
        print(f"\n📝 生成LaTeX报告...")
        report_path = solver.extract_to_latex(output_name)
        
        print(f"\n✨ 报告生成完成!")
        print(f"📁 文件位置: {report_path}")
        print(f"💡 编译命令: cd {os.path.dirname(os.path.abspath(report_path))} && xelatex {os.path.basename(report_path)}")
        
        # 显示求解摘要
        print(f"\n📈 求解摘要:")
        if solver.solve_status == COPT.OPTIMAL:
            print(f"   ✅ 求解状态: 最优解")
            print(f"   🎯 最优目标值: {solver.objective_value:.6g}")
            print(f"   📊 变量数量: {len(solver.solution)}")
        else:
            print(f"   ⚠️ 求解状态: {solver.solve_status}")
        
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
    except Exception as e:
        print(f"❌ 处理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()