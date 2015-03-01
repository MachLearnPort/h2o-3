import sys, os
sys.path.insert(1, "../../../")
import h2o

def getModelGBM(ip,port):
  # Connect to h2o
  h2o.init(ip,port)

  prostate = h2o.import_frame(path="smalldata/logreg/prostate.csv")
  #prostate.summary()
  prostate_gbm = h2o.gbm(y=prostate[1], x=prostate[2:9], nfolds=5)
  prostate_gbm.show()

  # Can't specify both nfolds >= 2 and validation data at once
  try:
    h2o.gbm(y=prostate[1], x=prostate[2:9], nfolds=5, validation_y=prostate[1], validation_x=prostate[2:9])
    assert False, "expected an error"
  except EnvironmentError:
    assert True

  prostate_gbm.predict(prostate)
  model = prostate_gbm.key().getModel()
  model.show()

if __name__ == "__main__":
  h2o.run_test(sys.argv, getModelGBM)
