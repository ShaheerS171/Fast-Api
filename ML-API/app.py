from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from schema.userinput import user_input
from model.predict import predict_output

app = FastAPI()
Model_version = 1.2

@app.get('/')
def home_msg():
  return {'message': 'insurance premium something'}

@app.get('/health')
def health_check():
  return {
    'status': 'okay',
    'version': Model_version
  }

@app.post('/predict')
def predict_premium(data: user_input):
  # we have to send this data in the form of the pandas data frame cause the random forest is trained on the data frame
  # the validation is done when we call the pydantic object
  user_input_dict = {
    'age_group': data.age_group,
    'lifestyle_risk': data.life_style,
    'occupation': data.occupation,
    'city_tier': data.city_tier,
    'bmi': data.bmi,
    'income_lpa': data.income_lpa
  }

  prediction = predict_output(user_input_dict)

  return JSONResponse(status_code= 200, content={'Predicted category': prediction})