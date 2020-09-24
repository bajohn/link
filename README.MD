
Repo for Chainlink Hackathon 
https://www.reddit.com/r/dataisbeautiful/comments/ip69jc/oc_container_ship_imports_into_the_united_states/
https://chainlink-hackathon.devpost.com/?ref_content=featured&ref_feature=challenge&ref_medium=discover

Chainlink->AWS Link
https://www.reddit.com/r/LINKTrader/comments/7ou4p2/install_chainlink_node_on_amazon_aws_free_tier/

#chainlink

# Repo directories
- `/demo_python` Various python scripts I used to learn how to interact with web3. To run these scripts:
    - `cd demo_python`
    - pipenv install
    - Insert private key and corresponding account address into `sensitive.py` at the root directory. You can use `sensitve_example.py` as a model.
    - Demo scripts are prefixed with an integer. Run via `pipenv run python {script name}`, for example `pipenv run python 5_contract_send_eth_main.py`
# Repo instructions
TODO: clean this up! Currently treating this like a notes section.

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
    
# Ideas
## Advertising contract execution app (AdChain)
- Alice the advertiser wants to advertise a product, and knows Chris the content creator has a solid following on Youtube.
- Alice wants to buy time on Chris's video. She wants the ad to be part of the video, such as 
Chris saying "Thanks to our sponsor Alice, check her out at alicesplace.com"
- Chris makes a video with Alice's Ad in it.
- Alice and Chris use AdChain to create a contract, which specifies the terms of payment guaranteed by the blockchain. For example:
    - Payment of $10 is made when views hit 1,000
    - Payment of $100 is made when views hit 10,000
    - Payment of $1000 is made when views hit 100,000. Therefore, the maximum payment in this contract is $1110.
- Alice and Chris have their own Ethereum wallet addresses. In order for the contract to execute, Alice must approve 
Chris's video, verifying that the ad is in the video and is up to her standards. FUTURE WORK- this step could be automated
with some auto-verification via some kind of bot that searches for keywords, etc.
- The contract is funded by Alice (?), who may need some staking to fund several of these contracts.
- Chainlink uses an Oracle node to watch the viewcount, and when it passes the set amount of views, the contract executes.
- Could also use an oracle to determine whether a video is still online, but this isn't explicitly needed!
Is that it?

# To build:

- Sample contract 1 
✅ Done via `5_contract_send_eth_main.py`. Note- need to sign all transactions and send raw in Infura!.
    - Constructor accepting
        - Two wallet addresses, for buyer and seller
    - A variable `sensorValue` that changes via an externally accessible getter/setter
    - A hardcoded constant value `payoutThreshold`, 
    - A getter/setter like the `StoreValue` we've already used
    - A boolean `hasPaidOut` so payout only happens once
    - The `sensorValue` setter checks the `payoutThreshold` and `hasPaidOut` 

- Sample contract 2 (optional stepping stone)
    - Use sample contract 1, except sensorvalue pulls in something real like wall clock time, paying out when
    the clock passes a hardcoded time.

- Actual contract
    - Constructor accepting:
        - the two wallet addresses, for buyer and seller
        - a video link
        - an array of unmet targets. Something like `[views: payout]`, like
        ```
        [
            1000: 10,
            10000: 100,
            100000: 1000,
        ]
        ```
    - A video verification callback, requiring the address of ad buyer. 
        - The buyer could fund the contract here, funding the maximum amount of payout
    - A GET function to retrieve the video URL
    - A GET function to retrieve the met targets
    - A GET function to retrieve the unmet targets





# Dead ideas:
## Quiz game
- Dealer chooses a
- Dealer chooses a question, like "Who won the Super Bowl last year?", from a list of 3-5 questions. These questions/answers would need to come from a pool of quiz questions, this all relies on the existence of this pool.
- They would want to choose something they think they know but think others don't know.
- Dealer enters their answer
- The question is presented to the other players
- They choose their answer (bonus points if they can guess the dealer's wrong answer?)
- All is revealed. Dealer should get extra negative points for not knowing something they said they knew

Turns out source of truth for such a quiz game would be really hard! And not too interesting of a problem for Chainlink.

## Shipping contract completion app
### Concept:
- Shipping contract completion
- Contract is created by an item being scanned at a warehouse
- Contract requires that an item be delivered by x date, and y location
- Source of truth for GPS is the (web)app, source of truth for the time is the local time. A "real" application would need some kind of verification especially on the GPS part. A native app would probably be necessary.
- Can Chainlink use a device's GPS as a Chainlink Node?! Then we're golden!
- When device is brought within time/position window, it fulfills the contract, completing the transaction.
- Best case would be the money is held in escrow by Chainlink's infrastructure, released to the deliverer when completed, refunded to consumer if the window passes.


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
- Integrate with credentialed API such as Youtube
- Figure out how polling works, aka how to trigger on an API event without constantly polling.

## Notes
