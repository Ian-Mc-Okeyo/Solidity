// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address=>uint) public AddressToAmountFunded;

    address public owner;
    constructor(){
        owner = msg.sender;
    }

    modifier reqAmount(uint _value){
        require(convert(_value) >= 50**18, "You need to spend more eth");
        _;
    }

    function fund() public payable reqAmount(msg.value) {
        AddressToAmountFunded[msg.sender] += msg.value;
    }

    function getVersion() public view returns(uint){
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e);
        return priceFeed.version();
    }

    function getPrice() public view returns(uint){
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e);
        (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return uint(answer);
    }

    function convert(uint ethAmount) public view returns(uint){
        uint rate = getPrice();
        uint amountInUSD = (rate * ethAmount) / (10**18);
        return amountInUSD;
    }

    modifier onlyOnwner {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOnwner {
        payable(msg.sender).transfer(address(this).balance); //after using the money, it is stored in this cotract and hence can be withdrawn
    }
}