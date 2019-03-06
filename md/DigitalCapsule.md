# Use Raspberry Pi as key storage (hot wallet)
Zymbit can verify and sign transaction. Zymbit can also encrypt RPI's root storage so that the OS and key storage won't be accessable by other TPM. In this case, as long as the RPI is physically save, the api only run secured booted OS and App, user can trust RPI as a safe device and use it (24*7 running) to issue AES key of his own digital capsule.

## Init
Brand new RPI with TPM install the trusted OS and apps environment. including encrypted root sector with the following apps
* Rasbian OS
* Zymbit API / SDK
* Docker Engine
* Docker image of KeyGen app, generate random master key (one time, docker image deleted after generated)
* Digital Capsule Engine (A python app as secure guard to release or lock AES key)

When init, start a docker container to run KeyGen. Create a master key then delete image. Store the key in storage and a piece of paper as well.

Use TPM to LUK dm-encrypt the root sector. 
Restart.

After that, the master key and whole OS won't accessable by other device.

## load docker images
the following images will be loaded from trusted source, monitored by P2P network

* docker image of P2P network node
* docker image of block light client
* docker image of database
* docker image of smart contract runtime

We do not store those images into the encrypted root sector because they may be frequently updated. Once data encrypted by TPM, it is very hard to update.

Docker engine and Checking and verifying those images are done by the code inside the encrypted sector, so they can be trusted.

Once those images are loaded, this RPI starts to server as a node in P2P network. 

# Digital capsule demo process - Data Capsule

## Create digital capsule 

- User has a chuck of data need to put into digital capsule -> the data, or payload
- User has a runtime logic to define when and how to unlock the digital capsule. -> the code, or wrapper
- Digital capsule engine random generate an AES key
- Use the AES key to encrypt the data. BTW, the data can also include other execution code which needs protection.
- After encryption, encrypte the AES using TPM's private key and store in RPI or anywhere else.
- Compile the logic into a smart contract. Deploy the smart contract on chain.
- Create header code. In header code, we define who owns the digital capsule, where to find the smart contract, hash of original (decrypted) payload. 
- Append encrypted data chunk to the header. Now the header and payload combined together as a digital capsule
- Put the digital capsule to IPFS, get the hash address. Broadcast the digital capsule hash.

## Transporation of digital capsule
The digital capsule itself is stored on IPFS which is an open storage. Because the data is encrtypted with the AES key, there is no need to protect the digital capsule itself, but to protect the AES key.

the AES key is stored in the original RPI and encrypted by that RPI's TPM. Actually even the encrypted AES key leaked, no one can decrypted without the TPM's RSA key.

With such protection, the digital capsule can be safely stored transferred in public internet.

## Request signature using smart contract from remote digital capsule executor

When the digital capsule is loaded into an executor's machine. The executor will read the header first. Validate the required envrionment is provided (such as docker images, network etc). 

Then the wrapper code will be executed first. The wrapper code will get the executor's public key from the running envrionment variables. Then it will call blockchain's smart contract. The calling parameters including
- digital capsule ID
- owner ID
- execution public ID
- smart contract ID

All of the above information could be faked, however, it any of them is faked, there is no way for the executor to get the AES key, since the owner's RPI will send the AES key encrypted using executor's public key. If a hacker use other good node's public key, the answer will be sent to that good node and decrypted by the good node only.

## Smart contract execution
When smart contract is triggered, it will check the blockchain against the executor's reputation data, all required environment setup etc based on what is previous defined in the smart contract code. If all requirements met, the smart contract will give a green light by saving a signed permission on the blockchain.

## Owner's RPI release the key
When owner's RPI received the new permission on the blockchain, it will trigger releasing AES key process.
During this process, it will first find the AES key(encrypted and stored in RPI),  decrypt using TPM's private key. do not save the plain key anywhere but put into a P2P message encrypted using executor's public key, sent to the executor.

## Executor get the AES key and lock the data
When executor receive the key, decrypt using it's own private key in the trusted environment. Use this AES key to lock the digital capsule and execute the code to get the return value.

## Remote attestation during execution

Blockchain will VRF select remote attestion verifier to make sure the executor is in good shape, before, during and after execution.

## Sending back the result
Based on who was predefined in the digital capsule, the result will be sent back to receiver over P2P network.

## Clean up and sign
Digital capsule code will quit after execution. The executor will clean up memory, storage, all remaining docker image etc. Make sure the hardware and software envinronment turn back identically to the stat before the digial capsule is executed. 
All of this kind of clean up and verification cannot be done by digital capsule wrapper code, because it is terminited. It will be monitored by those remote attestation nodes. They will verify throught the Root of Trust Agent (RPI with TPM in our demo case). If everything goes correct, those verifier will run a consensus (PBFT, or FastBFT) and sign a transaction to the blockchain. 

## Reward, punishment and reputation

This transaction will be used to pay the reward, or, in case of marlicious behevior, punish the executors or comprimised varifier. All the reward or punishment logic is defined in the basic consensus using smart contract on layer-1 blockchain layer. 

If the executor doing well, it will gain reputation. This reputation value will be accuminated to gain higher chance to be selected by VRF in the future.

# alternative solution and improvement

Digital capsule warpper to call smart contract will take pretty long time. if the wrapper code can directly contract the owner's RPI (P2P with encrypted messaging), it can ask the owner's RPI to check the executor's reputation, so that it can be done in one block time.

# Digital capsule demo process - Docker Capsule

Docker capsule is different than Data Capsule. Docker images itself is a docker image. All the files which needs protection will be encrypted using an AES key which is not inside the image. So it is OK to share to store in public spaces.

When the docker images are loaded into executor, the RUN command will start the plain code, just like the wrapper code in Data Capsule. The plain code will do the same as previous mentioned wrapper code to get AES key from the blockchain using smart contract. 

The pros of Docker Capsule is 
* All in one image. Self contained, Portable, less dependents on running environment
* can be run on any executor without prerequisites
The cons:
* Large size, cause large network traffic
* Update take more cost (need to rebuild image and upload)

# Kraken, an Open Source Peer-to-Peer Docker Registry
Kraken (see [github](https://github.com/uber/kraken)) is an open source, peer-to-peer (P2P) Docker registry.