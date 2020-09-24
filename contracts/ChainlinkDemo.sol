pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/ChainlinkClient.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

// This contract inherits the ChainlinkClient contract to gain the
// functionality of creating Chainlink requests
contract ChainlinkDemo is ChainlinkClient {
    // Stores the answer from the Chainlink oracle
    uint256 public currentPrice;
    address public owner;

    // Oracle / Job listed here:
    //https://market.link/jobs/dbdf3273-aaf3-4b70-8fd1-6d55e856da24
    address ORACLE_ADDRESS = 0x1b666ad0d20bC4F35f218120d7ed1e2df60627cC;
    string constant JOBID = "2d3cc1fdfede46a0830bbbf5c0de2528";

    uint256 private constant ORACLE_PAYMENT = 5 * 10**16; // .05 LINK

    constructor() public {
        setPublicChainlinkToken(); // notify chainlink network of this contract
        owner = msg.sender;
    }

    function requestEthereumPrice() public onlyOwner {
        // newRequest takes a JobID, a callback address, and callback function as input
        Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(JOBID), address(this), this.fulfill.selector);
        req.add(
            "get",
            "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD"
        );
        req.add("path", "USD");
        req.addInt("times", 100);
        sendChainlinkRequestTo(ORACLE_ADDRESS, req, ORACLE_PAYMENT);
    }

    // fulfill receives a uint256 data type
    function fulfill(bytes32 _requestId, uint256 _price)
        public
        recordChainlinkFulfillment(_requestId) // only requesting oracle can fulfill
    {
        currentPrice = _price;
    }

    // cancelRequest allows the owner to cancel an unfulfilled request
    function cancelRequest(
        bytes32 _requestId,
        uint256 _payment,
        bytes4 _callbackFunctionId,
        uint256 _expiration
    ) public onlyOwner {
        cancelChainlinkRequest(
            _requestId,
            _payment,
            _callbackFunctionId,
            _expiration
        );
    }

    function checkRecordedPrice() public view onlyOwner returns(uint256) {
        return currentPrice;
    }

    // Remember to delete this; is duplicated by OnlyOwner import
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    // A helper funciton to make the string a bytes32
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
}
