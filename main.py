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

Q: What are all the customer names in the database?
Thought: I need to get all customers and list them
Ask Func[getcustomers]: Get the names of all the customers in the database
Func[getcustomers] says: Here's a list of the customer names
A: Here are the customer names

Q: Let's add a contract for customer Alpha in month 5
Thought: I need to add a contract for customer Alpha with booked month 4 and get the contract ID
Ask Func[getcustomerbyname]: { "name": "Alpha" }
Func[getcustomerbyname] says: ID 6
Ask Func[addcontract]: { "customer_id": 6, "booked_month": 5 }
Func[addcontract] says: Contract ID 1 was added for customer Alpha with booked month 
A: Contract ID 1 was added for customer Alpha with booked month 5

Q: What are the details of customer with ID 6?
Thought: I need to get the details of customer with ID 6
Ask Func[getcustomerbyid]: { "id": 6 }
Func[getcustomerbyid] says: Here are the details of customer with ID 6
A: Customer with ID 6 has name Alpha and two contracts with IDs 4 and 5

Q: Let's add a new customer named Beta and a contract for customer Beta starting in month 6
Thought: I need to add a customer named Beta and get the ID, and then add the contract for customer Beta with booked month 6 and get the contract ID
Ask Func[addcustomer]: Beta
Func[addcustomer] says: Beta has ID 7
Ask Func[addcontract]: { "customer_id": 7, "booked_month": 6 }
Func[addcontract] says: Contract ID 2 was added for customer Beta with booked month 6
A: Customer Beta was added with ID 7 and Contract ID 2 was added for customer Beta with booked month 6

Q: Contract 1 for customer Alpha has a revenue segment with name of License, type Product, a total value of 12000, starting 2 months after the contract start date, and lasting 12 months with monthly invoicing that starts at same time as revenue.
Thought: I need to add a revenue segment for contract 1 for customer Alpha with name License, type Product, a total value of 12000, starting 2 months after the contract start date, and lasting 12 months with monthly invoicing that starts same time as revenue.
Ask Func[addrevenuesegment]: { "contract_id": 1, "name": "License", "type": "Product", "amount": 12000, "delay_rev_start_mths": 2, "delay_inv_from_rev_mths": 0, "length_rev_mths": 12, "invoice_schedule": "Monthly" }
Func[addrevenuesegment] says: Revenue segment ID 1 was added for contract 1 for customer Alpha with name License, type Product, a total value of 12000, starting 2 months after the contract start date, and lasting 12 months with monthly invoicing that starts same time as revenue.
A: Revenue segment ID 1 was added for contract 1 for customer Alpha with name License, type Product, a total value of 12000, starting 2 months after the contract start date, and lasting 12 months with monthly invoicing that starts same time as revenue.

Q: What are all the revenue segments for contract 1 for customer Alpha?
Thought: I need to get all revenue segments for contract 1 for customer Alpha and list them
Ask Func[getrevenuesegmentsforcontract]: { "contract_id": 1 }
Func[getrevenuesegmentsforcontract] says: There are the revenue segments: names are Pilot 1, License, and they have amounts of 10,000 and 12,000 and timelines of 3 and 12 months
A: Here are the revenue segments: names are Pilot 1, License, and they have amounts of 10,000 and 12,000 and timelines of 3 and 12 months

Q: can we clean out the full database please
Thought: I need to delete all customers, contracts, revenue segments and invoices
Ask Func[cleardatabase]: Please delete
Func[cleardatabase] says: Database cleared
A: Database cleared

