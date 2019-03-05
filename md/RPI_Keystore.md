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

## Create digital capsule 

- User has a chuck of data need to put into digital capsule -> the data, or payload
- User has a runtime logic to define when and how to unlock the digital capsule. -> the code, or wrapper
- Digital capsule engine random generate an AES key
- Use the AES key to encrypt the data. BTW, the data can also include other execution code which needs protection.
- After encryption, encrypte the AES using TPM's RSA key and store in RPI or anywhere else.
- Compile the logic into a smart contract. Deploy the smart contract on chain.
- Create header code. In header code, we define who owns the digital capsule, where to find the smart contract, hash of original (decrypted) payload. 
- Append encrypted data chunk to the header. Now the header and payload combined together as a digital capsule
- Put the digital capsule to IPFS, get the hash address. Broadcast the digital capsule hash.

## Transporation of digital capsule
The digital capsule itself is stored on IPFS which is an open storage. Because the data is encrtypted with the AES key, there is no need to protect the digital capsule itself, but to protect the AES key.

the AES key ... to be continue...

## Request signature using smart contract from remote digital capsule executor



