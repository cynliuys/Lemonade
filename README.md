# Lemonade

## 20181216 Updates
1. Add new coin
2. Send specific type of coin to someone
3. Modify 'getbalance' to show various types of coins a user has 

## 20190111 Updates
1. Add wallets

## Example Commands

### Create Wallet
```bash
$ python cli.py createwallet
```
p.s. Remember to store the wallet created here!

### Create new blockchain
```bash
$ python cli.py createblockchain --address LbLVRR9bKVto6mxTXow9VVviU9mJtvtZib --subsidy 200 --cointype BAR
```

### Send coins to another user
```bash
$ python cli.py send --from LbLVRR9bKVto6mxTXow9VVviU9mJtvtZib --to LV6hxtR4Axc9spcFLFGfZkYooa7XGQ4GzZ --cointype BAR --amount 20
```

### Add a new coin to the blockchain
```bash
$ python cli.py addcoin --subsidy 2000 --cointype JIMBEAN --address LV6hxtR4Axc9spcFLFGfZkYooa7XGQ4GzZ
```

### Show the balance of an address
```bash
$ python cli.py getbalance --address LV6hxtR4Axc9spcFLFGfZkYooa7XGQ4GzZ
```

### Print the blockchain
```bash
$ python cli.py print
```
