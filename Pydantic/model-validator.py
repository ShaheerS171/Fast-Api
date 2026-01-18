# now if you want to apply the condition that if the person is < 12 then he should have the emergency contact 
# now in this case we are dealing with the 2 fields but the field validator only deals with 1 field so in this case we will use the field validator
# in the  model validation we can combine the 2 feild to make the one feild validation 
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import List, Dict, Optional,Annotated

class Patient(BaseModel):

  name: str
  email: EmailStr
  age: int 
  weight: float
  married: bool
  allergies: List[str]
  contact_detail: Dict[str, str]

  # now we will make the model validator 
  @model_validator(mode= "after")
  def emergency(cls, model): # give the whole class and the whole model so you can access any feild in the class
    if model.age > 60 and 'emergency' not in model.contact_detail:
      raise ValueError("please give the emergency info")
    return model 

patient_info = {'name': 'Shaheer', "email": "abc@gmail.com", 'age': 10, 'weight': 75.2, "married": True, 'allergies': ["pollen", "something"], "contact_detail": {"phone no": "0310134032432"}}

patient1 = Patient(**patient_info)

def insert_patients(patient: Patient): 
  print(patient.name)
  print(patient.age)
  print(patient.married)
  if patient.allergies:
    for allergy in patient.allergies:
      print(allergy)
  for key, val in patient.contact_detail.items():
    print(f"{key}: {val}")
  print([patient.weight])
  print("Patient have been added to the system")
  print(patient.email)

insert_patients(patient1) 