# in the nested modeling you use one model as a field in the other model 
from pydantic import BaseModel

class Address(BaseModel):
  city: str
  state: str
  pin: int 

class Patient(BaseModel):
  name: str
  gender: str
  age: int
  address: Address

# now what should be the data set of the adress it contains the numbers string and more things. So what will you do now
# make another model adress and use this as the field in this model
adress = {'city': 'Khanewal', 'state': 'Punjab', 'pin': 4324}
patient_adress = Address(**adress)

patient_dict = {'name': 'shaheer', 'gender': 'male', 'age': 12, 'address': patient_adress}
patient1 = Patient(**patient_dict)

print(patient1.address) # this is how to use the nested model