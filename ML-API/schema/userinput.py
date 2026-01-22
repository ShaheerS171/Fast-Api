from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Optional, Literal, Annotated
from config.city_tier import tier_1_cities, tier_2_cities

Model_version = 1.0

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
  
  @field_validator('city')
  @classmethod
  def normalize_city(cls, v: str) -> str:
    v = v.strip().title() # .strip will remove any extra spaces and the title will make it like Lahore
    return v
     

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