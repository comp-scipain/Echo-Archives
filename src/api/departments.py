from fastapi import APIRouter, Depends, HTTPException
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



@router.get("/department/total_pay")
def get_total_department_pay(department_name: str):
    """
    Returns the total pay for all employees in the specified department
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("SELECT SUM(pay) FROM employees WHERE department = :department_name"),
            {"department_name": department_name}
        ).fetchone()

        if not result or result[0] is None:
            raise HTTPException(status_code=404, detail="Department not found or no employees in the department")

        total_pay = result[0]
        
        print(f"Total pay for department {department_name} is: ${total_pay:.2f}")
        return {"department": department_name, "total_pay": total_pay}

@router.post("/departments/total_paid")
def get_total_paid_by_department():
    """
    Calculates the total paid value for each employee by multiplying their wage by the days employed,
    and aggregates this total by department.
    """
    try:
        with db.engine.begin() as connection:
            history_records = connection.execute(
                sqlalchemy.text("SELECT days_employed, day_wage, in_dept FROM history")
            ).fetchall()

            if not history_records:
                raise HTTPException(status_code=404, detail="No history records found")

            department_totals = {}
            for record in history_records:
                department = record[2]
                total_paid = record[0] * record[1]  # days_employed * day_wage

                if department in department_totals:
                    department_totals[department] += total_paid
                else:
                    department_totals[department] = total_paid

            formatted_totals = [
                {"department": dept, "total_paid": round(total, 2)}
                for dept, total in department_totals.items()
            ]

            print(f"Total paid by department: {formatted_totals}")
            return {"status": "OK", "total_paid_by_department": formatted_totals}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while calculating the total paid by department")
