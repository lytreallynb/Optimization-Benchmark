from pyscipopt import Model

model = Model()
try:
    model.readProblem("de063155.mps")
    model.optimize()
    print("Status:", model.getStatus())
except Exception as e:
    print("❌ 出错:", e)
