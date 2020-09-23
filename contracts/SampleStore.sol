pragma solidity ^0.5.16;
// SPDX-License-Identifier: MIT
contract SampleStore {

    uint256 number;

    function store(uint256 num) public {
        number = num;
    }

    function retrieve() public view returns (uint256){
        return number;
    }



    }
