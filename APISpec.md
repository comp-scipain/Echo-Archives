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
