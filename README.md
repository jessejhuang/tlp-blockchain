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




###DATA FORMAT
# Citi Blockchain Project
Hey Baria, Braden and Cory! If we decide on using python, this is a repo we could use. It uses Travis CI, which tests the project's build with each pull request or push to Github.


### Setup Info
Apologies if this is redundant or unneccesary, but if you haven't worked with virtualenv before, here's all you have to do to get all the repo's dependencies without screwing with your computer:

- pip install --upgrade virtualenv
- virtualenv -p python3 venv
- source venv/bin/activate
- pip install -r requirements.txt

I've added a simple example test, and you can run all tests on your local machine with the command "pytest". To display test code coverage, run pytest --cov src from citi-blockchain-project/


###DATA FORMAT INFO:

'get("url/print")''

returns a json object structured as below...there are only 3 keys to the returned json (chain, last_hash, and peers)

'{
     'chain': #a list of dictionaries where each dictionary represents one check transaction
                 [
                 {"nonce\": 0,
                 "prev_hash\": \"00000000\",
                 "sender\": null,
                 "check_number\": null,
                 "recipient\": null,
                 "amount\": null,
                 "timestamp\": \"1532710266.587261\",
                 "hash\": \"db5d1b22c1448e9880af063c594ebdf0d33004430ca62e9f72c1170026166e9b\"}"
                   }
                   ,
                  {
                  "nonce\": 124124,
                 "prev_hash\": \"db5d1b22c1448e9880af063c594ebdf0d33004430ca62e9f72c1170026166e9b",
                 "sender\": Cory,
                 "check_number\": 48034871,
                 "recipient\": Baria,
                 "amount\": 25.33,
                 "timestamp\": \"1532710995.587261\",
                 "hash\": \"f2h83hb22c1443io2f82ht083c594ebdf038hf283h823hfieh20838hgg280j2920b\"}"
                  }
                  ,
                  ...
                  ]
                  ,

    'last_hash': f2h83hb22c1443io2f82ht083c594ebdf038hf283h823hfieh20838hgg280j2920b
     ,

     'peers': [url, url2, url3, url4,...]
}'



---------------------------------------------------------

/add    adds a new block to one node, which is then shared to all connected peers using gossip protocol
requires a data json to be passed in representing the new block and what nodes it has been shared to.

'data = {'block':
              {'sender':'cory',
               'recipient':'baria',
               'check_number':12345,
               'amount':12.33
               }
               ,
       'seen_nodes':[]
       }
'

'post("url/add",json=data)'

#making this call automatically distributes the new block to all other connected nodes, and begins validating it on all
#recieving nodes. the first node to complete validation will then alert the other nodes that the block has been validated and
#they will add it to their chain


I believe that these are the only two methods that need to be made through the front end, all other methods and routes are
handled by the backend.