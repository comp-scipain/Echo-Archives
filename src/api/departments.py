from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter (
    prefix="/Departments",
    tags=["Departments"],
    dependencies=[Depends(auth.get_api_key)],
)

class Department(BaseModel):
    name: str
    basePay: float
    population: int


@router.post("/new/")
def add_new_department(dept: Department):
    """
    Add a new department to the Database
    """
    print(f"Adding department named {dept.name} with ${dept.basePay} base pay and population {dept.population}.")
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("INSERT INTO dept (dept_name, base_pay, dept_populus) VALUES (:name, :pay, :popul)"),
            {"name": dept.name, "pay": dept.basePay, "popul": 0}
        )
        print("Done")
    return {"status": "OK"}

