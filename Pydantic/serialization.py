# now we will talk about the serialization. In this we send our pydantic object in form of the pythotn dict or the json file to use it in the fast api
# pydantic gives us the built in method to learn this one
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

# this method will convert the object into the python dictionary
# you can also select which field to dump
# similarly you can use the exclude and will also get the default value 
temp = patient1.model_dump(include={'name', 'gender'})
print(temp)
print(type(temp))

# This is how to convert the object into the json file  the type of this will be string 
temp2 = patient1.model_dump_json()