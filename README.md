# Citi Blockchain Project
Hey Baria, Braden and Cory! If we decide on using python, this is a repo we could use. It uses Travis CI, which tests the project's build with each pull request or push to Github. 

### Instructions for Setting up pylint with VSCode
Process may be different for 

### Setup Info
Apologies if this is redundant or unneccesary, but if you haven't worked with virtualenv before, here's all you have to do to get all the repo's dependencies without screwing with your computer:

- pip install --upgrade virtualenv
- virtualenv -p python3 venv
- source venv/bin/activate
- pip install -r requirements.txt

I've added a simple example test, and you can run all tests on your local machine with the command "pytest". To display test code coverage, run pytest --cov src from citi-blockchain-project/

Application Idea: Blockchain solution to combat check fraud
Anytime a client orders a checkbook, Citi adds a record of that check to the blockchain. When the check is cashed, the amount transferred is recorded on the ledger. That way, the only way to submit a fraudulent check is to would be to physically steal it.

On cashing a check:

Attempt to verify that the money is in the person's bank account