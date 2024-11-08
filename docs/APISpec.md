# API Specification for Echo Archive

Get Employees (GET)  #Could implement an option to choose specific department or whole company

Search Employees (GET)


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

### Create New Department (POST)
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

### Transfer Employee (POST)
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

///Get Department Employees (GET) #Could merge with Get Employees

/Get Department Payroll (GET)


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


### OLD STUFF FROM PREVIOUS PROJECT
### Get User Workouts - `/workouts/{user_id}` (GET)
Retrieves a list of workouts that are associated with user id.

Response:
```python
[
  {
    "workouts": str[],
  }
]
```

### Add User - `/users` (POST)
Adds a user to the database

Request:
```python
[
  {
    "first_name": int,
    "last_name": int,
  }
]
```

### Add a Workout to a User - `/users/{user_id}/workouts` (POST)
Adds a new workout to a user's account.

Request:
```python
[
  {
    "name": str,
    "sets": int,
    "reps": int[],
    "weight": int[],
    "rest_time": int[],
  }
]
```

### Get Muscle Distribution - `/analysis/{user_id}/distribution/` (GET)
Retrieves the muscle distribution of the workouts for a given user.

Response:
```python
[
  {
    "result": Distribution;
  }
]
```
```python
class Distribution:
  "chest": int,
  "back": int,
  "biceps": int,
  "triceps": int,
  "shoulders": int,
  "glutes": int,
  "calves": int,
  "quads": int,
  "hamstrings": int,
  ...
```

### Get Workout Analysis - `/analysis/{user_id}/` (GET)
Returns a general analysis of a user's workout.

Response:
```python
[
  {
    "average_duration": int,
    "average_workouts_per_week": int,
    "average_cals_burned_per_workout": int,
    "progression": Literal["very slow", "slow", "average", "fast", "very fast"]
  }
]
```

### Get Workout Improvement Tips - `/analysis/{user_id}/tips/` (GET)
Analyzes a user's workout routine and returns improvement tips.

Response:
```python
[
  {
    "sets": {
        "analysis": Literal["low", "just_right", "excessive"],
        "target": int,
      },
    "reps": {
        "analysis": Literal["low", "just_right", "excessive"],
        "target": int,
      },
    "weight": {
        "analysis": Literal["low", "just_right", "excessive"],
        "target": int,
      },
    "rest_time": {
        "analysis": Literal["low", "just_right", "excessive"],
        "target": int,
      }
  }
]
```
