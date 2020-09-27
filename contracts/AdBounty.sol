pragma solidity ^0.6.6;

// SPDX-License-Identifier: MIT
contract AdBounty {
    // one reward
    uint256 viewThreshold;
    uint256 paymentAmount;
    address payable buyer;
    address payable seller;
    uint256 startTimeSec;
    uint256 durationSec;
    string youtubeId;
    string state;

    constructor(
        uint256 _viewThreshold,
        uint256 _paymentAmount,
        address payable _buyer,
        address payable _seller,
        uint256 _startTimeSec,
        uint256 _durationSec,
        string memory _youtubeId
    ) public {
        viewThreshold = _viewThreshold;
        paymentAmount = _paymentAmount;
        buyer = _buyer;
        seller = _seller;
        startTimeSec = _startTimeSec;
        durationSec = _durationSec;
        youtubeId = _youtubeId;
        state = "PENDING";
    }

    function validate() public {
        require(msg.sender == buyer);
        state = "ACTIVE";
    }

    function checkState() public view returns (string memory) {
        return state;
    }

    function mockCallback() public {}
}
