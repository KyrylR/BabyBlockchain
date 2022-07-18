# Solutions to the practical assignment: "Implementing a 'baby' blockchain"

Distributed Lab Course in Summer of 2022.

## Description

The main purpose of this project is to understand the basic workings of blockchain technology.
Awareness is gained by implementing your own minimal version of blockchain
(no decentralisation and consensus mechanisms, just basic structures).

## Overview and purpose of the system/product

The system I wanted to develop is one where users can buy something in an auction format and also, in the future,
the possibility of scalability, including: the added functionality of data exchange systems, exchanges, registries
and those or other systems that can improve the project.
The system will be used for the creation and/or purchase of digital products such as novels, books, artworks and
any other items not requiring a lot of storage space, ideally up to 10 Mb.

## Content of the system (system boundaries)

The main components of the system will be as follows:

* Hash: a "wrapper" class for the use of the gash function;
* Signature: a "wrapper" class to use a digital signature;
* KeyPair: a class designed to work with keys;
* Account: a class for working with the wallet, creating transactions and signing data;
* Operation: a class allowing to create a payment operation;
* Transaction: a class allowing to create a transaction containing payments of users;
* Block: a class that forms a block with transactions;
* Blockchain: a class to create a blockchain, a database of coins and existing transactions;
* DigitalProduct: a class that describes the content and/or content of a digital product.

## Interaction (potential) of the product (with other products and components)

The system itself will need visualization and functionality such as, exhibition, product discussion,
notification of auction start and so on.
Also, if the system is to be scaled up, the use of the functionality of data exchange systems,
registries, voting platforms, if useful.

## Product functions (brief description)

1. Ability to create and/or purchase a digital product.
2. Ability to view the main features of the product.
3. The ability to verify who owns the product in question.
4. The ability to ensure the anonymity of the buyer and trade for the consumer.
   In my opinion, this is the basic functionality needed for an auction of digital products, ready to suggests.

## Security requirements

At the moment it is rather difficult for me to understand what the security requirements are; so, if possible,
please suggest what is meant by security requirements.
Is it stability of function or the same anonymity, integrity of the system?

## User characteristics (who is the end user of the system)

Authors, translators, readers, fans and so on. All people who want to own, create, use, sell, are able to use this
product, to ensure all these points; while providing their anonymity and the ability to verify ownership of this or that
product.

## Limitations

The most important issue is the resource cost, i.e. the memory and speed of the auction itself.
At the 1st stage I plan to limit the size of the block to 10 megabytes, respectively, the maximum amount of
the transaction will be 25 percent of this value.
I plan to use FBA algorithm to achieve consensus.

---

`Ready to hear opinions and suggestions on this idea.
Ready for criticism.
Thanks for your feedback!`

---

### Executing program

* To run the tests, you must activate hash_lib_venv:

```
.\venv\Scripts\activate
```

#### After performing one of the steps above, execute the following command sequences to execute appropriate algorithms:

* Auction test:
```
python .\console_test_auction.py
```

* Blockchain test:
```
python .\console_test_blockchain.py
```

### Test result

* Test auction
```
(venv) PS C:\Users\inter\source\Python\BabyBlockchain> python .\console_test_auction.py
Auction has started! Time left: 00:01:40
There is already a higher or equal bid
Winner account: 73b424725314fc80188681b04145a7c291160cefc9ec10bd6da81db13d995335
Winner paid: 11
The auction has already ended!
.
----------------------------------------------------------------------
Ran 1 test in 9.630s

OK
```

