# MPS COPT Solver & LaTeX Report Generator

A comprehensive tool for solving Mathematical Programming System (MPS) files using the COPT solver and generating detailed LaTeX reports with complete solution analysis.

## Features

- **MPS File Processing**: Reads and parses MPS format optimization problems
- **COPT Integration**: Utilizes COPT solver for high-performance optimization
- **LaTeX Report Generation**: Creates publication-ready reports with mathematical formatting
- **Intelligent File Finding**: Supports flexible file path inputs
- **Comprehensive Analysis**: Includes objective function, constraints, variables, and solution details
- **Large Dataset Support**: Handles models with thousands of variables and constraints

## Project Structure

```
.
├── mps/                    # MPS optimization problem files
├── scripts/
│   └── generate_report.py  # Main solver and report generator
├── tex_reports/            # Generated LaTeX reports and PDFs
├── solutions/              # Solution result files
├── lptestset/             # Additional test problems
├── logs/                  # Log files
├── uploads/               # File upload directory
└── work-log/              # Project documentation
```

## Requirements

### Software Dependencies

- **Python 3.7+**
- **COPT Solver**: Commercial optimization solver
- **LaTeX Distribution**: For PDF generation (recommended: TeX Live or MiKTeX)

### Python Packages

```bash
pip install coptpy
```

### LaTeX Packages Required

- `ctex` (for Chinese text support)
- `amsmath` (mathematical expressions)
- `longtable` (large tables)
- `booktabs` (professional tables)
- `geometry` (page layout)
- `fancyhdr` (headers and footers)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Set up Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install coptpy
   ```

3. **Install LaTeX distribution**
   - **Ubuntu/Debian**: `sudo apt-get install texlive-full`
   - **macOS**: Install MacTeX
   - **Windows**: Install MiKTeX or TeX Live

4. **Verify COPT license**
   Ensure you have a valid COPT license configured.

## Usage

### Basic Usage

Run the main script and follow the interactive prompts:

```bash
python scripts/generate_report.py
```

When prompted, enter the MPS file name (supports multiple formats):
- Full path: `mps/bk4x3.mps`
- Relative path: `bk4x3.mps`
- Base name only: `bk4x3`

### Example Session

```
$ python scripts/generate_report.py
============================================================
MPS文件COPT求解器与LaTeX报告生成器
============================================================
请输入MPS文件名 (例如: bk4x3): bk4x3

找到文件: mps/bk4x3.mps
开始读取MPS文件...
开始求解模型...
模型求解成功，找到最优解
最优目标值: 5.230000e+02
变量数量: 15

生成LaTeX报告...
已生成完整的求解报告: tex_reports/bk4x3_COPT_REPORT.tex
模型规模: 15个变量, 6个约束
包含: 模型结构 + 完整求解结果 + 最优解表格

报告生成完成!
文件位置: tex_reports/bk4x3_COPT_REPORT.tex
编译命令: cd tex_reports && xelatex bk4x3_COPT_REPORT.tex
```

### Generating PDF Reports

After generating the LaTeX report, compile it to PDF:

```bash
cd tex_reports
xelatex filename_COPT_REPORT.tex
```

This will generate a comprehensive PDF report containing:
- Model overview and statistics
- Formatted objective function
- Complete constraint listing
- Variable definitions
- Optimal solution table
- Solution summary

## Report Contents

The generated LaTeX reports include:

### 1. Model Overview
- File information and model name
- Problem dimensions (variables, constraints)
- Model type (LP/MIP) classification
- Optimization direction

### 2. Objective Function
- Mathematical formulation with proper subscripts
- Variable coefficient analysis
- Complete term-by-term breakdown

### 3. Constraints
- Equality and inequality constraints
- Proper mathematical formatting
- Named constraint references

### 4. Variable Definitions
- Binary and continuous variable specifications
- Domain definitions
- Variable range summaries

### 5. Solution Results
- Optimal objective value
- Solver status information
- Complete variable solution table
- Solution verification

## Supported File Formats

- **MPS**: Mathematical Programming System format
- **Output**: LaTeX (.tex) and PDF reports

## Example Files

The project includes several test problems in the `mps/` directory:

- `bk4x3.mps`: Small test problem (15 variables, 6 constraints)
- `bal8x12.mps`: Medium-scale problem
- `gr4x6.mps`: Grid-based optimization problem
- `n37xx.mps`: Large-scale numerical test suite
- `ranXxY.mps`: Random problem instances

## Troubleshooting

### Common Issues

1. **COPT License Error**
   - Ensure COPT is properly licensed
   - Check environment variables

2. **LaTeX Compilation Errors**
   - Install missing LaTeX packages
   - Use `xelatex` for Chinese text support

3. **File Not Found**
   - Check file paths and extensions
   - Ensure MPS files are in the `mps/` directory

4. **Memory Issues with Large Models**
   - The tool automatically handles large datasets
   - Reports may take longer for models with 1000+ variables

### File Path Examples

The solver accepts various input formats:
- `bk4x3` → finds `mps/bk4x3.mps`
- `bk4x3.mps` → finds `mps/bk4x3.mps` or `./bk4x3.mps`
- `mps/bk4x3.mps` → uses exact path

## Development

### Code Structure

The main script (`generate_report.py`) contains:

- `MPSCOPTSolver`: Main solver class
- `find_mps_file()`: Intelligent file locator
- LaTeX formatting methods for different report sections
- Error handling and resource cleanup

### Extending the Tool

To add new features:
1. Modify the `MPSCOPTSolver` class
2. Add new formatting methods for additional report sections
3. Update the LaTeX template as needed

## License

This project uses the COPT solver, which requires a commercial license. Please ensure compliance with COPT licensing terms.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with sample MPS files
5. Submit a pull request

## Support

For issues related to:
- **COPT Solver**: Contact COPT support
- **LaTeX**: Check LaTeX documentation
- **This Tool**: Create an issue in the repository