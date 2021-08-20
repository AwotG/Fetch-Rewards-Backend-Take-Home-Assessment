# Fetch Rewards Backend Engineer Take Home Assessment

## Introduction
This is based on the prompt and instructions found in the PDF provided `Fetch-Rewards-BE-Instructions.pdf`.

### Assumptions and restrictions I made:

### Overall:
1. We are only dealing with one user, and they'll have multiple payers.
2. We will need to keep track of all transactions (this includes adding and subtracting points). A transaction is based 
   on when the platform adds or removes points, NOT when the payer actually makes the points live (i.e. they provide a timestamp
   in the add points sections telling us when the points will be available)
3. Points added to account will be timestamped for the date that the points were issued to user NOT when they were submitted to 
   us, the platform. This is important to note, because of next point
4. When points are to be redeemed, they must be redeemed in payer order that the points were issued to user (based on timestamp)
   NOT when submitted to the platform.

### Specific Routes Breakdown
1. Add Transactions Route: 
    - Assumes that we can only ADD points
    - timestamp and payer must be included
    - Should return available balance, broken down by payers 
    
2. Get Balance Route
    - Will return the same as Add Transaction route, total balance broken down by payers
    
3. Redeem Points Route
    - Will return error message if user does not have enough points and display what the amount requested was
      and the users actual sum of points (total points, not broken down by payer)
    - If user has enough points, will return the points subtracted, broken down by payer

4. Transactions History Route
   - Wasn't included in prompt, but this is a more convenient way to validate that transactions happen in order
   - Returns list of all transactions executed. This is based on when actually processed on the platform. i.e. if
     points added to platform, this counts as a transaction at that instance NOT from the timestamp provided from payer saying
     when the points will be active.
     
To test these and to get a better understanding of the models and routes, there is a [Swagger UI](https://swagger.io/solutions/api-documentation/)
that will be available when you run the server. Refer to installation instructions.

**Using the Swagger UI will allow you to directly test the API in the browser!**

### Implementation

1. Python 3.6+
2. Python's [FastAPI](https://fastapi.tiangolo.com/) rest framework
3. Local development server packaged with FastAPI
4. Data using in-memory data structures

## Installation


```bash
#In terminal or CLI, in root directory of project

python3 -m venv venv

source ./venv/bin/activate

pip isntall -r requirements.txt
```

## Usage

```
#In terminal or CLI, in root directory of project

uvicorn PointsSystem:app --reload 
```
**For documentation, it'll be `base_url/docs`. If you're not setting your own port, most likely the url will be**
`http://127.0.0.1:8000/docs#/`

## Tests
Tests are run using Pythons PyTest. 

```bash
#In terminal or CLI, in root directory of project
pytest Tests.py
```

## Notes and limitations
1. Testing is only low level, not at the API level. This is because I spent the majority of my time on the lower level
   and ran out of time (I put a hard limit at 5 hours for this project).
   
2. Data is in memory, and uses a Priority Queue for figuring out order on what to spend, a simple list to track all transactions
   and simple dictionary to keep a running total of available points broken down by payer. This is fine for a quick solution,
   but a simple database like sqlite would be perfect for this
3. In order to reset data, you need to restart the server
4. More data modeleing should have been added, for more explicit understanding (i.e. transactions data, priority queue data etc)
5. Doesn't take into account multiple users, data structured assuming just one. 
6. Class that handles everything should be broken up, but figured it was fine for a quick prototype
7. Big thing for testing, dependency injection should be used so that testing is easier. 
