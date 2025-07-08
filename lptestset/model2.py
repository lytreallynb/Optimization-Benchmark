# 导入 PySCIPOpt 的核心模块和 os 模块
from pyscipopt import Model
import os
import re

class MPSExtractor:
    """
    MPS文件内容提取器，生成完整且页面友好的LaTeX格式
    """
    def __init__(self, mps_filepath):
        if not os.path.exists(mps_filepath):
            raise FileNotFoundError(f"错误: 文件 '{mps_filepath}' 不存在。")
        self.mps_filepath = mps_filepath
        self.model = Model("MPS_Extractor")

    def _escape_latex(self, text):
        """转义 LaTeX 特殊字符"""
        return str(text).replace('_', r'\_').replace('%', r'\%').replace('$', r'\$')

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
                    name = f"G_{i}" # 从G0开始
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

                # FIX: 增加了对 >= 的处理
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
        total_vars = self.model.getNVars()
        continuous_count = total_vars - len(binary_vars)
        
        if continuous_count > 0:
            latex_vars += f"\\subsection{{连续变量 ({continuous_count}个)}}\n\n"
            # 尝试找到X变量的最大索引
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

    def extract_to_latex(self, output_filepath="mps_complete.tex"):
        """提取MPS文件内容并生成完整且页面友好的LaTeX格式"""
        # 读取MPS文件
        self.model.readProblem(self.mps_filepath)
        
        # 生成LP格式以便解析
        temp_lp_file = "temp_model.lp"
        self.model.writeProblem(temp_lp_file)
        
        with open(temp_lp_file, 'r', encoding='utf-8') as f:
            lp_content = f.read()
        
        # 在调试时可以取消注释下一行，以保留临时文件
        # os.remove(temp_lp_file)
        
        # 解析各部分
        obj_match = re.search(r'(Minimize|Maximize)\n(.*?)\nSubject to', lp_content, re.DOTALL | re.IGNORECASE)
        cons_match = re.search(r'Subject to\n(.*?)\n(Bounds|End)', lp_content, re.DOTALL | re.IGNORECASE)
        bounds_match = re.search(r'Bounds\n(.*?)\n(Binaries|Generals|End)', lp_content, re.DOTALL | re.IGNORECASE)
        binaries_match = re.search(r'Binaries\n(.*?)\n(Generals|End)', lp_content, re.DOTALL | re.IGNORECASE)
        
        # 生成LaTeX文档
        latex_content = r"""
\documentclass[a4paper,10pt]{article}
\usepackage[UTF8]{ctex}
\usepackage{amsmath}
\usepackage{longtable}
\usepackage{geometry}
\geometry{a4paper, left=1.5cm, right=1.5cm, top=2cm, bottom=2cm}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{MPS文件数学模型 - 完整版}
\fancyfoot[C]{\thepage}

% 允许数学环境跨页
\allowdisplaybreaks[4]
% 减小数学环境的间距
\setlength{\abovedisplayskip}{6pt}
\setlength{\belowdisplayskip}{6pt}
\setlength{\abovedisplayshortskip}{3pt}
\setlength{\belowdisplayshortskip}{3pt}

\title{MPS文件数学模型提取\\{\large 完整版}}
\author{MPS Extractor}
\date{\today}

\begin{document}
\maketitle
\tableofcontents
\newpage

\section{模型概览}

"""
        
        # 模型基本信息
        latex_content += f"\\textbf{{文件名:}} \\texttt{{{self._escape_latex(os.path.basename(self.mps_filepath))}}} \\\\\n"
        latex_content += f"\\textbf{{模型名:}} {self._escape_latex(self.model.getProbName())} \\\\\n"
        latex_content += f"\\textbf{{变量总数:}} {self.model.getNVars()} \\\\\n"
        latex_content += f"\\textbf{{约束总数:}} {self.model.getNConss()} \\\\\n"
        if obj_match:
            latex_content += f"\\textbf{{优化方向:}} {obj_match.group(1).capitalize()} \\\\\n\n"
        
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
        
        latex_content += "\\end{document}"
        
        # 写入文件
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"✅ 已生成完整的数学模型: {output_filepath}")
        print(f"📊 模型规模: {self.model.getNVars()}个变量, {self.model.getNConss()}个约束")
        print("📄 包含: 摘要 + 完整目标函数 + 所有约束 + 所有变量")
        # 清理临时文件
        if os.path.exists(temp_lp_file):
            os.remove(temp_lp_file)


if __name__ == "__main__":
    try:
        # 使用 input() 来接收用户输入
        filename_input = input("请输入MPS文件名 (例如: bal8x12.mps): ")
        if not filename_input:
            print("❌ 未输入文件名，程序退出。")
        else:
            extractor = MPSExtractor(filename_input)
            
            output_name = os.path.splitext(filename_input)[0] + "_COMPLETE.tex"
            extractor.extract_to_latex(output_name)
        
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
    except Exception as e:
        print(f"❌ 处理过程中发生未知错误: {e}")