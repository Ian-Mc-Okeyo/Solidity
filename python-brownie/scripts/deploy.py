from brownie import accounts, MyContract, network

def deploy_my_contract():
    # account = accounts.load("first_account") - using my metamask account that i added
    account = get_account()
    my_contract = MyContract.deploy({"from":account})
    print(my_contract.retrieveData())
    txn = my_contract.addPerson(3, "IAN", {"from":account})
    txn.wait(1)
    print(my_contract.getPerson(0))

def get_account():
    if(network.show_active()=="development"): #for the default local network
        return accounts[0]
    else:
        return accounts.add("0x3c202d7b51276c160509262af18b9ec390d58876f7c9f111ef95763e68f26ee6") #private key though should be in in .env

def main():
    deploy_my_contract()

# etherium test network
#brownie run scripts/deploy.py --network goerli

# local network
#brownie run scripts/deploy.py