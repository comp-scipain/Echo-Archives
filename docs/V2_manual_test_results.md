# Example Flow
Kevin Coopa is the president of a video game development company who's been using our app for a little while. A need to move a couple employees to the legal department for upcoming lawsuit. So he calls `POST /employee/transfer` to transfer various qualified employees from other departments to the Legal department. After winning the lawsuit, he decides that the employees that worked on it deserve a promotion. So he uses `POST /employee/promote` to give those employees a promotion which raises their pay by 7%. 


# Testing results
`POST /employee/transfer`

1. Request
```bash
curl -X 'POST' \
  'https://echo-archives.onrender.com/employee/transfer?employee_id=7&new_department=Legal' \
  -H 'accept: application/json' \ 
  -d ''
```

2. Response
```python
{
  "status": "OK",
  "new_department": "Legal",
  "new_pay": 89.75,
  "new_level": 0
}
```

`POST /employee/promote`

1. Request
```bash
curl -X 'POST' \
  'https://echo-archives.onrender.com/employee/promote?employee_id=7' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -d ''
```

2. Response
```python
{
  "status": "OK",
  "new_level": 1,
  "new_pay": 96.03
}
```


# Example Flow
Macrohard, the largest AI company in the world, is struggling to expand due to current economic conditions. So they must downsize in order to maintain profits. So they call `GET /Departments/department/total_pay` to assess how much all the employees in each department is being payed. After some deliberation, they call `POST /employee/delete` to remove a few employees from the database and call `POST /employee/demote` to reduce the pay of some their remaining employees by 7%.

# Testing results
`GET /Departments/department/total_pay`

1. Request
```bash
curl -X 'GET' \
  'https://echo-archives.onrender.com/Departments/department/total_pay?department_name=Legal' \
  -H 'accept: application/json' \
```

2. Response
```python
{
  "department": "Legal",
  "total_pay": 229.1
}
```

`POST /employee/delete`

1. Request
```bash
curl -X 'POST' \
  'https://echo-archives.onrender.com/employee/delete?employee_id=5' \
  -H 'accept: application/json' \
  -d ''
```

2. Response
```python
{
  "status": "OK"
}
```

`POST /employee/demote`

1. Request
```bash
curl -X 'POST' \
  'https://echo-archives.onrender.com/employee/demote?employee_id=7' \
  -H 'accept: application/json' \
  -d ''
```

2. Response
```python
{
  "status": "OK",
  "new_level": 0,
  "new_pay": 89.31
}
```