//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MyContract {
    struct People{
        uint favouriteNumber;
        string name;
    }

    People[] public people;

    function addPerson(uint _favouriteNumber, string memory _name) public {
        People memory person  = People(_favouriteNumber, _name);
        people.push(person);

    }

    function getPerson(uint _id) public view returns(uint){
        return (people[_id].favouriteNumber);
    }
}