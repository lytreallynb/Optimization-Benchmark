from highspy import Highs
model = Highs()
model.readModel("bal8x12.mps")
model.run()
model.writeSolution("solution.txt",1)