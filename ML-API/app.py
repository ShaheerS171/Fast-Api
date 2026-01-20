from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Optional, Literal, Annotated
import pickle
import pandas as pd

 # now first we will import the model using the pickel
with open("model.pkl", 'rb') as f:
  model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# now we will make the pydantic model
class user_input(BaseModel):
  age: Annotated[int, Field(..., description= "Give the age of the person", gt=0, lt=  100)]
  weight: Annotated[float, Field(..., description= "Give the weight of the person", gt=0, lt=  200)]
  height: Annotated[float, Field(..., description= "Give the height of the person", gt=0, lt=  2.5)]
  income_lpa: Annotated[float, Field(..., description= "Give the annual pay of the person", gt=0)]
  smoker: Annotated[bool, Field(..., description= "Is the person smoker or not")]
  city: Annotated[str, Field(..., description= "The city person lives in")]
  occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government job', 'business owner', 'unemployed', 'private job'],
                        Field(..., description= "Tell me the current occupation of the user")]
  
  # now we have to make the new feilds using these feilds
  @computed_field
  @property
  def bmi(self) -> float:
    bmi = self.weight/(self.height**2)
    return bmi #so the bmi has been obtained
  
  @computed_field
  @property
  def life_style(self) -> str:
    if self.smoker and self.bmi> 30:
      return 'high'
    elif self.smoker or self.bmi> 27:
      return 'medium'
    else:
      return 'low'
    
  @computed_field
  @property
  def age_group(self) -> str: 
    if self.age< 25:
      return 'young'
    elif self.age< 45:
      return 'adult'
    elif self.age< 60:
      return 'middle-age'
    else:
      return 'senior'
    
  @computed_field
  @property
  def city_tier(self) -> int:
    if self.city in tier_1_cities:
      return 1
    elif self.city in tier_2_cities:
      return 2
    else:
      return 3
  
@app.post('/predict')
def predict_premium(data: user_input):
  # we have to send this data in the form of the pandas data frame cause the random forest is trained on the data frame
  # the validation is done when we call the pydantic object
  input = pd.DataFrame([{
    'age_group': data.age_group,
    'lifestyle_risk': data.life_style,
    'occupation': data.occupation,
    'city_tier': data.city_tier,
    'bmi': data.bmi,
    'income_lpa': data.income_lpa
  }])

# now our data is in the form of the pandas data frame so now we will predict the results
  prediction = model.predict(input)[0]# 0 mean we only need the row

  return JSONResponse(status_code= 200, content={'Predicted category': prediction})