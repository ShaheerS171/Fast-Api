from pydantic import BaseModel, EmailStr, Field, field_validator
# EmailStr is the variable in the pydantic that will automatically check the email 
# Now we will import the field_validator from the pydantic module
from typing import List, Dict, Optional,Annotated

class Patient(BaseModel):

  name: str
  email: EmailStr
  age: int 
  weight: float
  married: bool
  allergies: List[str]
  contact_detail: Dict[str, str]

  @field_validator('email') # always use the this and give hte value you want to validate
  @classmethod # you have to tell the compiler that this is the calss method
  def email_validator(cls, val): # give the value and perform the validation on this value

    print("VALIDATOR CALLED WITH:", val)   
    valid_domains = ["gmail.com"]
    domain_name =  val.split('@')[-1] # this will split the value from the @ and dont give hte @
    if domain_name not in valid_domains:
      raise  ValueError(" Not a valid value")
    return val
  
  # now we will make the field validator that will make the name in the capital letter
  # this is exactly how the field validator works
  @field_validator('name')
  @classmethod
  def name_validator(cls, value):
    return value.upper()

patient_info = {'name': 'Shaheer', "email": "abc@gmail.com", 'age': 10, 'weight': 75.2, "married": True, 'allergies': ["pollen", "something"], "contact_detail": {"phone no": "0310134032432"}}

#now we will make the object
patient1 = Patient(**patient_info)# the ** is the dictionary unpacking operator which will give all the parameter in the dictionary one by one

# now the data is cleaned we can send it to our function is well

def insert_patients(patient: Patient): # now we are getting the object of the patient as teh parameter
  print(patient.name)
  print(patient.age)
  print(patient.married)
  if patient.allergies:# now you have to apply the check condition if the allergies exist or not
    for allergy in patient.allergies:
      print(allergy)
  for key, val in patient.contact_detail.items():
    print(f"{key}: {val}")
  print([patient.weight])
  print("Patient have been added to the system")
  print(patient.email)

insert_patients(patient1) 