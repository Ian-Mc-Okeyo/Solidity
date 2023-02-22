from solcx import compile_standard, install_solc
import json
from web3 import Web3
#read the file
with open("../contracts/MyContract.sol", "r") as file:
    my_cotract_file = file.read()


#compile solidity
#install_solc('0.8.0') - to be run ones to install the required version
print("Compiling contract...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"../contracts/MyContract.sol":{"content":my_cotract_file}},
        "settings": {
            "outputSelection": {
                "*":{
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version = "0.8.0",
)

#write to a json file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#get the bytecode
bytecode = compiled_sol["contracts"]["../contracts/MyContract.sol"]["MyContract"]["evm"]["bytecode"]["object"]

#get the abi
abi = compiled_sol["contracts"]["../contracts/MyContract.sol"]["MyContract"]["abi"]
print("Successfully Compiled!")

#for connecting to ganache
print("Connecting to Block Chain network...")
# to ganache w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/4ff51484963a4a2da25ac6b1d02e8331")) #to infura goerli
print("Connected")
chainId = 5 #for goerli. ganache is 1337

my_address = '0x5CAc5A383CE94C196945E55361891ED6A88Fd6Ea'
privateKey = '0x3c202d7b51276c160509262af18b9ec390d58876f7c9f111ef95763e68f26ee6' #don not hardcode. Use environment variables

#create the contract in python
MyContract = w3.eth.contract(abi = abi, bytecode = bytecode)
# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
#1.Build a transaction
#2.Sign a transaction
#3. Send a transaction

print("Deploying contract...")
#1
transaction = MyContract.constructor().buildTransaction({"chainId":chainId, "from":my_address, "nonce":nonce,  "gasPrice": w3.eth.gas_price})
#2
signed_txn = w3.eth.account.sign_transaction(transaction, private_key = privateKey)
#3
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#wait for the transaction receipt
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Successfully Deployed!")

#working with the contract,  needs:
#contract Address
#contract ABI

my_contract = w3.eth.contract(address = txn_receipt.contractAddress, abi=abi)

#interacting with the contract can be in two ways:
#1.Call -> simulate making the call and getting the value. Does not make a state change to the contract
#2.Transact -> Actually make a state change to the contract

print(my_contract.functions.retrieveData().call()) #calling a function makes no state change. Retrieve data in this case is a view function

print("Adding a new person to the contract...")
#to make a call function that actually changes state, we have to make a transaction
add_person_txn = my_contract.functions.addPerson(23, "IAN").buildTransaction({"chainId": chainId, "from": my_address, "nonce":nonce+1, "gasPrice": w3.eth.gas_price})

signed_add_person_txn = w3.eth.account.sign_transaction(add_person_txn, private_key = privateKey)
add_person_txn_hash = w3.eth.send_raw_transaction(signed_add_person_txn.rawTransaction)
add_person_txn_receipt = w3.eth.wait_for_transaction_receipt(add_person_txn_hash)
print("Successfully added the person!")

#getting the person's fav_number
person = my_contract.functions.getPerson(0).call()
print(f'New Person: Name:{person[1]}, FavNumber:{person[0]}')

#access-tkn: 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