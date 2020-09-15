
Repo for Chainlink Hackathon 

https://chainlink-hackathon.devpost.com/?ref_content=featured&ref_feature=challenge&ref_medium=discover

Chainlink->AWS Link
https://www.reddit.com/r/LINKTrader/comments/7ou4p2/install_chainlink_node_on_amazon_aws_free_tier/


# Ideas
## Shipping contract completion app
### Concept:
- Shipping contract completion
- Contract is created by an item being scanned at a warehouse
- Contract requires that an item be delivered by x date, and y location
- Source of truth for GPS is the (web)app, source of truth for the time is the local time. A "real" application would need some kind of verification especially on the GPS part. A native app would probably be necessary.
- Can Chainlink use a device's GPS as a Chainlink Node?! Then we're golden!
- When device is brought within time/position window, it fulfills the contract, completing the transaction.
- Best case would be the money is held in escrow by Chainlink's infrastructure, released to the deliverer when completed, refunded to consumer if the window passes.
### To build:
- Chainlink node living in some python code running independently, providing coordinates as an independent data source.
- Smart contract generator that determines the required time window that is allowed.
- Chainlink protocol calls that convert this smart contract into a Chainlink-specific Request Contract, that (somehow) requires fulfillment by a Chainlink Node running in a deliverer's device. 
- Finally, build a nice visualization demo!



# Dead ideas:
## Quiz game
- Dealer chooses a
- Dealer chooses a question, like "Who won the Super Bowl last year?", from a list of 3-5 questions. These questions/answers would need to come from a pool of quiz questions, this all relies on the existence of this pool.
- They would want to choose something they think they know but think others don't know.
- Dealer enters their answer
- The question is presented to the other players
- They choose their answer (bonus points if they can guess the dealer's wrong answer?)
- All is revealed. Dealer should get extra negative points for not knowing something they said they knew


## TODO
Do this! Send transaction
https://ethereum.stackexchange.com/questions/70240/how-to-send-transaction-with-web3-py