Bob is new to fitness. He has an idea of what muscles he wants to target but doesn’t know how to. Our API will give him a list of exercises when he specifies what muscles he wants to target.

Jamal has some experience in the weight room but he has been doing the same exact workouts for the past 3 years!! He thinks it’s time to start hitting a new muscle workout to improve his muscle growth. He tells our API the exercises he’s been doing and our api suggests new workouts.

Carlos is a dedicated weight training gym rat. He wants to track the calories burned during his lifting sets. He uses our super cool API to track the calories burned when he inputs exercises, sets, and weight of the weights used.

Sally is an olympian training for the next olympics. She has a feeling that there is a more efficient way to workout her muscles but she doesn’t know what that workout is. She asks our API about a more efficient way to workout and our API delivers. 

As a person who has trouble staying motivated enough to consistently go to the gym. I want to see that I’m making some kind of progress towards my fitness goals and not feel like I’m wasting my time and money at the gym. 

John is white-collar worker who’s free time is extremely valuable. He wants to be able to keep track of his workouts on his days off. So that he can make the most of his very limited free time.

As a person who doesn’t know much about how to accomplish their fitness goals. I want to be able to figure out where I'm going wrong. So I can accomplish my fitness goals.

Charlie wants to train in order to become a professional athlete and wants to keep close track of his workouts and so that he can figure out how he can improve his training regimen.


As a freshman who recently entered college, Chris is new to weightlifting and wants to find ways to optimize his workout with longer breaks or less weight, so that he can maximize his muscle growth. 
As a novice weightlifter, Sean wants to better distribute his workouts to target different muscle groups, so that he develops a more balanced build. 

As a busy college student, Kevin often forgets which workouts he does for each muscle group and wants a way to plan his workouts for the week so that he can make the best use of his limited time at the gym. 

As a professional football player, Leo wants to track his progress and history of the amount of weight he’s able to lift for each of the exercises he does regularly so that he knows if his time at the gym is meeting his goals.


Exceptions:

- Weight machine / workout isn’t in the database

In the case that the user’s machine or workout isn’t in our database, the application will return back an error and list of similar workouts (e.g. target same muscle group), along with a message to create a custom workout.

- User doesn’t input their full workout

In the case that the user forgets to document a part of their workout (e.g. no breaks in between sets), the user can call an API that inputs the missed activity so that the app will make recommendations based on missing data. 

- User inputs an invalid break time

In this case, the app will return an error indicating that the break time must be a positive integer. 

- User creates a custom workout that already exists

In this case, the app will return the existing workout and alert the user that the workout already exists. If the workout is different, then the user can override the response and the custom workout.

- The app can’t connect to database

In this case, the app will show the user an error message with potential causes and fixes. If the app can’t connect to the internet, it will ask the user to check if they’re connected to the internet.

- User enters an invalid weight

In this case, the app will return an error indicating that the weight must be a positive integer. 

- User enters an invalid set number

In this case, the app will return an error indicating that the set number must be a positive integer. 

- User enters invalid reps

In this case, the app will return an error indicating that the reps must be a positive integer. 