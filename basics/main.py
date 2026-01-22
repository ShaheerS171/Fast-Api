# the fast api is for the fast api http exception is to give the costumizable exception while the path is to give
# the good description to your path parameters 
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional# Literal is use to give the specific option to the user
import json

app = FastAPI() # making the object of the fast api

class Pateint(BaseModel):
  # now add the field the patient required to fill
  id: Annotated[str, Field(..., description= "id of the patient", examples=["P001"])]
  name: Annotated[str, Field(..., description="Name of the patient")]
  city: Annotated[str, Field(...,  description=" Where the patient is living")]
  age: Annotated[int, Field(..., description=" Age of the patient", gt=0, lt=120)]
  gender: Annotated[Literal["male", "female", "Other"], Field(default="Male", description="Gender of the patient")]# wew dont need the required after the default value
  height: Annotated[float, Field(..., description="Give me the weight in ft", gt= 0, lt= 8)]
  weight: Annotated[float, Field(..., description=" give me the weight in lb", gt=0, lt= 250)]

  @computed_field
  @property
  def bmi(self) -> float:
    bmi = self.weight/(self.height**2)
    return bmi
  
  @computed_field
  @property
  def verdict(self) -> str:
    if self.bmi < 18.5:
      return "under weight"
    elif self.bmi < 25:
      return "normal"
    elif self.bmi < 30:
      return "normal"
    else:
      return "obese"

class Patient_update(BaseModel):
  name:   Annotated[Optional[str], Field(default= None)]
  city:   Annotated[Optional[str], Field(default= None)]
  age:    Annotated[Optional[int], Field(default = None, gt = 0)]
  gender: Annotated[Optional[Literal["male", "female", "Other"]], Field(default="male")]# wew dont need the required after the default value
  height: Annotated[Optional[float], Field(default= None, gt= 0)]
  weight: Annotated[Optional[float], Field(default= None, gt=0, lt= 250)]


# here we will make the function to load the data from the json file
def load_data():
  with open("patients.json", "r") as f:
    return json.load(f) # this is the method to load the json file in the easiest way possible

@app.get("/")
def hello():
  return (" Patient management system Api")

# this is how to make the routes in the fast api
@app.get("/about")
def about():
  return ("A fully functional api to manage your patient records")

# we will make the patient system api but before this we will have to make the one for the data loading for the json file
@app.get("/view")
def view_patient():
  data = load_data() # now this will load the data into the data
  return data

@app.get("/patient/{id}") # this is how you give the parameter in it. It is like i wanna see this patient id
# this is how you give the path parameters the ... is that the field is required and the other things are defined by their names
def search_patient(id: str = Path(..., description= "Give the id of the patient you wanna see", examples= ["P001"])): # This is how you give the parameter in the python
  data = load_data() # load the data of the patient in there 
  if id in data:
    return data[id] # if the id of the patient is present in the data then return the whole thing to the user
  else:# this is how you raise the exception of your choice in the fast api
    raise HTTPException(status_code= 404, detail= "There is no patient with such id in this data base")
  
@app.get("/sort")
# now the query parameters we will not get them in the route we will get them into the function itself
# now here the 3 dots in the first parameter mean that it is required but the second one we dont need this we 
# have set the default value if the user wants to change it it is up to him
def sort_patient(sort_by: str =
                Query(..., description= "Sort on the basis of height, weight and bmi"),
                order: str = Query('asc', description= "sort it in the ascending or the descending" )):
  
  # now first we will see if the sorting is in the correct order
  valid_field = ["height", "weight", "bmi"]

  if sort_by not in valid_field:# the status code 404 represents the bad reuest from the user
    raise HTTPException(status_code= 404, detail="There is no field to be sorted like this") 
  if order not in ["asc", "dcs"]:
    raise HTTPException(status_code= 404, detail="Select between asc, dsc") 

  data = load_data()
  # now we have to make the code so the data is sorted as the user requested to us

  # now this is the code to sort the things up, reverse = true means the descending order. sort_by, 0 means
  # if the value is not given then consider it 0. sorted is the built in function in the python. So this is
  # the code to sort things up in thsi case. we will have to make our own logic in the different things
  sort_order = False if order == "asc" else True
  sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse=sort_order)
  return sorted_data

# save the data into the json file
def save_data(data):
  with open("patients.json", "w") as f:
    json.dump(data, f)# this will convert thr python dictionary into the  json file

# this is how to create the post route   
@app.post("/create")
# now the user will send the data to us in the form of the json or anything and we will send it to the pydantic
def create_pateint(patient: Pateint):
  
  # load the existing data into the file 
  data = load_data()

  #check if the patient already exist or not
  if patient.id in data:
    raise HTTPException(status_code=400, detail="Patient already exist")

  # add the new patient to the data base
  # now we have to add the pydantic object patient into the python dictionary
  # now we exclude the id cause the id is in the successive term 
  data[patient.id] = patient.model_dump(exclude={'id'})

  save_data(data)

  # Now we will give the json response to tell the user that the patient have been created
  return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})


@app.put("/edit/{patient_id}")
def update_record(patient_id: str, patient: Patient_update): # we are taking the id to be updated and the object of the patient update
  
  data = load_data()
  if patient_id not in data:
    raise HTTPException(status_code= 400, detail= "Patient not found")
  
  # now if the patient id is correct then we will extract the whole info of that patient and then we will update this 
  existing_info = data[patient_id]

  patient_updates = patient.model_dump(exclude_unset= True) # in this case we are only getting the values which are set by the client not all the fields
  # now we have the existing and the updated data
  # now we will run a loop in which we have the loop over the items of the updated dictionary and for each element we will have update the value
  for key, value in patient_updates.items():
    existing_info[key] = value

  # now before updating the data we will have to update the bmi as well as the other things. So we will make the new pydantic object of the updated data and then store it into the file
  existing_info['id'] = patient_id
  paitent_overall = Pateint(**existing_info)

  final = paitent_overall.model_dump(exclude={'id'})
  data[patient_id] = final
  save_data(data)
  return JSONResponse(status_code=200, content={"message": "Patient successfully updated"})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
  data = load_data()

  if patient_id not in data:
    raise HTTPException(status_code= 404, detail= "Patient not exist")
  
  del data[patient_id]
  save_data(data) 

  return JSONResponse(status_code= 200, content= {"message": "Patient has been deleted from the data base"})
