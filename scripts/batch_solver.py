# scripts/batch_solver.py

import os
import pandas as pd
from pyscipopt import Model
from contextlib import redirect_stdout
import io

# 设置路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MPS_DIR = os.path.join(BASE_DIR, 'mps')
SOLUTIONS_DIR = os.path.join(BASE_DIR, 'solutions')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# 确保输出文件夹存在
os.makedirs(SOLUTIONS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

def solve_mps(file_path):
    model = Model()
    model.readProblem(file_path)

    # 设置输出级别（可调节详细程度）
    model.setParam('display/verblevel', 4)
    model.setParam('display/freq', 1)

    # 捕获求解过程的控制台输出
    log_stream = io.StringIO()
    with redirect_stdout(log_stream):
        model.optimize()
    
    # 保存求解日志
    log_filename = os.path.splitext(os.path.basename(file_path))[0] + '.log'
    with open(os.path.join(LOGS_DIR, log_filename), 'w') as f:
        f.write(log_stream.getvalue())

    # 获取变量结果
    if model.getStatus() == 'optimal':
        results = []
        for var in model.getVars():
            val = model.getVal(var)
            results.append((var.name, val))

        df = pd.DataFrame(results, columns=["Variable", "Value"])
        mps_name = os.path.splitext(os.path.basename(file_path))[0]
        xlsx_path = os.path.join(SOLUTIONS_DIR, f"{mps_name}_solutions.xlsx")
        df.to_excel(xlsx_path, index=False)
        print(f"[✓] {mps_name} 求解完成，结果保存至 {xlsx_path}")
    else:
        print(f"[×] {file_path} 未找到最优解，状态为：{model.getStatus()}")

if __name__ == "__main__":
    print("开始批量求解 MPS 文件...\n")
    mps_files = [f for f in os.listdir(MPS_DIR) if f.endswith(".mps")]
    
    if not mps_files:
        print("未在 mps 文件夹中发现任何 .mps 文件。")
    else:
        for filename in mps_files:
            file_path = os.path.join(MPS_DIR, filename)
            print(f"正在求解：{filename}")
            solve_mps(file_path)
