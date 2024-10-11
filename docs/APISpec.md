# API Specification for Fitness Tracker App

### Get Workouts - `/workouts/` (GET)
Retrieves a list of workouts that are supported on the fitness app.

Response:
```python
[
  {
    "name": str,
    "muscle_groups": str[],
  }
]
```

### Add Custom Workout - `/workouts/{workout_name}` (POST)
Add a custom workout to the app. Note that the name of this workout must not conflict with any workouts already existing in the database.

Request:
```python
[
  {
    "name": str, # Must be unique
    "muscle_groups": str[],
  }
]
```

### Get set number - `/set_number/` (POST)
Returns the weight of 

Request:

```python
{
  "set_number": int
}
```

### Get rest time - `/rest_time/` (POST)
Returns 

Request:

```python
{
  "rest_time": int 
}
```

### Get Workouts`/workouts/{muscle_groups}` (GET)
Returns muscle workouts that work out a specific muscle group.

Request:
```python
[
  {
    "muscle_groups": str[],
  }
]
```
Response:
```python
[
  {
    "workout_names": str[],
  }
]
```

### `/`

Request:

```python

```

### `/`

Request:

```python

```

### `/`

Request:

```python

```
