
# Ad Bounty 
Repo for Chainlink Hackathon 

https://chainlink-hackathon.devpost.com/

#chainlink

Application is online at:
https://ad-bounty.com/

# Repo directories
- `/frontend` Contains all Angular source code. Run locally (fully functional thanks to lack of CORS :) by running `ng serve` in this directory.
- `/lambdas` Backend API code, written for AWS Lambda
- `/contracts` Main smart contract for this application
- `/terraform` Terraform- manages all cloud infrastructure 
- `/scripts` Deploy script

# Application Flow
- Content creator finds an ad with a suitable payout (x ethereum at y video views).
- Content creator clicks on this offering and states which video will contain the ad, which creates the smart contract.
- Advertiser approves of this contract after seeing the video, and funds the contract with the potential payout.
- An external service monitors the video viewcount via an external adapter included in this repo. When the video passes the given threshold, the service triggers a smart contract function which uses a Chainlink oracle to record the "threshold passing" event into the blockchain, which triggers the payout.
- After a set amount of time, and remaining Ethereum/Link on the contract is returned to the advertiser who funded it originally.

# Complete
- Fully functional web app connected to Metamask
- Backend API, which reads/writes from NoSQL DynamoDB.
- Dynamo Schema
- Smart contract written in Solidity, compilable using Truffle
- Automated smart contract generation and deployment, using templates stored in Dynamo and the compiled contract.
- Fully managed AWS infrastructure, which was used to deploy the frontend/backend/database/etc via Terraform.
- Serverless infrastructure used- the backend uses AWS Lambdas to reply to requests, the frontend is hosted by AWS Cloudfront, and the databse is DynamoDB.
- Stores minimal information about deployed smart contracts by instead instantiating the contract in Web3 using the contract's address and pulling information directly from the chain.
- External adapter (as part of same Lambda API) which integrates with the Youtube Data API to return viewcounts for arbitrary video IDs.  (Try it here, the last bit is the Youtube Video ID https://h8a4i8udc3.execute-api.us-east-1.amazonaws.com/prod/youtube-views/gN-T6NDWQ1g)

# Incomplete
- Off-chain polling mechanism
- Ran into problems with approval/payout mechanism in Solidity
- Automatic contract funding mechanism
- Automated notification that a contract was created and an advertiser can approve/disapprove


# Repo instructions

Installation

- Install solidity 
    ```Solidity compiler 
    brew update
    brew upgrade
    brew tap ethereum/ethereum
    brew install solidity
    ```

-  AngularCLI 
    ```
    npm install -g @angular/cli 
    ```
- Truffle CLI 
    ```
    npm install -g truffle
    ```

- Python
    ```
    pipenv install
    ```

- Deploy backend (warning- this will attempt to deploy a bunch of real AWS infrastructure!)
    ```
    ./scripts/deploy.sh --libs=true
    ```

- Insert youtube API key into AWS secrets manager, secret name `youtube-cred`
    ```
    {
    "api_key": <insert youtube api key>
    }
    ```


## Working 
Create a new contract at 
http://localhost:4200

Or access an existing contract at:
http://localhost:4200/contract/0xd9455befed4a124b0515881806ba159b3966cdbb

✅ Compile contract using truffle / chainlink truffle box
✅ Insert compiled contract into Angular source code
✅ Deploy contract from web3-integrated frontend using Metamask and pure browser Javascript
✅ Trigger contract call to Chainlink Oracle, which pulls from a simple API
✅ Check the result of this API call

## TODO
✅ - Integrate with credentialed API such as Youtube
- Figure out how polling works, aka how to trigger on an API event without constantly polling.

## Notes
