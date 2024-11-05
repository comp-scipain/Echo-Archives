# Example Flow
John Apple is the COO of a small tech company and needs a way to keep track of his employees. First, John creates a department to track by calling `POST /Departments/new/`. He's also going to need to add all of his employees to the database using `POST /employee/add`. After setting everything up he's curious about how much money all employees per given department is being payed. So he calls `GET /Departments/department/total_pay` which tells him that the marketing department is being payed 18,523,691.45 in total. Which can help him decide whether he should reduce the number of employees working that department or not.

# Testing results

`POST /Departments/new/`
1. Request
```bash
curl -X 'POST' \
  'https://echo-archives.onrender.com/Departments/new/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "IT",
  "basePay": 26.49,
  "population": 0
}'
```

2. Response
```python
{
  "status": "OK"
}
```

`POST /employee/add`
1. Request
```bash
curl -X 'POST' \
  'https://echo-archives.onrender.com/employee/add' \
  -H 'accept: application/json' \
  -H 'access_token: a' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Sergio",
  "skills": [
    "Network Troubleshooting","Computer Troubleshooting"
  ],
  "department": "IT"
}'
```

2. Response
```python
{
  "status": "OK"
}
```


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
  "total_pay": 133.07
}
```