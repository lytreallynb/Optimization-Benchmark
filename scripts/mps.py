# -*- coding: utf-8 -*-
"""
MPS文件COPT求解器与LaTeX报告生成器 (增强版)

本脚本根据 COPT 6.5.1 及以上版本的官方API进行开发。
主要功能:
- 读取MPS文件并使用COPT求解器求解
- 生成完整的LaTeX格式报告
- 支持自动换行以避免PDF排版问题
- 将求解日志保存到单独的文件中
- 智能查找多个目录下的MPS文件
"""
import coptpy as cp
from coptpy import COPT
import os
import re
import datetime
import sys

class MPSCOPTSolver:
    """
    MPS文件COPT求解器，生成完整且页面友好的LaTeX格式报告。
    """
    def __init__(self, mps_filepath):
        if not os.path.exists(mps_filepath):
            raise FileNotFoundError(f"错误: 文件 '{mps_filepath}' 不存在。")
        self.mps_filepath = mps_filepath
        # 创建环境和模型
        self.env = cp.Envr()
        self.model = self.env.createModel("MPS_Solver")
        self.solve_status = None
        self.objective_value = None
        self.solution = {}
        self.all_vars_cache = None  # 缓存变量列表
        self.log_filepath = None    # 用于存储日志文件路径

    def _escape_latex(self, text):
        """转义 LaTeX 特殊字符"""
        return str(text).replace('\\', r'\textbackslash{}').replace('_', r'\_').replace('%', r'\%').replace('$', r'\$').replace('&', r'\&').replace('#', r'\#').replace('{', r'\{').replace('}', r'\}')

    def _parse_variable_name(self, var_name):
        """将变量名 'VarName123' 转换为 LaTeX 下标格式 'VarName_{123}'"""
        match = re.match(r"([a-zA-Z_]+)(\d+)", var_name)
        if match:
            return f"{self._escape_latex(match.group(1))}_{{{match.group(2)}}}"
        else:
            return self._escape_latex(var_name)

    def _format_expr_to_latex(self, expr, terms_per_line=6):
        """
        将 coptpy.LinExpr 对象格式化为 LaTeX 字符串。
        包含自动换行逻辑以修复排版问题。
        """
        n_terms = expr.size
        if n_terms == 0:
            return "0"
        
        latex_expr = ""
        
        terms = sorted([(expr.getVar(i).Name, expr.getCoeff(i)) for i in range(n_terms)], key=lambda x: x[0])
        
        for i, (var_name, coeff) in enumerate(terms):
            var_name_latex = self._parse_variable_name(var_name)
            
            sign_str = ""
            if i > 0:
                sign_str = " + " if coeff >= 0 else " - "
            elif coeff < 0:
                sign_str = "-"
            
            coeff_val = abs(coeff)
            coeff_str = f"{coeff_val:g}" if coeff_val != 1 else ""
            
            latex_expr += f"{sign_str}{coeff_str}{var_name_latex}"

            if (i + 1) % terms_per_line == 0 and (i + 1) < n_terms:
                latex_expr += " \\\\[0.5ex]\n&\\quad "
        
        return latex_expr.lstrip(" +").strip()

    def _format_objective_function_from_api(self):
        """使用 COPT API 将目标函数格式化为 LaTeX"""
        model = self.model
        sense_text = "\\min" if model.ObjSense == COPT.MINIMIZE else "\\max"
        obj_expr = model.getObjective()
        
        latex_obj = "\\section{目标函数}\n\n"
        
        latex_obj += "\\textbf{完整目标函数:}\n\n"
        latex_obj += "\\allowdisplaybreaks\n{\\small\n\\begin{align}\n"
        latex_obj += f"{sense_text} \\quad Z = &\\; "
        
        full_obj_str = self._format_expr_to_latex(obj_expr, terms_per_line=3)
            
        latex_obj += full_obj_str
        latex_obj += "\\nonumber\n\\end{align}\n}\n\n"
        return latex_obj

    def _format_constraints_from_api(self):
        """使用 COPT API 将约束条件格式化为 LaTeX"""
        model = self.model
        latex_constraints = "\\section{约束条件}\n\n"
        
        all_conss = model.getConstrs()
        if not all_conss:
            return latex_constraints + "模型中没有约束条件。\n\n"

        all_conss = sorted(all_conss, key=lambda c: c.Name)

        equality_constraints = []
        less_constraints = []
        greater_constraints = []
        ranged_constraints = []

        for c in all_conss:
            lb = c.LB
            ub = c.UB
            is_le = ub < COPT.INFINITY
            is_ge = lb > -COPT.INFINITY

            if is_ge and is_le:
                if abs(lb - ub) < 1e-9:
                    equality_constraints.append(c)
                else:
                    ranged_constraints.append(c)
            elif is_le:
                less_constraints.append(c)
            elif is_ge:
                greater_constraints.append(c)

        def format_cons_group(con_list, title, sense_type):
            nonlocal latex_constraints
            if not con_list: return

            latex_constraints += f"\\subsection{{{title} ({len(con_list)}个)}}\n\n"
            latex_constraints += "\\allowdisplaybreaks\n{\\small\\begin{align}\n"
            for i, cons in enumerate(con_list):
                expr = self.model.getRow(cons)
                lhs = self._format_expr_to_latex(expr)
                name = self._escape_latex(cons.Name)
                
                if sense_type == 'eq':
                    rhs = f"{cons.LB:g}"
                    op_latex = "="
                elif sense_type == 'le':
                    rhs = f"{cons.UB:g}"
                    op_latex = "\\leq"
                elif sense_type == 'ge':
                    rhs = f"{cons.LB:g}"
                    op_latex = "\\geq"
                
                latex_constraints += f"{lhs} &{op_latex} {rhs} && \\text{{({name})}} \\\\\n"
                if (i + 1) % 20 == 0: latex_constraints += "\\allowbreak\n"
            latex_constraints += "\\end{align}}\n\n"

        def format_ranged_group(con_list, title):
            nonlocal latex_constraints
            if not con_list: return

            latex_constraints += f"\\subsection{{{title} ({len(con_list)}个)}}\n\n"
            latex_constraints += "\\allowdisplaybreaks\n{\\small\\begin{align}\n"
            for i, cons in enumerate(con_list):
                expr = self.model.getRow(cons)
                lhs = self._format_expr_to_latex(expr)
                name = self._escape_latex(cons.Name)
                lb_str = f"{cons.LB:g}"
                ub_str = f"{cons.UB:g}"
                
                latex_constraints += f"{lb_str} \\leq {lhs} &\\leq {ub_str} && \\text{{({name})}} \\\\\n"
                if (i + 1) % 20 == 0: latex_constraints += "\\allowbreak\n"
            latex_constraints += "\\end{align}}\n\n"

        format_cons_group(equality_constraints, "等式约束", 'eq')
        format_cons_group(less_constraints, "小于等于约束", 'le')
        format_cons_group(greater_constraints, "大于等于约束", 'ge')
        format_ranged_group(ranged_constraints, "范围约束")
        
        return latex_constraints

    def _format_variables_from_api(self):
        """使用 COPT API 将变量定义格式化为 LaTeX"""
        latex_vars = "\\section{变量定义}\n\n"
        
        if self.all_vars_cache is None:
            self.all_vars_cache = sorted(self.model.getVars(), key=lambda v: v.Name)
        
        all_vars = self.all_vars_cache
        
        binary_vars = [v for v in all_vars if v.VType == COPT.BINARY]
        integer_vars = [v for v in all_vars if v.VType == COPT.INTEGER]
        continuous_vars = [v for v in all_vars if v.VType == COPT.CONTINUOUS]

        def format_var_list(vars_list, title, var_type_latex):
            nonlocal latex_vars
            if not vars_list: return
            
            latex_vars += f"\\subsection{{{title} ({len(vars_list)}个)}}\n\n"
            
            display_limit = 100
            sample_vars = vars_list[:display_limit]
            
            formatted_vars = [self._parse_variable_name(var.Name) for var in sample_vars]
            latex_vars += "{\\small $" + "$, $".join(formatted_vars) + "$}\n\n"
            latex_vars += f"变量类型: $v \\in {var_type_latex}$\n\n"
            if len(vars_list) > display_limit:
                latex_vars += f"\\textit{{...及其他 {len(vars_list) - display_limit} 个{title}。}}\n\n"

        format_var_list(binary_vars, "二元变量", "\\{0,1\\}")
        format_var_list(integer_vars, "整数变量", "\\mathbb{Z}")
        
        if continuous_vars:
            latex_vars += f"\\subsection{{连续变量 ({len(continuous_vars)}个)}}\n\n"
            all_non_negative = all(v.LB == 0 and v.UB >= COPT.INFINITY for v in continuous_vars)
            if all_non_negative:
                 latex_vars += "所有连续变量均为非负实数 ($v \\geq 0$)。\n\n"
            else:
                latex_vars += "连续变量具有特定的上下界，详情请查阅模型文件。\n\n"
        
        return latex_vars

    def _format_solution_table(self):
        """格式化求解结果表格"""
        if self.solve_status is None or self.solve_status == COPT.UNSTARTED:
             return "\\section{求解结果}\n\n\\textbf{注意:} 模型尚未求解。\n\n"
        
        latex_solution = "\\section{求解结果}\n\n"
        
        status_mapping = {
            COPT.OPTIMAL: "已得最优解 (Optimal)", COPT.INFEASIBLE: "不可行 (Infeasible)",
            COPT.UNBOUNDED: "无界 (Unbounded)", COPT.INF_OR_UNB: "不可行或无界",
            COPT.NODELIMIT: "达到节点数限制 (Node Limit)", COPT.TIMEOUT: "达到时间限制 (Timeout)",
            COPT.INTERRUPTED: "求解被中断 (Interrupted)",
            COPT.NUMERICAL: "数值问题 (Numerical)", COPT.IMPRECISE: "解不精确 (Imprecise)",
        }
        status_text = status_mapping.get(self.solve_status, f"未知状态码 ({self.solve_status})")
        latex_solution += f"\\subsection{{求解状态}}\n\n求解状态: \\textbf{{{status_text}}}\n\n"

        latex_solution += "\\subsection{目标函数值}\n\n"
        if self.objective_value is not None:
            obj_qualifier = "最优" if self.solve_status == COPT.OPTIMAL else "当前可行"
            latex_solution += f"{obj_qualifier}目标值为: $\\mathbf{{{self.objective_value:.8g}}}$\n\n"
        else:
            latex_solution += "未能获得目标函数值。\n\n"
        
        if self.solution:
            latex_solution += "\\subsection{变量取值}\n\n"
            nonzero_solution = {k: v for k, v in self.solution.items() if abs(v) > 1e-9}
            
            def sort_key(item):
                match = re.search(r'\d+', item[0])
                return int(match.group()) if match else float('inf')

            all_vars_sorted = sorted(nonzero_solution.items(), key=sort_key)
            
            latex_solution += f"共有 {len(self.solution)} 个变量，其中 {len(nonzero_solution)} 个变量的取值非零。\n\n"

            latex_solution += "\\begin{center}\n\\begin{longtable}{cc}\n"
            latex_solution += "\\toprule\n\\textbf{变量名} & \\textbf{取值} \\\\\n\\midrule\n\\endfirsthead\n"
            latex_solution += "\\multicolumn{2}{c}{\\textit{续表}} \\\\\n\\toprule\n\\textbf{变量名} & \\textbf{取值} \\\\\n\\midrule\n\\endhead\n"
            latex_solution += "\\bottomrule\n\\endfoot\n\\bottomrule\n\\endlastfoot\n"
            
            for var_name, var_value in all_vars_sorted:
                formatted_value = f"{var_value:.8g}"
                latex_solution += f"${self._parse_variable_name(var_name)}$ & {formatted_value} \\\\\n"
            
            latex_solution += "\\end{longtable}\n\\end{center}\n\n"
        else:
            latex_solution += "\\subsection{变量取值}\n\n模型无解或未提取到解信息。\n\n"
        
        return latex_solution

    def solve_model(self):
        """求解模型，并以更稳健的方式提取结果"""
        try:
            print("开始读取MPS文件...")
            self.model.read(self.mps_filepath)
            self.all_vars_cache = sorted(self.model.getVars(), key=lambda v: v.Name)
            
            # 设置日志文件
            log_dir = "copt_logs"
            os.makedirs(log_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(self.mps_filepath))[0]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_filepath = os.path.join(log_dir, f"{base_name}_log_{timestamp}.log")
            
            # 将求解过程的日志输出到指定文件
            self.model.setLogFile(self.log_filepath)
            print(f"求解日志将被记录到: {self.log_filepath}")

            print("开始求解模型...")
            self.model.solve()
            
            self.solve_status = self.model.Status
            
            solution_available = self.model.hasmipsol if self.model.IsMIP else self.model.haslpsol

            if solution_available:
                status_str = "已得最优解" if self.solve_status == COPT.OPTIMAL else "找到可行解"
                print(f"模型求解完成: {status_str} (状态码: {self.solve_status})")

                self.objective_value = self.model.ObjVal
                for var in self.all_vars_cache:
                    self.solution[var.Name] = var.X
                print(f"目标值: {self.objective_value:.8g}")
            else:
                status_map = {COPT.INFEASIBLE: "不可行", COPT.UNBOUNDED: "无界"}
                status_str = status_map.get(self.solve_status, f"未知状态 ({self.solve_status})")
                print(f"模型求解失败或无解。状态: {status_str}")
                self.objective_value = None
                self.solution = {}
                
        except Exception as e:
            print(f"求解过程中发生严重错误: {e}")
            self.solve_status = None

    def extract_to_latex(self, output_filepath=None):
        """提取模型信息并生成完整的LaTeX格式报告"""
        if self.model.Cols == 0:
            print("模型尚未读取或读取失败，无法生成报告。")
            return None

        if self.solve_status is None:
            print("模型尚未求解，将仅生成模型结构报告...")
            self.solve_status = COPT.UNSTARTED

        if output_filepath is None:
            tex_reports_dir = "tex_reports"
            os.makedirs(tex_reports_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(self.mps_filepath))[0]
            output_filepath = os.path.join(tex_reports_dir, f"{base_name}_COPT_REPORT.tex")
        
        current_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        model_name = os.path.splitext(os.path.basename(self.mps_filepath))[0]
            
        cols = self.model.Cols
        rows = self.model.Rows
        is_mip = self.model.IsMIP

        if self.all_vars_cache is None:
            self.all_vars_cache = self.model.getVars()
        
        bin_vars = sum(1 for v in self.all_vars_cache if v.VType == COPT.BINARY)
        int_vars = sum(1 for v in self.all_vars_cache if v.VType == COPT.INTEGER)
        
        model_type = "混合整数规划 (MIP)" if is_mip else "线性规划 (LP)"

        latex_content = f"""
\\documentclass[a4paper,10pt]{{article}}
\\usepackage[UTF8]{{ctex}}
\\usepackage{{amsmath, amssymb, longtable, booktabs, geometry, fancyhdr}}
\\geometry{{a4paper, left=1.5cm, right=1.5cm, top=2cm, bottom=2cm}}
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[C]{{数学优化模型求解报告}}
\\fancyfoot[C]{{\\thepage}}
\\allowdisplaybreaks[4]

\\title{{数学优化模型求解报告\\\\{{\\large {self._escape_latex(os.path.basename(self.mps_filepath))}}}}}
\\author{{COPT求解器}}
\\date{{报告生成时间: {current_time}}}

\\begin{{document}}
\\maketitle
\\tableofcontents
\\newpage

\\section{{模型概览}}
\\begin{{itemize}}
    \\item \\textbf{{文件名:}} \\texttt{{{self._escape_latex(os.path.basename(self.mps_filepath))}}}
    \\item \\textbf{{模型名:}} {self._escape_latex(model_name)}
    \\item \\textbf{{变量总数:}} {cols} (二元: {bin_vars}, 整数: {int_vars}, 连续: {cols - bin_vars - int_vars})
    \\item \\textbf{{约束总数:}} {rows}
    \\item \\textbf{{优化方向:}} {'最小化 (Minimize)' if self.model.ObjSense == COPT.MINIMIZE else '最大化 (Maximize)'}
    \\item \\textbf{{模型类型:}} {model_type}
\\end{{itemize}}
"""
        
        latex_content += self._format_objective_function_from_api()
        latex_content += self._format_constraints_from_api()
        latex_content += self._format_variables_from_api()
        latex_content += self._format_solution_table()
        
        latex_content += "\\end{document}"
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"已生成求解报告: {output_filepath}")
        return output_filepath

    def __del__(self):
        """清理COPT环境资源"""
        try:
            if hasattr(self, 'env'):
                self.env.close()
        except Exception:
            pass

