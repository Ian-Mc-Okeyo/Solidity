from brownie import MyContract, accounts

def test_deploy():
    #arrange
    account = accounts[0]
    #act
    my_contract = MyContract.deploy({"from":account})
    starting_value = my_contract.retrieveData()
    expected_value = 3
    #assert
    assert starting_value == expected_value