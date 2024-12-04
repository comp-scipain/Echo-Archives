Sarah, an Engineering Manager at Cloud Corp, needs to submit quarterly performance reviews for her 15-person team before promotion discussions begin next month. She gives performance reviews for all of her employees using our api.

Mike from HR needs to track why Backend Engineering has had 3 demotions in the past quarter while Frontend Engineering is seeing consistent promotions. He checks the reviews to get to the bottom of this

Jennifer, the CTO, wants metrics on which departments have the highest performing engineers to inform hiring and training strategies. She uses the metrics provided by the reviews endpoints to make her hiring decisions

David, a Tech Lead, needs to document that his junior developer has improved from a 2 to a 4 rating after completing a performance improvement plan. He updates his improvements using our database.

Lisa in Platform Engineering wants to verify her performance history before discussing a potential promotion with her manager. She logs into her performance portal where all of her rating come up and she is mildly surprised.

Alex, Director of Data Science, needs to compare performance scores across his teams to ensure fair review practices



Exceptions:

-Employee ID not found in database

In this case, the system will return an error and list similar employee names that might be a match, along with a prompt to verify the correct ID with HR.

-Manager forgets to input complete review

In the case that a manager submits an incomplete review (e.g., missing performance score or feedback), they can submit additional information through a supplement API endpoint that updates the existing review.

-User inputs invalid performance score

In this case, the system will return an error indicating that performance scores must be between 1-5 integers.

-Manager creates a review that already exists for that period

In this case, the system will return the existing review and alert the manager of the duplicate. If this is an intended update, the manager can use the update endpoint instead.

-System can't connect to HR database

In this case, the system will show an error message with potential causes and fixes. If it's a connection issue, it will prompt to check VPN connectivity and network status.

-User enters invalid salary adjustment

In this case, the system will return an error indicating that salary adjustments must be within approved percentage ranges.

-User enters invalid employee level

In this case, the system will return an error indicating that employee levels must be within the defined range (-2 to 12).

-User enters invalid review date

In this case, the system will return an error indicating that review dates must be within the current review period.