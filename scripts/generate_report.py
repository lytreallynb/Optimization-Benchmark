# -*- coding: utf-8 -*-
"""
MPS文件COPT求解器与LaTeX报告生成器 (API最终修正版)
本脚本根据 COPT 6.5.1 及以上版本的官方API进行了重构和修正。
主要变更:
- 放弃读写.lp文件，直接使用 coptpy API 获取模型信息。
- 优化求解结果提取逻辑，确保在找到可行解但未达最优时也能生成报告。
- [最终修正] 修复了获取模型统计信息的方式，使用正确的直接属性(如 model.Cols, model.Rows)
  和迭代计数，替代了错误的 getAttr 调用。
- [最终修正] 修复了获取模型名称的方式，使用文件名作为模型名，避免无效的API调用。
- [最终修正] 修复了 LinExpr.size 的调用方式，其为属性而非方法。
- [最终修正] 修复了 LinExpr.copy 的调用方式，该方法不存在且非必要。
- [最终修正] 修复了 getConss 的调用方式，正确方法为 getConstrs。
- [最终修正] 修复了 Constraint.Sense/Expr 的调用方式，改用更稳健的LB/UB属性和model.getRow()方法。
- [最终修正] 移除了不存在的 COPT.USERINTERRUPT 状态枚举。
"""
import coptpy as cp
from coptpy import COPT
import os
import re
import datetime

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
        self.all_vars_cache = None # 缓存变量列表

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

    def _format_expr_to_latex(self, expr):
        """将 coptpy.LinExpr 对象格式化为 LaTeX 字符串"""
        # .size 是一个属性，不是方法
        n_terms = expr.size
        if n_terms == 0:
            return "0"
        
        latex_expr = ""
        
        # 按变量名排序以获得确定性输出
        # LinExpr 没有 .copy() 方法，且此处为只读操作，无需复制。
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
        
        return latex_expr.lstrip(" +").strip()

    def _format_objective_function_from_api(self):
        """使用 COPT API 将目标函数格式化为 LaTeX"""
        model = self.model
        sense_text = "\\min" if model.ObjSense == COPT.MINIMIZE else "\\max"
        obj_expr = model.getObjective()
        
        latex_obj = "\\section{目标函数}\n\n"
        
        # 完整目标函数
        latex_obj += "\\textbf{完整目标函数:}\n\n"
        latex_obj += "\\allowdisplaybreaks\n{\\small\n\\begin{align}\n"
        latex_obj += f"{sense_text} \\quad Z = &\\; "
        
        full_obj_str = self._format_expr_to_latex(obj_expr)
        
        # 美化长公式断行
        display_terms = re.split(r'\s*([+\-])\s*', full_obj_str)
        if display_terms and display_terms[0] == '': display_terms.pop(0)

        output_terms = []
        # 第一个项可能没有前导符号
        if display_terms and display_terms[0] not in '+-':
            output_terms.append(display_terms.pop(0))

        # 剩下的项都是 符号-数值 对
        for i in range(0, len(display_terms), 2):
            if i + 1 < len(display_terms):
                output_terms.append(f"{display_terms[i]} {display_terms[i+1]}")
            else:
                output_terms.append(display_terms[i])

        terms_per_line = 3
        for i, term in enumerate(output_terms):
            latex_obj += term
            if (i + 1) % terms_per_line == 0 and (i + 1) < len(output_terms):
                latex_obj += " \\\\[0.5ex]\n&\\; "
            elif i < len(output_terms) - 1:
                latex_obj += " "
            
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

        # 不再使用 .Sense 属性，改用 LB/UB 判断，更稳健
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
                if abs(lb - ub) < 1e-9: # 浮点数比较
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
                # 使用 model.getRow(cons) 获取表达式，而不是 cons.Expr
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
        
        # --- API 调用最终修正 ---
        # 移除了不存在的 COPT.USERINTERRUPT 属性
        status_mapping = {
            COPT.OPTIMAL: "已得最优解 (Optimal)", COPT.INFEASIBLE: "不可行 (Infeasible)",
            COPT.UNBOUNDED: "无界 (Unbounded)", COPT.INF_OR_UNB: "不可行或无界",
            COPT.NODELIMIT: "达到节点数限制 (Node Limit)", COPT.TIMEOUT: "达到时间限制 (Timeout)",
            COPT.INTERRUPTED: "求解被中断 (Interrupted)",
            COPT.NUMERICAL: "数值问题 (Numerical)", COPT.IMPRECISE: "解不精确 (Imprecise)",
        }
        # --------------------
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
            print("🚀 开始读取MPS文件...")
            self.model.read(self.mps_filepath)
            self.all_vars_cache = sorted(self.model.getVars(), key=lambda v: v.Name) # 读取后缓存变量
            
            print("⚙️ 开始求解模型...")
            self.model.solve()
            
            self.solve_status = self.model.Status
            
            solution_available = self.model.hasmipsol if self.model.IsMIP else self.model.haslpsol

            if solution_available:
                status_str = "已得最优解" if self.solve_status == COPT.OPTIMAL else "找到可行解"
                print(f"✅ 模型求解完成: {status_str} (状态码: {self.solve_status})")

                self.objective_value = self.model.ObjVal
                for var in self.all_vars_cache:
                    self.solution[var.Name] = var.X
                print(f"📊 目标值: {self.objective_value:.8g}")
            else:
                status_map = {COPT.INFEASIBLE: "不可行", COPT.UNBOUNDED: "无界"}
                status_str = status_map.get(self.solve_status, f"未知状态 ({self.solve_status})")
                print(f"❌ 模型求解失败或无解。状态: {status_str}")
                self.objective_value = None
                self.solution = {}
                
        except Exception as e:
            print(f"❌ 求解过程中发生严重错误: {e}")
            self.solve_status = None

    def extract_to_latex(self, output_filepath=None):
        """提取模型信息并生成完整的LaTeX格式报告 (API已最终修正)"""
        if self.model.Cols == 0:
            print("❗️ 模型尚未读取或读取失败，无法生成报告。")
            return None

        if self.solve_status is None:
            print("🤔 模型尚未求解，将仅生成模型结构报告...")
            self.solve_status = COPT.UNSTARTED

        if output_filepath is None:
            tex_reports_dir = "tex_reports"
            os.makedirs(tex_reports_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(self.mps_filepath))[0]
            output_filepath = os.path.join(tex_reports_dir, f"{base_name}_COPT_REPORT.tex")
        
        current_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        # model.Name 不是一个有效的属性。我们使用文件名作为模型名。
        model_name = os.path.splitext(os.path.basename(self.mps_filepath))[0]
            
        # 使用正确的直接属性和迭代计数
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
        
        print(f"✅ 已生成基于API的求解报告: {output_filepath}")
        return output_filepath

    def __del__(self):
        """清理COPT环境资源"""
        try:
            if hasattr(self, 'env'):
                self.env.close()
        except Exception:
            pass

