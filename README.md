# Mathematical Programming Solvers with COPT

This project provides two Python scripts for solving mathematical optimization problems using the COPT (Cardinal Optimizer) solver and generating detailed LaTeX reports.

## 🔧 Features

### Common Features
- Automatically reads and parses mathematical programming files
- Uses the COPT solver for optimization
- Generates comprehensive LaTeX reports with:
  - Problem overview and statistics
  - Mathematical model formulation
  - Objective function with proper LaTeX formatting
  - Detailed constraint listings
  - Variable definitions and bounds
  - Optimal solutions and solver status
  - Automatic line breaking for large formulas
- Intelligent file discovery across multiple directories
- Comprehensive error handling and logging
- Command-line interface with interactive prompts
- Bilingual support (Chinese/English)

### MPS Solver (`mps.py`)
- Handles Linear Programming (LP) and Mixed-Integer Programming (MIP) problems
- Supports binary, integer, and continuous variables
- Processes standard MPS format files
- Categorizes constraints by type (equality, inequality, ranged)

### QPS Solver (`qps.py`)
- Handles Quadratic Programming (QP) problems
- Parses QPS format files with quadratic objective functions
- Supports quadratic terms in objective function
- Analyzes quadratic matrix properties (diagonal/off-diagonal terms)

## 📁 Project Structure

```
project/
├── mps/                     # MPS files directory
├── qps/                     # QPS files directory  
├── milp/                    # Alternative MPS files directory
├── data/                    # Data files directory
├── instances/               # Problem instances directory
├── tex_reports/             # LaTeX reports output (MPS)
├── qps_reports/             # LaTeX reports output (QPS)
├── copt_logs/               # Solver logs directory
├── mps.py                   # MPS solver script
├── qps.py                   # QPS solver script
└── README.md                # This file
```

## 🚀 Usage

### Prerequisites

Ensure you have Python 3.7+ and the COPT Python API installed:

```bash
pip install coptpy numpy
```

### MPS File Solver

#### Interactive Mode
```bash
python mps.py
```

#### Command Line Mode
```bash
python mps.py filename.mps
# or
python mps.py milp/problem_name
```

The script will:
- Search for the file in multiple directories (`./`, `mps/`, `milp/`, `data/`, `instances/`)
- Load and solve the optimization problem
- Generate a LaTeX report: `tex_reports/{filename}_COPT_REPORT.tex`
- Save solver logs: `copt_logs/{filename}_log_{timestamp}.log`

### QPS File Solver

#### Interactive Mode
```bash
python qps.py
```

#### Command Line Mode
```bash
python qps.py filename.qps
# or
python qps.py qps/problem_name
```

The script will:
- Search for the file in multiple directories
- Parse the QPS format including quadratic terms
- Generate a LaTeX report: `qps_reports/{filename}_QPS_REPORT.tex`
- Save solver logs: `copt_logs/{filename}_qps_log_{timestamp}.log`

### Compile LaTeX Reports

Generate PDF from the LaTeX reports:

```bash
# For MPS reports
cd tex_reports/
xelatex filename_COPT_REPORT.tex

# For QPS reports  
cd qps_reports/
xelatex filename_QPS_REPORT.tex
```

## 📊 Report Contents

### MPS Reports Include:
- **Model Overview**: Variables, constraints, problem type (LP/MIP)
- **Objective Function**: Complete mathematical formulation
- **Constraints**: Categorized by type (equality, ≤, ≥, ranged)
- **Variable Definitions**: Binary, integer, and continuous variables
- **Solution Results**: Optimal values, solver status, solution table

### QPS Reports Include:
- **Problem Information**: Quadratic programming specifics
- **Mathematical Model**: Objective with linear and quadratic terms
- **Quadratic Matrix Analysis**: Diagonal/off-diagonal term statistics
- **Constraint Analysis**: Detailed constraint breakdowns
- **Variable Bounds**: Comprehensive boundary information
- **Solution Analysis**: Statistical analysis of optimal solution

## 🎯 File Format Support

### MPS Format
- Standard Mathematical Programming System format
- Supports LP and MIP problems
- Handles various constraint types and variable bounds

### QPS Format  
- Quadratic Programming System format extension
- Includes `QUADOBJ` section for quadratic objective terms
- Supports all standard MPS sections plus quadratic extensions

## ⚙️ Solver Configuration

Both scripts automatically configure COPT with optimized settings:
- Dual simplex method for linear problems
- High precision tolerances (1e-9)
- Comprehensive logging
- Automatic problem type detection

## 📦 Dependencies

- **Python 3.7+**
- **coptpy**: COPT Python API
- **numpy**: Numerical computations (QPS solver)
- **LaTeX environment**: For PDF compilation (XeLaTeX recommended)

## ⚠️ Notes

- **Performance**: Large models may require significant solve time (1+ hours)
- **Memory**: QPS solver uses efficient parsing for large quadratic problems  
- **Logs**: All solver output is captured in timestamped log files
- **File Discovery**: Scripts automatically search multiple common directories
- **Error Handling**: Robust error handling with detailed feedback

## 🔍 Troubleshooting

### Common Issues:
1. **File Not Found**: Check file paths and ensure files are in supported directories
2. **COPT License**: Ensure valid COPT license is available
3. **Memory Issues**: For very large problems, consider using a server environment
4. **LaTeX Compilation**: Install XeLaTeX for proper Chinese character support

### Debug Information:
- Check generated log files in `copt_logs/` directory
- Review solver status messages in console output
- Verify file format compliance for parsing issues

## 📄 License

This project is for academic and research use only. Please refer to COPT licensing terms for commercial usage.

---

**Note**: Both solvers are designed to handle production-scale optimization problems while generating publication-ready mathematical documentation.