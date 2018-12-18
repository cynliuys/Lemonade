# Lemonade

The  reference pages of PBFT/BFT go here.


## Proposal of our works
* [GoogleDoc](https://docs.google.com/document/d/1ZApj2F91H3XlKshC2FbxyRc39nQODNzGCMPabv3QAhE/edit?fbclid=IwAR0j2m9nXTKY7zaGl7bshuHgs3M6v_-9oztuuhc_9ooqvWoqJfTMNJhpB7E)

## Concepts about Our projects

### Weakness of BFT
The members should be pre-defined and identified rather than participating at will at any time like POW. Moreover, it is considered that the upper bound of the number of nodes is 100, so it is hard to implement on the public blockchain. It is rather suitable for private blockchain or consortium blockchain. FOr example, the famous consortium blockchain 'Hyperledger fabric' utilizes PBFT. 

### why PBFT
PBFT(Practical BFT) solve the effiency problem of BFT, from O(exponential) to O(polynomial). This algorithm asserts the liveness and safety only with (n-1)/3 fault tolerance, so the number of bodes must be N >= 3f+1, where f means the number of fault nodes. Therefore, the whole blockchain are required to contain at least 4 nodes for 1 fault tolerance.

### What is PBFT

First of all, all the evaluation nodes elect a 'primary'(like a leader) to be responsible for new block generation and broadcast to all the evaluation nodes.(maybe pre-elect or take turns) At the same time, the other evalution nodes are called 'backup'. And 'view' means the combination of 1 primary and many backups. To reach a consensus, there are three stages below:

1. pre-prepare:
  * A client send a request to the primary and the primary goes to the stage 'pre-prepare', generates a new block and broadcast to all the other backups.
  * After that, all the evaluation nodes(including the primary) switch to the next stage 'prepare'.
  * If the client doesn't receive the reply for a long time, the client can choose to send the request to all the evaluation node, and switch to the 'change view' stage.

2. prepare
  * wait until 2f+1 confirms (accept or reject)
  * if timeout, change view, elect a new primary ,and go back to step1.

3. commit
  * broadcast again to tell all the other evaluation nodes that you have more than 2f+1 evalation nodes comfirm.
  * wait until 2f+1 commits and reply back to client
  * if timeout, change view, elect a new primary, keep the information before and go back to step1..

#### How to solve the problem of view change 

'View change' stage ensures that the whole system can still work even though the primary is the node who is at fault. If one's timeout happens, the node can broadcast the signal 'view-change' to all the other nodes. If the v+1 node receive more than 2f+1 view-change signal (include itself), new-view happens, and the v+1 node broadcast to all the evaluation nodes that it becomes the new primary.

## Reference Pages

There are various reference websites categorized by their objectives. 

### BFT vs PBFT
* [Jianshu(BFT)](https://www.jianshu.com/p/5d10cf62d942?fbclid=IwAR3fbBwpbP7Fp3q_Q62EzZozlktIVotQzdpi3g55kdSVsgfoPhR9_oPmmS8)
* [Jianshu(PBFT)](https://www.jianshu.com/p/fb5edf031afd)
* [Wikipedia](https://zh.wikipedia.org/wiki/%E6%8B%9C%E5%8D%A0%E5%BA%AD%E5%B0%86%E5%86%9B%E9%97%AE%E9%A2%98)

### PBFT
* [samsonhoi](https://www.samsonhoi.com/570/blockchain-pbft?fbclid=IwAR09yIO8ZefBw4HyDpDH-9qYwobxeDchqhO-SX5O4DEpQki-rMz3N6BUqfA)
* [Baidu](https://baike.baidu.com/item/%E6%8B%9C%E5%8D%A0%E5%BA%AD%E5%B0%86%E5%86%9B%E9%97%AE%E9%A2%98?fbclid=IwAR3hlrfV8X5zhO_Dfa6BBHfzfdHOsEjIU-_XbuuQS2ZrqCk5x3DWqpKSTEQ)
* [saowen](https://hk.saowen.com/a/a92ab374b7ce3366948dae182747f662919efd7282dc87cad75ec32470d98a40)

### STO(Security Token Offering)
* [blockchainappfactory](https://www.blockchainappfactory.com/security-token-offering-services)

### Consortium Blockchain
* [Insider](https://www.inside.com.tw/article/14233-consortium-blockchain-b2b-bitcoin-peer?fbclid=IwAR0e4Ih6ALkTQ2l6hjSzPh9-seJCxZ5NHoyacIxe3D-lgyyeHnN3hgt9Cws)

### Implementation
* [HoneyBadgerBFT-Python](https://github.com/initc3/HoneyBadgerBFT-Python/)
* [pbft](https://github.com/luckydonald/pbft)
* [oschina](https://my.oschina.net/andylo25/blog/1831043)


## Contributing


## Authors

* **Cynthia Liu** - *Initial work* - [DannyTsai](https://github.com/Chung-Hung)
* **Danny tsai** - *Initial work* - [CynthiaYLiu](https://github.com/CynthiaYLiu)
* **Pierre Su** - *Initial work* - [PierreSue](https://github.com/PierreSue)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

