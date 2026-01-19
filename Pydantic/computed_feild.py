# now we will talk about the computed field. 
# Computed feild are those in which we compute the values of the one from the given things
from pydantic import BaseModel, EmailStr, Field, field_validator, computed_field
from typing import List, Dict, Optional,Annotated

class Patient(BaseModel):

  name: str
  email: EmailStr
  age: int 
  weight: float
  married: bool
  allergies: List[str]
  contact_detail: Dict[str, str]
  # now we will compute the bmi of a persom using the weight and the height

  @computed_field
  @property
  def compute_bmi(self) -> float:
    bmi = self.weight/2
    return bmi

