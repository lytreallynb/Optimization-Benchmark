# MPS Model Report Generator with COPT

This Python script reads `.mps` (Mathematical Programming System) files, solves them using the COPT (Cardinal Optimizer) solver, and generates a structured LaTeX report with detailed information about the optimization model.

## 🔧 Features

- Automatically reads and parses `.mps` files.
- Uses the COPT solver to extract model details.
- Outputs a well-structured LaTeX report including:
  - File overview
  - Model summary
  - Objective function
  - Constraints
  - Variable definitions
  - Optimal objective value and decision variable results
- Easy command-line interaction
- Handles large instances (solver optimization may take ~1h+ depending on the file)

## 📁 Project Structure

```
project/
├── mps/                  # Folder containing your .mps files
├── reports/              # Output directory for LaTeX reports
├── scripts/
│   └── generate_report.py  # Main Python script
```

## 🚀 Usage

### 1. Setup

Ensure you have Python and the COPT Python API installed. Activate your virtual environment if needed.

```bash
pip install coptpy
```

### 2. Run the script

```bash
python generate_report.py
```

You will be prompted to input the MPS file name (without extension). Example:

```bash
Please enter the MPS file name (e.g., ran12x12): ran12x12
```

The script will:

- Load the file `mps/ran12x12.mps`
- Use COPT to analyze the model
- Generate a LaTeX file: `reports/ran12x12_report.tex`

### 3. Compile LaTeX

You can compile the generated `.tex` file using `pdflatex` or any LaTeX editor (e.g., Overleaf, TeXworks):

```bash
cd reports/
pdflatex ran12x12_report.tex
```

## 📦 Dependencies

- Python 3.7+
- [COPT Python API (coptpy)](https://guide.coap.online/copt/zh-doc/pythoninterface.html)
- LaTeX environment (for compiling the report)

## ⚠️ Notes

- Some attributes (like `NumVars`) may raise errors if not available in the COPT API; make sure to use valid attribute names from [COPT documentation](https://guide.coap.online/copt/zh-doc/pythoninterface.html).
- Large models may require significant compute time; consider running on a server if solving exceeds 1 hour.

## 📄 License

This project is for academic and research use only.

---

Feel free to modify the script to adjust formatting, add visualizations, or support other file formats.
