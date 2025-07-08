import os
import time
from pyscipopt import Model
import pandas as pd

MPS_DIR = "../mps"
OUTPUT_DIR = "../solutions"
LOG_PATH = "../logs/run_log.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def solve_mps(file_path, output_path):
    model = Model()
    model.readProblem(file_path)
    model.optimize()

    solution = [(v.name, model.getVal(v)) for v in model.getVars()]
    df = pd.DataFrame(solution, columns=["Variable", "Value"])
    df.to_excel(output_path, index=False)

def log(message):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)

def main():
    mps_files = [f for f in os.listdir(MPS_DIR) if f.endswith(".mps")]
    if not mps_files:
        log("⚠️ 没有找到任何 .mps 文件")
        return

    log("====== 批量求解开始 ======")
    for filename in mps_files:
        mps_path = os.path.join(MPS_DIR, filename)
        base_name = filename.replace(".mps", "")
        output_name = f"{base_name}_solutions.xlsx"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        try:
            start = time.time()
            solve_mps(mps_path, output_path)
            duration = time.time() - start
            log(f"✅ {filename} 求解成功 | ⏱ {duration:.2f}s | 输出: {output_name}")
        except Exception as e:
            log(f"❌ {filename} 求解失败 | 错误: {e}")

    log("====== 批量求解结束 ======\n")

if __name__ == "__main__":
    main()