* Test blockchain
```
(venv) PS C:\Users\inter\source\Python\BabyBlockchain> python .\console_test_blockchain.py
('Balance: 20 for account: '
 '99fc518cbdad12964fe2c03f7779d2ee4b5ddc09abc40308659d312491911dcd')
Account 1:      None
('Balance: 13 for account: '
 '676068c77002f35d80ce3566db18763803533497debb003eb8a757775e1efc56')
Account 2:      None
Coin database:  {'58e4d61a652e371dd08936bb4cfdbb8c69495a3f7b8347342e01cc93c2518b48': 0, '99fc518cbdad12964fe2c03f7779d2ee4b5ddc09abc40308659d312491911dcd': 20}
Coin database:  {'58e4d61a652e371dd08936bb4cfdbb8c69495a3f7b8347342e01cc93c2518b48': 0, '99fc518cbdad12964fe2c03f7779d2ee4b5ddc09abc40308659d312491911dcd': 20, '676068c77002f35d80ce3566db18763803533497debb003eb8a757775e1efc56': 13}
Transaction:    Transaction id: 8f1eeb1027364b554f6801b7001143c43eb3f1c4
Timestamp:      1658167744
Sequence:       255]

Transaction:    Transaction id: 4db9f8124bdf052587d32d9b4810e2fd81a67251
Timestamp:      1658167744
Sequence:       120]

Block 1:        Block id:       05b342f2faf29466b0fc59e38017be1dbe3a4d55
Prev hash:      0be0199a8a6912949176129e153595a493bbd661
Timestamp:      1658167745
Target:         91343852333181432387730302044767688728495783935
Nonce:          4]



Start block history
--------------------
Block id:       0be0199a8a6912949176129e153595a493bbd661
Prev hash:      0x00000000000000000000000000000000000000000000
Timestamp:      1658167744
Target:         91343852333181432387730302044767688728495783935
Nonce:          24]


Block id:       05b342f2faf29466b0fc59e38017be1dbe3a4d55
Prev hash:      0be0199a8a6912949176129e153595a493bbd661
Timestamp:      1658167745
Target:         91343852333181432387730302044767688728495783935
Nonce:          4]


--------------------
End block history


Block history:  None
Coin database:  {'58e4d61a652e371dd08936bb4cfdbb8c69495a3f7b8347342e01cc93c2518b48': 0, '99fc518cbdad12964fe2c03f7779d2ee4b5ddc09abc40308659d312491911dcd': 57, '676068c77002f35d80ce3566db18763803533497debb003eb8a757775e1efc56': 26}
Block 2:        Block id:       08f6ec05dc3cdeb22146a64e34990ef4fc111e60
Prev hash:      05b342f2faf29466b0fc59e38017be1dbe3a4d55
Timestamp:      1658167746
Target:         91343852333181432387730302044767688728495783935
Nonce:          32]



Start block history
--------------------
Block id:       0be0199a8a6912949176129e153595a493bbd661
Prev hash:      0x00000000000000000000000000000000000000000000
Timestamp:      1658167744
Target:         91343852333181432387730302044767688728495783935
Nonce:          24]


Block id:       05b342f2faf29466b0fc59e38017be1dbe3a4d55
Prev hash:      0be0199a8a6912949176129e153595a493bbd661
Timestamp:      1658167745
Target:         91343852333181432387730302044767688728495783935
Nonce:          4]


Block id:       08f6ec05dc3cdeb22146a64e34990ef4fc111e60
Prev hash:      05b342f2faf29466b0fc59e38017be1dbe3a4d55
Timestamp:      1658167746
Target:         91343852333181432387730302044767688728495783935
Nonce:          32]


--------------------
End block history


Block history:  None
Coin database:  {'58e4d61a652e371dd08936bb4cfdbb8c69495a3f7b8347342e01cc93c2518b48': 0, '99fc518cbdad12964fe2c03f7779d2ee4b5ddc09abc40308659d312491911dcd': 94, '676068c77002f35d80ce3566db18763803533497debb003eb8a757775e1efc56': 39}
.
----------------------------------------------------------------------
Ran 1 test in 3.954s

OK
```

## Authors

ex. Kyrylo Riabov [Gmail](kyryl.ryabov@gmail.com)

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.

* [Bitcoin White paper](https://bitcoin.org/bitcoin.pdf)
* [Blockchain demo](https://andersbrownworth.com/blockchain/hash)


