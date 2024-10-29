from fastapi import APIRouter, Depends
from pydantic import BaseModel
#Remember to uncomment this in order to work with render and supabase
#from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter (
    prefix="/Employee",
    tags=["Employee"],
    #Gonna need this later for supabase and render
    #dependencies=[Depends(auth.get_api_key)],
)
    

class Employee(BaseModel):
    name: str

    skills: list[str]
    pay: float

    department: str


@router.post("/get")
def get_employee_stats(Employee: Employee):

    print(f"Name: {Employee.name}")
    print(f"Skills: {Employee.skills}")
    print(f"Pay: {Employee.pay}")
    print(f"Department: {Employee.department}")