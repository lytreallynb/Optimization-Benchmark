# 数学规划模型求解与报告生成系统

## 项目概述

本项目是一个专业的数学规划模型求解与LaTeX报告生成系统，旨在为研究人员和优化从业者提供高质量的模型分析工具。系统支持多种格式的数学规划问题（AMPL、MPS、QPS），并能使用不同的求解器（Gurobi、COPT等）进行求解，最终生成结构化的LaTeX报告。

项目特点：
- 支持多种格式的数学规划模型
- 集成多种商业和开源求解器
- 智能变量格式化和排序功能
- 专业LaTeX报告自动生成
- 易于使用的命令行界面

## 代码结构

项目包含以下核心脚本：

### 1. ampl.py
- 功能：处理AMPL格式的模型（.mod）和数据（.dat）文件
- 特点：可自动检测并使用多种求解器（Gurobi、CPLEX、COPT、HiGHS等）
- 报告：生成包含模型摘要、求解结果和变量值的LaTeX报告

### 2. mps.py
- 功能：处理MPS格式的模型文件，使用COPT求解器
- 特点：支持智能变量格式化和排序，提高报告可读性
- 报告：生成包含模型结构、约束条件和求解结果的LaTeX报告

### 3. mps_gurobi.py
- 功能：处理MPS格式的模型文件，使用Gurobi求解器
- 特点：与mps.py功能相似，但使用Gurobi优化引擎
- 报告：生成与mps.py类似的LaTeX报告

### 4. qps.py
- 功能：处理QPS格式的模型文件（支持二次规划）
- 特点：能解析和处理二次目标函数和约束
- 报告：生成包含二次项分析的专业LaTeX报告

## 目录结构

```
/intern/
│
├── scripts/             # 核心脚本目录
│   ├── ampl.py          # AMPL模型处理脚本
│   ├── mps.py           # MPS文件COPT求解器
│   ├── mps_gurobi.py    # MPS文件Gurobi求解器
│   └── qps.py           # QPS格式解析器
│
├── ampl/                # AMPL模型和数据文件
│   ├── *.mod            # 模型文件
│   └── *.dat            # 数据文件
│
├── mps/                 # MPS格式模型文件
│   └── *.mps            # MPS文件
│
├── qps/                 # QPS格式模型文件
│   └── *.qps            # QPS文件
│
├── ampl_logs/           # AMPL求解日志目录
├── copt_logs/           # COPT求解日志目录
├── gurobi_logs/         # Gurobi求解日志目录
│
├── ampl_reports/        # AMPL生成的LaTeX报告
├── tex_reports/         # MPS生成的LaTeX报告
└── qps_reports/         # QPS生成的LaTeX报告
```

## 使用说明

### 环境配置

1. 确保已安装Python 3.6+
2. 安装所需的Python包：
   ```
   pip install amplpy coptpy gurobipy numpy
   ```
3. 确保相关求解器已正确安装并配置许可证

### 处理AMPL模型

```bash
python scripts/ampl.py <模型文件> [数据文件]
# 示例
python scripts/ampl.py ampl/transportation.mod ampl/transportation.dat
```

### 处理MPS文件（使用COPT求解器）

```bash
python scripts/mps.py <MPS文件>
# 示例
python scripts/mps.py mps/afiro.mps
```

### 处理MPS文件（使用Gurobi求解器）

```bash
python scripts/mps_gurobi.py <MPS文件>
# 示例
python scripts/mps_gurobi.py mps/afiro.mps
```

### 处理QPS文件

```bash
python scripts/qps.py <QPS文件>
# 示例
python scripts/qps.py qps/sample.qps
```

### 生成PDF报告

求解完成后，系统会生成LaTeX格式的报告文件。要将其转换为PDF，可以使用以下命令：

```bash
cd <报告目录>  # 如tex_reports
xelatex <报告文件>.tex
```

## 特色功能

### 智能变量格式化

系统会根据变量数量自动调整格式化方式：
- 如果变量超过100个，使用三位数填充（如X_{001}, X_{002}）
- 如果变量在10到99之间，使用两位数填充（如X_{01}, X_{02}）
- 如果变量少于10个，使用单位数（如X_{1}, X_{2}）

### 变量和约束排序

系统实现了智能排序功能，确保变量和约束按照逻辑顺序显示：
- 先按前缀字母排序
- 然后按数字大小排序
- 支持多维下标变量（如X[1,2], X[1,3]等）

### 自动日志记录

所有求解过程都会自动记录到对应的日志目录中，便于追踪和调试问题。

## 常见问题

1. **找不到模型文件？**
   - 确认文件路径正确
   - 尝试使用相对路径或绝对路径
   - 检查文件扩展名是否正确

2. **求解器许可证问题？**
   - 确保许可证文件位于license目录下
   - 检查环境变量是否正确设置
   - 对于商业求解器，确认许可证有效性

3. **如何定制报告格式？**
   - 直接修改脚本中的LaTeX模板部分
   - 调整`_build_mathematical_model_latex`等方法

4. **如何添加新的求解器？**
   - 参考现有求解器集成方式
   - 实现相应的接口和调用方法
   - 更新自动检测和选择逻辑

## 进阶使用

### 批处理多个模型

可以编写简单的批处理脚本，例如：

```python
import os
import subprocess

mps_files = ["file1.mps", "file2.mps", "file3.mps"]
for mps_file in mps_files:
    subprocess.run(["python", "scripts/mps.py", f"mps/{mps_file}"])
```

### 自定义求解参数

各脚本支持额外的求解参数设置，查看脚本帮助或源代码了解更多选项。

## 贡献指南

1. 遵循现有的代码风格和注释规范
2. 添加新功能时包含完整的中文注释
3. 确保新代码不破坏现有功能
4. 提交前进行充分测试

## 结语

本项目致力于提供高质量、易用的数学规划模型求解和报告生成工具。通过智能格式化和专业排版，使复杂的优化结果更加直观易懂，适合研究和教学使用。
