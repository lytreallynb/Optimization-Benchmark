# MPS 模型求解与变量导出工具

## 📌 项目简介

本项目支持批量求解 `.mps` 数学优化模型，导出最优变量值为 Excel 表格（`.xlsx`），并生成 LaTeX 模型文档。

## 📂 文件结构

- `mps/`：原始 .mps 文件（模型）
- `solutions/`：求解结果（.xlsx）
- `tex/`：模型结构 LaTeX 文件
- `logs/`：求解日志和输出记录
- `scripts/`：所有 Python 求解脚本

## 🚀 使用方法

### 1. 求解单个模型

```bash
cd scripts
python solution.py 文件名.mps
```

### 2. 批量求解所有模型

```bash
cd scripts
python batch_solver.py
```

### 3. 生成 LaTeX 表达式（选做）

```bash
python model2.py
```

## 🔧 依赖安装

```bash
pip install pyscipopt pandas openpyxl
```

## 📌 作者

内部使用工具，适合科研、教学或求解大规模线性优化模型。