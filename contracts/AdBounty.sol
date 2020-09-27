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
    bool paymentMade = false;

    constructor(
        uint256 _viewThreshold,
        uint256 _paymentAmount,
        address payable _buyer,
        address payable _seller,
        uint256 _durationSec,
        string memory _youtubeId
    ) public {
        viewThreshold = _viewThreshold;
        paymentAmount = _paymentAmount;
        buyer = _buyer;
        seller = _seller;
        startTimeSec = -1;
        durationSec = _durationSec;
        youtubeId = _youtubeId;
        state = "PENDING";
    }

    function validate() public {
        require(msg.sender == buyer);
        state = "ACTIVE";
        startTimeSec = block.timestamp;
    }

    function checkState() public view returns (string memory) {
        return state;
    }

    function mockCallback(uint256 viewCount) public {
        if (startTimeSec + durationSec < block.timestamp || paymentMade) {
            state = "EXPIRED";
        } else {
            if (viewCount > viewThreshold) {
                seller.transfer(paymentAmount);
                state = "EXPIRED";
                paymentMade = true;
            }
        }
    }
}
