# TrustedComputing_POC
Zymbit on Raspberry Pi as TPM, build a P2P network. use Pi as PXE to boot PC as execution node. Remote attestation consensus save to the blockchain. Proof of Security and Reputation enforce node trustworthy

# POC Experiment Goal
* To setup a P2P network with few nodes. 
* One node A can can create a execution task (pure function) but executed in other nodes X which cannot be predict. 
* We need an algorithm to guarantee the execution node X did run the exactly the same code in exactly environment as node A originally defined.
* During the execution in Node X, there is no way for X to communicate with any other nodes or outside world except those connections defined in the execution task originally by node A.
* During the execution in Node X, there is no way for X to connect / disconnect any hardware or any modification unless predefined originally in the execution task by Node A.
* After the execution completed, Node X will send the result to Node A or any other nodes predefined in the execution task. 
* After the execution completed Node X will return the whole system stat to the original stat before execution. If there is any temp files or data in any storage, they will be cleanly removed (non recoverable). The RAM need to be clean as well. All above clean up can be verified and guaranteed. 
* All permanent storage will be on blockchain. But only the remote attestation record, nothing related to the execution task or data.

Link to [Digital Capsule](md/DigitalCapsule.md)

# Experiment Limitations
* We do not guarantee the execution result is correct. We do not know , do not care, do not monitor any mistakes in the execution code. We just make sure the Node X is running exactly the code Node A defined. 
* The execution tasks are ideally batch task which have limited execution time. Long running web services are not good for this kind of execution environment. 
* Execution environment need to be running in Docker container. 
* The computer who do execution need to have a Ethernet RJ 45 port and BIOS supports LAN boot from a PXE server
* As long as the malicious node would like to wait enough time and accept the lost of historical reputation built up over a long period of time and the deposit, it actually can stop execution and take the machine offline while steal the private data already decrypted in memory or hard drive. Like other blockchain project, we cannot prevent malicious activities happen, we can raise the cost of attack to stop.
* We use Zymbit Raspberry Pi TPM module as our hardware root of trust. If that module is not trustable, our experiment won’t be trustable either.
* We have not set gas limit yet. If there is a dead loop, it will dead until we force it quit. We can have a quick and dirty temp solution, that is to set a timeout. 

# Planned Future Experiments
* Complete the reputation system on blockchain
* As long as the node execution is trustable, we can design a new consensus to replace existing POW or POS. Such as PoET or any other consensus based on TEE
* Automatically convert smart contract into digital capsule
* new [CQRS](md/Bridge_to_traditional_cloud_app_developer_CQRS_model.md) model for traditional cloud app developers.
# Experiment Setup
## Whole picture
![whole picture](/md/imgs/img001.svg)

### P2P Network of Trusted Raspberry Pi with TPM

### RPI with TPM as trusted node. 