def find_mps_file(filename_input):
    """智能查找 MPS 文件"""
    base_name = filename_input.replace('.mps', '')
    possible_paths = [
        filename_input,
        f"{base_name}.mps",
        os.path.join("mps", f"{base_name}.mps"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 MPS文件COPT求解器与LaTeX报告生成器 (API最终修正版)")
    print("=" * 60)
    
    try:
        filename_input = input("请输入MPS文件名 (例如: mps/ran12x12.mps 或 ran12x12): ").strip()
        if not filename_input:
            print("❌ 未输入文件名，程序退出。")
            return
        
        actual_filepath = find_mps_file(filename_input)
        
        if actual_filepath is None:
            print(f"❌ 文件 '{filename_input}' 未找到。请检查文件名和路径。")
            return
        
        print(f"🔍 找到文件: {actual_filepath}")
        
        solver = MPSCOPTSolver(actual_filepath)
        solver.solve_model()
        
        print(f"\n📝 正在生成LaTeX报告...")
        report_path = solver.extract_to_latex()
        
        if report_path:
            print(f"\n✨ 报告生成完成!")
            print(f"📁 文件位置: {os.path.abspath(report_path)}")
            report_dir = os.path.dirname(os.path.abspath(report_path))
            report_basename = os.path.basename(report_path)
            print(f"💡 如需生成PDF, 请在终端执行: cd \"{report_dir}\" && xelatex \"{report_basename}\"")
        
    except Exception as e:
        print(f"❌ 处理过程中发生严重错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
