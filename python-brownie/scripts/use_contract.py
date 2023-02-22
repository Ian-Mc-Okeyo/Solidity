from brownie import MyContract, accounts

def use_contract():
    my_contract = MyContract[-1] #getting the latest contract index -1
    print(my_contract)
    print(my_contract.retrieveData())
    print(my_contract.getPerson(0))

def main():
    use_contract()

# etherium test network
#run brownie run scripts/use_contract.py --network goerli