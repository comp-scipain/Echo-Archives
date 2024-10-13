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
