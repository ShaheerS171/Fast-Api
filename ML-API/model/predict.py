import pickle
import pandas as pd

# now first we will import the model using the pickel
with open("model/model.pkl", 'rb') as f:
  model = pickle.load(f)

def predict_output(user_input: dict):
  input_df = pd.DataFrame([user_input])
  output = model.predict(input_df)[0]
  return output