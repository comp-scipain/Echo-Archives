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

### Search Workouts - `/workouts/search` (GET)
Searches for workouts based on specified query parameters

**Query Parameters**

- `workout_name`: The name of the workout.
- `muscle_groups`: The muscle groups that the workout targets

**Response**:
- `results`: A list of each line item has the following properties:
  - `workout_name`: A string that represents the name of the workout
  - `muscle_groups`: A list of strings that represents the muscle groups that the workout targets


### Reset App - `/admin/reset/` (POST)
A call to Reset App will erase all saved workout data. Should only be called when the user no longer uses the app and wants to delete everything.


### Get Workouts - `/workouts/{muscle_groups}` (GET)
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
    "name": str[],
  }
]
```

### Current time - `/info/current_time` (POST)
Share the current time

Request:

```python
[
  {
    "day": "string",
    "hour": "number",
    "minute": "number"
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