def find_mps_file(filename_input):
    """智能查找 MPS 文件 - 支持多个目录"""
    base_name = filename_input.replace('.mps', '')
    possible_paths = [
        filename_input,  # 原始输入路径
        f"{base_name}.mps",  # 当前目录加扩展名
        os.path.join("mps", f"{base_name}.mps"),  # mps目录
        os.path.join("milp", f"{base_name}.mps"),  # milp目录
        os.path.join("mps", filename_input),  # mps目录下的原始路径
        os.path.join("milp", filename_input),  # milp目录下的原始路径
        os.path.join("data", f"{base_name}.mps"),  # data目录
        os.path.join("instances", f"{base_name}.mps"),  # instances目录
    ]
    
    print(f"查找文件: {filename_input}")
    for path in possible_paths:
        if os.path.exists(path):
            print(f"  找到: {path}")
            return path
        else:
            print(f"  未找到: {path}")
    return None

def list_mps_files():
    """列出可用的MPS文件"""
    mps_files = []
    search_dirs = [".", "mps", "milp", "data", "instances"]
    
    for directory in search_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            for file in os.listdir(directory):
                if file.endswith('.mps') and os.path.isfile(os.path.join(directory, file)):
                    if directory == ".":
                        mps_files.append(file)
                    else:
                        mps_files.append(f"{directory}/{file}")
    
    return sorted(mps_files)

