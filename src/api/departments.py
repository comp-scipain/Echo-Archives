from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
import time

router = APIRouter (
    prefix="/departments",
    tags=["departments"],
    dependencies=[Depends(auth.get_api_key)],
)

class Department(BaseModel):
    name: str
    basePay: float
    population: int


@router.post("/new")
def add_new_department(dept_name: str, dept_basePay: float):
    #Execution Time: 0.024ms
    """
    Add a new department to the Database
    """
    if dept_basePay < 0:
        return {"error":"dept_basePay can't be a negative number"}
    print(f"Adding department named {dept_name} with ${dept_basePay} base pay and population {0}.")
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("INSERT INTO dept (dept_name, base_pay, dept_populus) VALUES (:name, :pay, :popul)"),
            {"name": dept_name, "pay": dept_basePay, "popul": 0}
        )
        print("Done")

    return {"status": "Successfully added new department"}



@router.get("/daily_pay")
def get_total_department_pay(department_name: str):
    #Execution Time: 119.029ms
    """
    Returns the total pay for all employees in the specified department
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("SELECT ROUND(CAST(SUM(pay) AS decimal), 2) FROM employees WHERE department = :department_name"),
            {"department_name": department_name}
        ).fetchone()

        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="Department not found or no employees in the department")

        total_pay = result[0]
        print(f"Total pay for department {department_name} is: ${total_pay:.2f}")
        return {"department": department_name, "total_pay": total_pay}

@router.post("/total_paid")
def get_total_paid_by_department():
    #Execution Time: 111.974ms
    try:
        with db.engine.begin() as connection:

            connection.execute(
                sqlalchemy.text("""
                    CREATE INDEX IF NOT EXISTS idx_history_total_calc 
                    ON history(in_dept, days_employed, day_wage)
                    INCLUDE (days_employed, day_wage)
                """)
            )
            
            history_records = connection.execute(
                sqlalchemy.text("""
                    SELECT days_employed, day_wage, in_dept 
                    FROM history
                    WHERE in_dept IS NOT NULL
                    ORDER BY in_dept
                """)
            ).fetchall()

            if not history_records:
                raise HTTPException(status_code=404, detail="No history records found")


            department_totals = {}
            for record in history_records:
                department = record[2]
                total_paid = record[0] * record[1]
                department_totals[department] = department_totals.get(department, 0) + total_paid

            formatted_totals = [
            {"department": dept, "total_paid": round(amount, 2)}
            for dept, amount in department_totals.items()
            ]

            return {"status": "OK", "total_paid_by_department": formatted_totals}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while calculating the total paid by department")
    

@router.get("/history")
def get_department_history(department_name: str):
    #Execution Time: 8.533ms
    """
    Fetches the employment history of all employees who were in the specified department,
    aggregating the days employed for each employee.
    """
    with db.engine.begin() as connection:
        history_records = connection.execute(
            sqlalchemy.text("SELECT emp_id, emp_name, days_employed, day_wage FROM history WHERE in_dept = :department_name"),
            {"department_name": department_name}
        ).fetchall()

        if not history_records:
            raise HTTPException(status_code=404, detail="No history records found for the specified department")

        employee_history = {}
        for record in history_records:
            emp_id = record[0]
            if emp_id in employee_history:
                employee_history[emp_id]["days_employed"] += record[2]
            else:
                employee_history[emp_id] = {
                    "emp_id": emp_id,
                    "emp_name": record[1],
                    "days_employed": record[2],
                    "day_wage": record[3]
                }

        department_history = list(employee_history.values())

        print(f"Fetched history for department: {department_name}")
        return {"status": "OK", "department_history": department_history}
