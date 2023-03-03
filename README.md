# Emergency Withdrawal

## Instructions

1) Install Python
2) [Optional] Setup python venv environment
3) pip install -r requirements
4) Set your wallet address here: https://github.com/bl4z3ng41n/emergency-withdraw/blob/main/private.py#L1
5) Set your private key here: https://github.com/bl4z3ng41n/emergency-withdraw/blob/main/private.py#L2
6) [Optional] Set the contract (MasterChief) address here: https://github.com/bl4z3ng41n/emergency-withdraw/blob/main/contract-decode.py#L4
7) python contract-decode.py

## Errors

### No stakes found for user

```
raise ContractLogicError(response['error']['message'])
web3.exceptions.ContractLogicError: execution reverted: No stakes found for user
```

Explanation: This is when you call a function, but it does not have a signed transaction. See this line https://github.com/bl4z3ng41n/emergency-withdraw/blob/main/contract-decode.py#L96

### Requesting before lock time

```
raise ContractLogicError(response['error']['message'])
web3.exceptions.ContractLogicError: execution reverted: Requesting before lock time
```

Explanation: You need to wait the lock time of the pool to be able to use this fonction. If there is a flaw or another mechanism, then it may be possible to change the lock time, and call that function again.

### The field extraData is 97 bytes, but should be 32.

```
web3.exceptions.ExtraDataLengthError: The field extraData is 97 bytes, but should be 32. It is quite likely that you are connected to a POA chain. Refer to http://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority for more details. The full extraData is: [...]
```

Solution: https://github.com/bl4z3ng41n/emergency-withdraw/blob/main/contract-decode.py#L91

### KeyError: 'baseFeePerGas'

```
return self.__dict__[key]  # type: ignore
KeyError: 'baseFeePerGas'
```
Solution: Add gas parameters at line https://github.com/bl4z3ng41n/emergency-withdraw/blob/main/contract-decode.py#L103


### transaction underpriced

```
    raise ValueError(response["error"])
ValueError: {'code': -32000, 'message': 'transaction underpriced'}
```
Explanation: This is mostly due to the gas parameters being too low at line https://github.com/bl4z3ng41n/emergency-withdraw/blob/main/contract-decode.py#L103

## FAQ

Q.1 Could this code be simplified?  
A.1 Yes. See question 2 for an example with react. Same logic can be done with Python.

Q.2 Could it be done with react (web3.js)?  
A.2 Yes. See:

 ![react_poc.jpg](https://github.com/bl4z3ng41n/emergency-withdraw/blob/main/react_poc.jpg)

## Disclaimer
The readers following these instructions accept all risks. The author share this information to educate the crypto space on how to call the emergencyWithdraw function from MasterChef look-like contract.