Q: Can you generate the dataframe from the database?
Thought: I need to generate the dataframe from the database
Ask Func[populatedataframe]: Please generate the dataframe
Func[populatedataframe] says: Here is the dataframe
Thought: I need to convert this dataframe to a CSV and display as a table
A: Here is the dataframe in table format
"""

agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)

# Customer functions

@agent.register_func
def addcustomer(query: fixieai.Message) -> str:
    """Add a customer to the database."""
    data = {'name': query.text} 
    response = requests.post(base_url + '/customers', json=data, headers=headers)
    return response.text

@agent.register_func
def getcustomers(query: fixieai.Message) -> str:
    """Get the names and IDs of all customers from the database."""
    response = requests.get(base_url + '/customers', headers=headers)
    data = json.loads(response.text)
    customers = data['data']
    names = ''
    for customer in customers:
        names += customer['name'] + ', '
    print(names)
    return names

@agent.register_func
def getcustomerbyname(query: fixieai.Message) -> str:
    """Get customer id by name."""
    data = {'name': json.loads(query.text)['name']}
    print(data)
    response = requests.get(base_url + '/customers/name/' + str(data['name']), json=data, headers=headers)
    customer_id = json.loads(response.text)['data']['id']
    return 'The customer ID is ' + str(customer_id)

@agent.register_func
def getcustomerbyid(query: fixieai.Message) -> str:
    """Get customer name by ID."""
    data = {'id': json.loads(query.text)['id']}
    response = requests.get(base_url + '/customers/id/' + str(data['id']), json=data, headers=headers)
    return 'Customer name is ' +str(json.loads(response.text)['name'])

# Contract functions

@agent.register_func
def addcontract(query: fixieai.Message) -> str:
    """Add a contract to the database."""
    data = json.loads(query.text)
    response = requests.post(base_url + '/contracts', json=data, headers=headers)
    return response.text

@agent.register_func
def getcontracts(query: fixieai.Message) -> str:
    """Get all contracts from the database."""
    response = requests.get(base_url + '/contracts', headers=headers)
    return json.loads(response.text)

@agent.register_func
def getcontractsforcustomer(query: fixieai.Message) -> str:
    """Get all contracts for a customer from the database."""
    data = {'customer_id': json.loads(query.text)['customer_id']}
    response = requests.get((base_url + '/customers/id/' + str(data['customer_id']) + '/contracts'), headers=headers)
    if response.text == '[]':
        return 'No contracts for this customer'
    else:
        ids = [item['id'] for item in json.loads(response.text)]
        return 'The contracts for customer with ID are ' + str(ids)

# Revenue segment functions

@agent.register_func
def addrevenuesegment(query: fixieai.Message) -> str:
    """Add a revenue segment to the database."""
    data = json.loads(query.text)
    response = requests.post(base_url + '/revenuesegments', json=data, headers=headers)
    return response.text

@agent.register_func
def getrevenuesegments(query: fixieai.Message) -> str:
    """Get all revenue segments from the database."""
    response = requests.get(base_url + '/revenuesegments', headers=headers)
    return json.loads(response.text)

@agent.register_func
def getrevenuesegmentsforcontract(query: fixieai.Message) -> str:
    """Get all revenue segments for a contract from the database."""
    data = {'contract_id': json.loads(query.text)['contract_id']}
    response = requests.get((base_url + '/contracts/id/' + str(data['contract_id']) + '/revenuesegments'), json=data, headers=headers)
    if response.text == '[]':
        return 'No revenue segments for this contract'
    else:
        names = [item['name'] for item in json.loads(response.text)]
        amounts = [item['amount'] for item in json.loads(response.text)]
        timelines = [item['length_rev_mths'] for item in json.loads(response.text)]
        return 'There are the following revenue segments: names are ' + str(names) + ', and they have amounts of ' + str(amounts) + ' and timelines of ' + str(timelines)

# Other functions

@agent.register_func
def cleardatabase(query: fixieai.Message) -> str:
    """Clear the database."""
    response = requests.delete(base_url + '/clear_database', headers=headers)
    return response.text

# Populate dataframe

@agent.register_func
def populatedataframe(query: fixieai.Message) -> str:
    """Populate the dataframe."""
    response = requests.get(base_url + '/dataframe', headers=headers)
    return response.text