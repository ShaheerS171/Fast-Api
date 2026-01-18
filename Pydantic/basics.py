from pydantic import BaseModel, EmailStr, Field # EmailStr is the variable in the pydantic that will automatically check the email 
from typing import List, Dict, Optional,Annotated # to make the pydantic object optoinal so we dont need them all along

# all the fields in the pydantic i required by default. But you can make them optional 
# there is another validator in the pydantic known as the anyurl. It will check the url 
# Now if you want apply some costum rules then you can use the field validaotr of the pydantic
# you can also include the description in the field using the field validator
# So the annotated is use for the field validator to add the description as it is shown below
# Now there is a thing known as the field validator. In this you will make the costum changes to your feilds
# like wether you want to add something apply a check make the first letter of the name capital then you will use this one
# The example of all this is given below

# now we will make the schema of our program in this we will make the validation test 
class Patient(BaseModel): # Now this class should always take the base model in order to make it the pydantic class
  name: Annotated[str, Field(max_length=50, title= "name of the title", description="give the name", examples=["shaheer"])] # This is how to use the annotaiotn to combine the description with the field validator
  email: EmailStr # now we are checking the email using the pydantic email checker
  age: int
  # The strict is use to make it like if "75" is given then it will not convert it into the 75. This is to supress this behaviour
  weight: Annotated[float, Field(gt=0, strict= True)] # This is how to use the field validator. In this the weight should be greater then 0
  married: Annotated[bool, Field(default= None, description= "is the patient married or not")] # In this way you can give the default value to all the parameters
  # This is how to make the things optinal in the easiest way using the optional module from typing module
  allergies: Optional[list[str]] = Field(max_length=5) # now this is how to initiate the list but for this you have to import the list from the typing module but you have to give the default value
  contact_detail: Dict[str, str] # now the first str refer to the string while the second one refers to the value

# now we will perform the second step in which we will make the object of the model 
# first we will make the dictionary that we will pass to the object
patient_info = {'name': 'Shaheer', "email": "abc@gmail.com", 'age': 10, 'weight': 75.2, 'allergies': ["pollen", "something"], "contact_detail": {"phone no": "0310134032432"}}

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

insert_patients(patient1) # now we can use the same function with the similar function with same object

"""Note: You have to define all the variable of the pydantic in the single class. Dont make different class
for all the objects. Make the single one and test as many parameters as you like. and pydantic will also  convert
the '30' into the integer. It will not give the error"""