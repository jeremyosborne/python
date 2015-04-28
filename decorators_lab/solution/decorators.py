'''
>>> data = '{"username": "oscar", "password": "trashcan", "account": 1234, "amount": 12.03}'
>>> deposit(data)
'OK'
>>> data = '{"username": "oscar", "password": "trash", "account": 1234, "amount": 14.98}'
>>> deposit(data)
'Invalid Password'
>>> data = '{"username": "oscar", "password": "trashcan", "account": 1234, "amount": 4.12}'
>>> withdraw(data)
'OK'
>>> data = '{"username": "oscar", "password": "trashcan", "account": 1235, "amount": 2.54}'
>>> withdraw(data)
'Invalid Account'
>>> data = '{"username": "oscar", "password": "trashcan", "account": 1234}'
>>> balance(data)
'7.91'
>>> data = '{"username": "oscar", "password": "trashcan"}'
>>> balance(data)
'No Account Number Provided'

Hint: that's json data
'''

import json
from decimal import *



account = {
    "username": "oscar",
    "password": "trashcan",
    "account": 1234,
    "balance": Decimal("0.00"),
}



def data_parser(f):
    def parse(j):
        trans = json.loads(j)
        return f(trans)
    return parse

def validate(f):
    def validate(trans):
        if not "account" in trans:
            return 'No Account Number Provided'
        elif trans["password"] != account["password"]:
            return 'Invalid Password'
        elif trans["account"] != account["account"]:
            return 'Invalid Account'
        else:
            return f(trans)
    return validate



@data_parser
@validate
def deposit(transaction):
    global account
    account["balance"] += Decimal(str(transaction["amount"]))
    return 'OK'



@data_parser
@validate
def withdraw(transaction):
    global total
    account["balance"] -= Decimal(str(transaction["amount"]))
    return 'OK'



@data_parser
@validate
def balance(transaction):
    return str(account["balance"])



if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
