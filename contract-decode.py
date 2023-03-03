from web3 import Web3
from evmdasm import EvmBytecode

address = "0x7F62c957151810cD743e5707465F4937422300cC" # Light 90 day smart contract

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))


# Decode function because we don't have the ABI
# Link: https://louisabraham.github.io/articles/no-abi.html

from evmdasm import EvmBytecode

bytecode = web3.eth.get_code(address)

opcodes = EvmBytecode(bytecode).disassemble()

hashes = set()
for i in range(len(opcodes) - 3):
    if (
        opcodes[i].name == "PUSH4"
        and opcodes[i + 1].name == "EQ"
        and opcodes[i + 2].name == "PUSH2"
        and opcodes[i + 3].name == "JUMPI"
    ):
        hashes.add(opcodes[i].operand)
hashes = list(hashes)

import requests
from tqdm import tqdm
from time import sleep
from json import JSONDecodeError

signatures = {}


def getSignature(hash):
    global signatures
    r = requests.get(
        "https://www.4byte.directory/api/v1/signatures/?hex_signature=" + hash
    )
    try:
        res = r.json()["results"]
        res.sort(key=lambda r: r["created_at"])
        signatures[hash] = [m["text_signature"] for m in res]
        return True
    except JSONDecodeError:
        return False


for hash in tqdm(hashes):
    while not getSignature(hash):
        sleep(1)

abi = []
functions = []
for h, sign in signatures.items():
    if not sign:
        print("No match found for", h)
        continue
    if len(sign) > 2:
        print(f"Multiple matches found for {h}:", ", ".join(sign))
    functions.append(sign[0])
    name, sign = sign[0].split("(")
    args = sign[:-1].split(",")
    if args == ['']: # ''.split() returns ['']
        args = []
    abi.append(
        {
            "type": "function",
            "name": name,
            "inputs": [{"type": t} for t in args],
            "outputs": [{"type": "unknown"}],
        },
    )

print("Initialized interface with functions:")
for f in sorted(functions):
    print("   ", f)

web3.codec._registry.register_decoder("unknown", lambda b: bytes(b.getbuffer()))
contract = web3.eth.contract(
    address=address,
    abi=abi,
)

from private import wallet_address, private_key

from web3.middleware import geth_poa_middleware
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

Chain_id = web3.eth.chain_id
caller = wallet_address

#print("calling emergencyWithdraw:", contract.functions.emergencyWithdraw().call())

# Initialize address nonce
nonce = web3.eth.getTransactionCount(caller)

# Call your function

call_function = contract.functions.emergencyWithdraw().buildTransaction({"chainId": Chain_id, "from": caller, "nonce": nonce, 'gas': 200000, 'gasPrice': web3.toWei('5', 'gwei') })

# Sign transaction
signed_tx = web3.eth.account.sign_transaction(call_function, private_key=private_key)

# Send transaction
send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Wait for transaction receipt
tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)
print(tx_receipt) # Optional
