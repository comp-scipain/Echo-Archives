# API Specification for Echo Archive

## Employees

### Promote Employee - `/employee/promote` (POST)
Promotes an employee by increasing their level by 1 and increasing their pay by approximately 7%.

Request:
```python
{
  "employee_id": int
}
```

Response:
```python
{
  "success": bool,
}
```

### Demote Employee - `/employee/demote` (POST)
Demotes an employee by decreasing their level by 1 and decreasing their pay by approximately 7%

Request:
```python
{
  "employee_id": int
}
```

Response:
```python
{
  "success": bool,
}
```

### Transfer Employee - `/employee/transfer` (POST)
Transfers an employee to a new department, resetting their pay, level, and updating department population.

Request:
```python
{
  "employee_is": int,
  "new_department": str,
}
```

Response:
```python
{
  "success": bool,
}
```




### Get Employees - `/employee/get` (GET)
Retrieves a list of all current employees.

Response:
```python
[
  {
    "name": str,
    "skills": str[],
    "pay": float,
    "department": str
  },
{
...
}
]
```

### Add New Employee - `/employee/add` (POST)
Add a new employee to the roster

Request:
```python
[
  {
    "name": str,
    "skills": str[],
    "pay": float,
    "department": str,
    "level": int
  }
]
```

### Search Employees - `/employee/search` (GET)
Searches for employees based on specified query parameters

**Query Parameters**
- `employee_name`: The name of the employee.
- `skills`: The muscle groups that the workout targets

**Response**:
- `results`: A list of each line item has the following properties:
  - `employee_name`: A string that represents the name of the employee
  - `skills`: A list of strings that represents the skills that each employee has


### Reset App - `/admin/reset/` (POST)
A call to Reset App will erase all saved data. Should only be called when the user no longer uses the app and wants to delete everything.

### Fire Employee - `/employee/delete` (POST)
Fire an employee (remove from database) based on a specified ID
Request:
```python
{
  "employee_id": int
}
```
Response:
```python
{
  "status":"OK"
}
```

### Get Total Paid By Employee - `/employee/total_paid` (POST)
Calculates the total paid value for a specific employee and aggregates this total by department.

Request:
```python

```
Response:
```python

```

### Log Employee History (POST)
Logs an employee's history into the history table. (Gets Called automatically whenever `/employee/promote`, `/employee/transfer`, or `/employee/demote` are called. It can also be called manually)

Request:
```python
{
  "Employee_id": int,
  "days_employed": int,
  "day_wage": float,
  "department": str
}
```
Response:
```python
{
  "status": "OK"
}
```

## Departments  

### Create New Department - `/Departments/new` (POST)
Adds a new department to the database 

Request:
```python
[
  {
    "name": str,
    "basepay": int,
    "population": int
  }
]
```
Response:
```python
{
  "Status": "OK"
}
```


### Get Total Department Pay - `/department/daily_pay` (POST)
Returns the total pay for all employees in the specified department

Request:
```python
{
  "department_name": str
}
```

Response:
```python
{
  "status": "OK",
  "total_paid_by_department": list
}
```

### Get Total Paid By Department - `/departments/total_paid` (POST)
Calculates the total paid value for each employee by multiplying their wage by the days employed, and aggregates this total by department.

Request:
```python

```
Response:
```python
{
  "status": "OK",
  "total_paid_by_department": list
}
```

### Get Department History - `/department/history` (GET)
Fetches the employment history of all employees who were in the specified department, aggregating the days employed for each employee.
Request:
```python
{
  "department_name": str
}
```
Response:
```python
{
  "Status": "OK"
  "department_history": list[employee_history]
}
```