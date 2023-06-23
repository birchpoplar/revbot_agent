"""A templated Fixie agent!

Fixie docs:
    https://docs.fixie.ai

Fixie agent example:
    https://github.com/fixie-ai/fixie-examples
"""

import fixieai
import requests
import json

base_url = 'http://127.0.0.1:5000'
headers = {'Content-Type': 'application/json'}

BASE_PROMPT = """This agent takes input about customers, contracts, revenue recognition policies and invoices and returns rigorous financial statement data."""

FEW_SHOTS = """
Q: Add a customer named Meta
Thought: I need to add a customer named Meta and get the ID
Ask Func[addcustomer]: Meta
Func[addcustomer] says: Meta has ID 4
A: Customer Meta was added with ID 4

Q: Let's stuff in a new customer named Alpha
Thought: I need to add a customer named Alpha and get the ID
Ask Func[addcustomer]: Alpha
Func[addcustomer] says: Alpha has ID 5
A: Customer Alpha was added with ID 5

Q: Let's add a contract for customer Alpha in month 5
Thought: I need to add a contract for customer Alpha (that has integer ID 6) with booked month 5 and get the contract ID
Ask Func[addcontract]: { "customer_id": 6, "booked_month": 5 }
Func[addcontract] says: Contract ID 1 was added for customer Alpha with booked month 
A: Contract ID 1 was added for customer Alpha with booked month 5

Q: Let's add a new customer named Beta and a contract for customer Beta starting in month 6
Thought: I need to add a customer named Beta and get the ID, and then add the contract for customer Beta with booked month 6 and get the contract ID
Ask Func[addcustomer]: Beta
Func[addcustomer] says: Beta has ID 7
Ask Func[addcontract]: { "customer_id": 7, "booked_month": 6 }
Func[addcontract] says: Contract ID 2 was added for customer Beta with booked month 6
A: Customer Beta was added with ID 7 and Contract ID 2 was added for customer Beta with booked month 6
"""

agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)

@agent.register_func
def addcustomer(query: fixieai.Message) -> str:
    """Add a customer to the database."""
    data = {'name': query.text} 
    response = requests.post(base_url + '/customers', json=data, headers=headers)
    return response.text

@agent.register_func
def addcontract(query: fixieai.Message) -> str:
    """Add a contract to the database."""
    data = json.loads(query.text)
    response = requests.post(base_url + '/contracts', json=data, headers=headers)
    return response.text

