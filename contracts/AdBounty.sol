pragma solidity ^0.6.6;
import "@chainlink/contracts/src/v0.6/ChainlinkClient.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

// SPDX-License-Identifier: MIT
contract AdBounty is ChainlinkClient {
    // one reward
    uint256 viewThreshold;
    uint256 paymentAmount;
    address payable buyer;
    address payable seller;
    uint256 startTimeSec;
    uint256 durationSec;
    string externalUrl;
    string state;
    bool paymentMade = false;

    // Oracle / Job listed here:
    //https://market.link/jobs/dbdf3273-aaf3-4b70-8fd1-6d55e856da24
    address ORACLE_ADDRESS = 0x1b666ad0d20bC4F35f218120d7ed1e2df60627cC;
    string constant JOBID = "2d3cc1fdfede46a0830bbbf5c0de2528";
    uint256 private constant ORACLE_PAYMENT = 5 * 10**16; // .05 LINK
    uint256 MIN_LINK_ALLOWED = 1;

    constructor(
        uint256 _viewThreshold,
        uint256 _paymentAmount,
        address payable _buyer,
        address payable _seller,
        uint256 _durationSec,
        string memory _externalUrl
    ) public {
        viewThreshold = _viewThreshold;
        paymentAmount = _paymentAmount;
        buyer = _buyer;
        seller = _seller;
        startTimeSec = 0;
        durationSec = _durationSec;
        externalUrl = _externalUrl;
        state = "PENDING";
    }

    function validate() public {
        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
        require(
            address(this).balance > paymentAmount,
            "Insufficient Ether provided to contract"
        );
        require(
            link.balanceOf(address(this)) >= MIN_LINK_ALLOWED,
            "Insufficient Link provided to contract"
        );
        require(msg.sender == buyer);
        state = "ACTIVE";
        startTimeSec = block.timestamp;
    }

    function getState() public view returns (string memory) {
        return state;
    }

    function getBuyer() public view returns (address) {
        return address(buyer);
    }

    function getSeller() public view returns (address) {
        return address(seller);
    }

    function getExternalUrl() public view returns (string memory) {
        return externalUrl;
    }

    function mockCallback(uint256 viewCount) public {
        viewCountHandler(viewCount);
    }

    // This uses an oracle to
    // access our external adapter.
    function requestViewCount() public {
        // require(msg.sender == buyer);
        // newRequest takes a JobID, a callback address, and callback function as input
        Chainlink.Request memory req = buildChainlinkRequest(
            stringToBytes32(JOBID),
            address(this),
            this.oracleFulfill.selector
        );
        req.add("get", externalUrl);
        req.add("path", "viewCount");
        sendChainlinkRequestTo(ORACLE_ADDRESS, req, ORACLE_PAYMENT);
    }

    function oracleFulfill(bytes32 _requestId, uint256 viewCount)
        public
        recordChainlinkFulfillment(_requestId) // only requesting oracle can fulfill
    {
        viewCountHandler(viewCount);
    }

    function viewCountHandler(uint256 viewCount) public {
        if (startTimeSec + durationSec < block.timestamp || paymentMade) {
            state = "EXPIRED";
            refund();
        } else {
            if (viewCount > viewThreshold) {
                seller.transfer(paymentAmount);
                state = "EXPIRED";
                paymentMade = true;
                refund();
            }
        }
    }

    // Contract is done, refund
    // any remaining tokens / eth to buyer
    function refund() public {
        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());

        require(
            link.transfer(buyer, link.balanceOf(address(this))),
            "Unable to refund chainlink"
        );
        seller.transfer(address(this).balance);
    }

    function stringToBytes32(string memory source)
        private
        pure
        returns (bytes32 result)
    {
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
            return 0x0;
        }
        assembly {
            // solhint-disable-line no-inline-assembly
            result := mload(add(source, 32))
        }
    }

    // fallback function 
    fallback () external payable {
    }
}