def main():
    """主函数"""
    print("=" * 60)
    print("MPS文件COPT求解器与LaTeX报告生成器 (增强版)")
    print("=" * 60)
    
    try:
        # 显示可用文件
        available_files = list_mps_files()
        if available_files:
            print("\n可用的MPS文件:")
            for i, file in enumerate(available_files[:10], 1):  # 只显示前10个
                size = os.path.getsize(file)
                print(f"  {i}. {file} ({size} 字节)")
            if len(available_files) > 10:
                print(f"  ...及其他 {len(available_files) - 10} 个文件")
            print()
        
        # 检查命令行参数
        if len(sys.argv) > 1:
            filename_input = sys.argv[1]
            print(f"使用命令行参数: {filename_input}")
        else:
            # 交互式输入
            try:
                filename_input = input("请输入MPS文件名 (例如: milp/22433.mps 或 22433): ").strip()
                if not filename_input:
                    print("未输入文件名，程序退出。")
                    return
            except (EOFError, KeyboardInterrupt):
                print("输入被中断，程序退出。")
                return
        
        actual_filepath = find_mps_file(filename_input)
        
        if actual_filepath is None:
            print(f"\n文件 '{filename_input}' 未找到。")
            print("请检查文件名和路径，或者查看上面列出的可用文件。")
            return
        
        print(f"\n找到文件: {actual_filepath}")
        
        solver = MPSCOPTSolver(actual_filepath)
        solver.solve_model()
        
        print("\n正在生成LaTeX报告...")
        report_path = solver.extract_to_latex()
        
        if report_path:
            print("\n任务完成!")
            if solver.log_filepath:
                print(f"求解日志位置: {os.path.abspath(solver.log_filepath)}")
            print(f"LaTeX报告位置: {os.path.abspath(report_path)}")
            report_dir = os.path.dirname(os.path.abspath(report_path))
            report_basename = os.path.basename(report_path)
            print(f"如需生成PDF, 请在终端执行: cd \"{report_dir}\" && xelatex \"{report_basename}\"")

    except Exception as e:
        print(f"处理过程中发生严重错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()