They connected together as a P2P network. Ideal Chord DHT connection.
![Rpi with TPM](https://zymbit.com/wp-content/uploads/2019/01/ZK-II-I2C-fitted-to-RPI-inside-case-landscape.gif)
RPI cannot run complicated computation. We use them as Trust Root of HPC. The actual computation (if complicated enough) will be done by the HPC.

HPC (High Performance Computer) will not connect to any other network directly but connect solely to the RPI with TPM. 

The RPI is the HPC’s network gateway and  PXE boot server. Detail in in the diagram below
![relationship between rpi and hpc](/md/imgs/img002.svg)
### HPC (High Performance Computer) is the one actually execute computation tasks. 
* HPC is trapped in a isolated environment. HPC cannot have any kind of physical or logical communication with outside world
* HPC’s only network connection is the RPI
* HPC has a hard drive, but there is no boot OS there. 
* HPC will boot from RPI which is working as PXE server. RPI will store the HPC’s boot OS image and server to HPC when booting.
* After HPC boot, HPC’s remote attestation agent will auto start and talk to RPI’s remote attestation server. Answer question from the RPI honestly.
* HPC will receive RPI’s request of execution digital capsule. Any communication will go through RPI. Any unexpected trial to connect outside internet will be log and banned by RPI.
![relationship between rpi and hpc](/md/imgs/img003.svg)

RPI (Raspberry Pi) with Zymbit TPM as Root of Trust for the HPC. But inside the RPI, the Zymbit TPM is the root of trust for RPI. 
## Chain of trust
![chain of trust](/md/imgs/img004.svg)
We can see the Zymbit TPM is the root of trust for everything. It is a hardware TPM chips plugin to RPI’s GPIO ports. 

Zymbit TPM has a lot of security features for detail please go to https://www.zymbit.com/zymkey/

We will use the hardware TPM as the root of trust for RPI. RPI’s boot disk will be encrypted using LUKS dm-crypt https://community.zymbit.com/t/topic/150

The boot image is supposed not to have a lot of changes. All changes will be on the docker images. All the services are not directly loaded from boot image, but from docker images.

## How to reduce the risk without HPC's TPM
You can see we simplified the HPC's requirement, we do not have a TPM installed on the HPC. We only have a TPM equiped RPI connect to HPC via network. This is a huge security risk since network attestation is far less secure than embedded TPM directly plant on bare metal.

We use the follow solution to reduece the risk
### The HPC boot from RPI

RPI control the boot OS image, there is no way for HPC to load malicious software through the secured boot

### VRF random selected executor cause the side channel attacker to wait for unexpectations

Side channel attack is very hard to detect and prevent. We do not try to deal with it, but we create as much uncertainty as possible to the attacker. Since no one know what digital capsule will be executed in this particular node, and how much the value is supposed to be. The execution time is very short. If the attack is waiting for a valuable digital capsule to attack, he will need to pay a lot time cost. 

If the exeuction is only few ms, it would be hard for the attacker to get useful information leaks. There is no way to predict and very low chance when the same digital capsule will come to this node again.

Once the side attack (although hard) to be detected. The node will lost all its reputation for a very long time and deposit. It will be a rather long time to rebuild the reputation from ground up. the time cost is huge for attackers.

VRF will not announce which node is going to execute which digltal capsule before it is completed. So if any attacker want to make a remote attack, he cannot find the high value target.

### Some hardware fingerprint can be got from pure software

Not all kind of hardware fingerprint need direct hardware access. One example is described in "Run-Time Accessible DRAM PUFs in Commodity Devices" -  https://www.youtube.com/watch?v=PmDhe3Na7LQ

We can use Attestation Agent to generate some of those hardware fingerprint when hardware shipped from manufacturer. This fingerprint (most likely in merkle tree format) will be stored in blockchain with public key. This finger print can be validate later. If the fingerprint not matching in the future, it most likely caused by hardware attack.

### In the future, we also consider additional hardware TPM on HPC's bare metal

The reputation system in layer-1 blockchain can set different level based on hardware security level. The bare metal with TPM will have higher level by default.

Hardware fingerprint is a big topic, we won't dive too deep in this document

## Benefit of not having TPM in HPC

### Not all digital capsule need HPC, most of them can be done inside RPI

Yes, the more and more will be in the future. If we design correctly, at least most of the smart contract doesn't need intensive computation. They can be execute in a light weighted docker container supported by RPI. We do not need HPC in this case at all.

### HPC without TPM can be general available to general public. Keep our blockchain permissionless

There is always trade off between permissionless and security. If every machine need TPM of course will gain on security, but limits who can join the computation network. 

Software or no TPM is much easier, but of course, lack of hardware supported security. What we are going to do is to use blockchain to patch on those security we lost. 

Simple consensus and reputation system , especially VRF can cover many of the security losses. When the consensus is running between trusted RPI, the speed is much faster than traditional blockchain. So we do not lose scalability either.



## Storage area inside RPI
![storage area on RPI](/md/imgs/img005.svg)
There are two major storage area inside the RPI SD card. 
The encrypted part is the boot OS image. It include everything required for docker to start those services. 

The plain part is the different services will be load to docker container and run. Those images are supposed to get frequent updated, so we prefer not to put them into the encrypted storage part. Instead, download from trusted source as a docker image. 

All the images will be downloaded from trusted P2P network source, and the hash will be checked by “Verification module” which stay inside the encrypted part. 

So inside the RPI, the Trust Chain looks like

![trust chain inside](/md/imgs/img006.svg)

So the hardware is the root of trust, and the relationship between each module in the trust chain.

## RPI Secure Boot

The RPI will boot from encrypted OS. The decryption is done by the TPM, so it is trusted.
The boot image includes all necessary components to run except those can be running in docker containers. 

After RPI booted, it will start docker engine and load those docker images into containers and run. 

All the docker images RPI downloaded and load will be checked by the Verification Module. It will only allow to download and load the “blockchain” approved images. Also, everything it allow to load will be saved to blockchain as expected so that other remote attestation nodes can verify using consensus. 


## HPC Secure Boot
HPC doesn’t book itself, it will set BIOS to boot from LAN PXE server. The boot image is fed from RPI, and under monitoring by RPI.

# Tasks
## Task 1: Setup Raspberry Pi with Zymbit TPM
Done
## Task 2: Setup Raspberry Pi with Docker Engine
Done
## Task 3: Setup PXE server to support PC remote boot from secured image
Set the BIOS of the PC to boot from LAN. 
Set up the PXE server in RPI. If possible, put into docker container so that we can stop the container after boot successfully completed.


## Task 4: HPC remote attestation agent
Agent runs in system root level of OS on HPC
Agent only communicate with RPI where HPC boot from. Use encryption and automatically change keys.

Based on the Remote Attestation Server required, the agent will get all kind of system information to the server. Including memory hash, hard drive hash. So called hardware fingerprint
![relationship between remote attestation agent, server and consensus services](/md/imgs/img007.svg)

## Task 5. RPI remote attestation server
Server runs on RPI. It will talk to the connected HPC’s agent. Monitor the HPC’s running stats. The monitoring process is constant, frequent and unpredicted. 

Based on predefined logic, in case of some critical criteria not meet, the server can decide to report, as well as extreme steps to be made (such as stop execution, reboot the HPC).

Also, Based on RPI’s remote attestation consensus service request, check the stats of the HPC and report to other consensus nodes.

## Task 6. RPI remote attestation consensus service
As one of the consensus node running in a RPI, it will contact with other RPI nodes ( VRF selected Verifier. Other verifier will ask questions about the stat of HPC before, during and after executing a task. Services will relay the question to the remote attestation server and agent on HPC to get the trusted result and get back to those Verifier. 


## Task 7. Create test digital capsule
We can do very simple digital capsule task to demo how the workflow works. One example is like this:
Node A define a function: Get two name lists of strings from two different untrusted nodes, find out the common strings and send them back to both nodes
Node B prepare a name list, put into digital capsule, store in IPFS
Node C prepare a name list, put into digital capsule, store in IPFS
Any of A,B or C, create a task including the function and two digital capsule, submit into P2P network
## Task 8. Node X execute the task with digital capsule
Node X is VRF selected to execute the task. Load two digital capsule. Execute and return the result in two other digital capsules and notify node B and C.
Node B and C open the result digital capsules check the answer.
## Task 9. Smart Contract to calculate payment
We still use traditional smart contract (such as Etherium or NEO) to run the token economics. Because the trusted computing is still under testing. We want to make sure the economy can still punish malicious node correctly even if the malicious node can control the trusted computing to untrusted.

