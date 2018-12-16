# Lemonade

## 20181216 Updates
1. Add new coin
2. Send specific type of coin to someone
3. Modify 'getbalance' to show various types of coins a user has 

## Example Commands

### Create new blockchain
```bash
$ python cli.py createblockchain --address Pierre --subsidy 200 --cointype BAR
```

### Send coins to another user
```bash
$ python cli.py send --from Pierre --to Danny --cointype BAR --amount 20
```

### Add a new coin to the blockchain
```bash
$ python cli.py addcoin --subsidy 2000 --cointype JIMBEAN --address Cynthia
```

### Show the balance of an address
```bash
$ python cli.py getbalance --address Pierre
```

### Print the blockchain
```bash
$ python cli.py print
```
