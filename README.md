MPS to LaTeX Report Generator with COPT Solver
A robust and efficient tool for solving optimization problems from Mathematical Programming System (MPS) files using the COPT solver. It generates comprehensive, publication-ready reports in LaTeX format, detailing the model structure and solution analysis.

This version has been completely refactored to use the native coptpy Python API directly, ensuring maximum accuracy, performance, and stability by avoiding intermediate file parsing.

Key Features
Direct COPT API Integration: Parses MPS files and builds the model structure using native coptpy objects and methods (model.getVars, model.getConstrs, model.getRow, etc.) for enhanced reliability.
High-Performance Solving: Leverages the powerful COPT engine to solve Linear Programming (LP) and Mixed-Integer Programming (MIP) problems.
Professional LaTeX Reports: Automatically generates detailed .tex reports with properly formatted mathematical equations for the objective function, constraints, and variables.
Robust Solution Handling: Correctly captures and reports feasible solutions, even when the solver terminates before reaching optimality (e.g., due to time limits).
Intelligent File Finder: Locates MPS files with flexible path inputs (e.g., problem.mps, mps/problem.mps, or just problem).
Comprehensive Analysis: The generated report includes a model overview, full objective and constraint listings, variable definitions, and a detailed solution table.
Project Structure
.
├── mps/                    # Directory for MPS input files
├── scripts/
│   └── generate_report.py  # The main solver and report generator script
└── tex_reports/            # Directory for generated LaTeX (.tex) reports

Requirements
Software
Python 3.7+
COPT Solver: A valid and licensed installation of the Cardinal Optimizer.
LaTeX Distribution: Required for compiling the .tex report into a PDF. Recommended: TeX Live, MiKTeX, or MacTeX.
Python Packages
The only required Python package is coptpy, which is included with the COPT solver. If you need to install it separately:

pip install coptpy

LaTeX Packages
The generated .tex files rely on the following standard packages, which are included in most LaTeX distributions:
ctex (for Chinese text support)
amsmath, amssymb
longtable, booktabs
geometry, fancyhdr
How to Use
Running the Script
Navigate to the project's root directory.
Run the script from your terminal:
python scripts/generate_report.py

When prompted, enter the name of the MPS file you wish to solve. The script will automatically search for it.
Example Session
$ python scripts/generate_report.py
============================================================
🔧 MPS文件COPT求解器与LaTeX报告生成器 (API最终修正版)
============================================================
请输入MPS文件名 (例如: mps/ran12x12.mps 或 ran12x12): ran12x12

🔍 找到文件: mps/ran12x12.mps
🚀 开始读取MPS文件...
⚙️ 开始求解模型...
✅ 模型求解完成: 已得最优解 (状态码: 1)
📊 目标值: 1131.5

📝 正在生成LaTeX报告...
✅ 已生成基于API的求解报告: tex_reports/ran12x12_COPT_REPORT.tex

✨ 报告生成完成!
📁 文件位置: /path/to/your/project/tex_reports/ran12x12_COPT_REPORT.tex
💡 如需生成PDF, 请在终端执行: cd "tex_reports" && xelatex "ran12x12_COPT_REPORT.tex"

Generating a PDF Report
After the script generates the .tex file, navigate to the tex_reports directory and compile it using xelatex:

cd tex_reports
xelatex your_model_name_COPT_REPORT.tex

This command creates a polished PDF document ready for review or publication.

Development Insights
Code Structure
The generate_report.py script is built around the MPSCOPTSolver class, which encapsulates the entire workflow.

Key API Usage (The Right Way)
After extensive testing, the script now uses the following robust patterns to interact with the coptpy API, which is crucial for stability:
Model Statistics: Accessed via direct properties.
model.Cols: Get the number of variables.
model.Rows: Get the number of constraints.
model.IsMIP: Check if the model is a Mixed-Integer Program.
Model Components: Accessed via specific methods.
model.getVars(): Get a list of all variable objects.
model.getConstrs(): Get a list of all constraint objects.
model.getObjective(): Get the objective function as a LinExpr object.
model.getRow(constraint): Get the linear expression of a specific constraint row.
Object Properties: Information is read from object properties, not methods with the same name.
LinExpr.size: Get the number of terms in an expression.
Constraint.LB, Constraint.UB: Get the lower/upper bounds to determine the constraint type (e.g., equality, inequality, ranged).
This API-first approach avoids the pitfalls of parsing intermediate files or using unstable internal attributes.

Troubleshooting
COPT License Error: Ensure your COPT license is active and properly configured in your environment.
LaTeX Compilation Fails: Make sure you have a full LaTeX distribution installed. If you encounter errors about missing fonts or packages, use your distribution's package manager to install them.
File Not Found: Place your .mps files inside the mps/ directory or provide a correct relative/absolute path.
