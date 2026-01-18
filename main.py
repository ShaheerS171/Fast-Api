# the fast api is for the fast api http exception is to give the costumizable exception while the path is to give
# the good description to your path parameters 
from fastapi import FastAPI, HTTPException, Path, Query
import json

app = FastAPI() # making the object of the fast api

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
def search_patient(id: str = Path(..., description= "Give the id of the patient you wanna see", example= "P001")): # This is how you give the parameter in the python
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