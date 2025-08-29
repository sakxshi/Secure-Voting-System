# Secure Voting System

## Overview
A blockchain-inspired voting system that ensures fairness, privacy, and security using SHA-256 hashing, digital signatures, Merkle Trees, and Zero-Knowledge Proofs (ZKP).

## Features
- **Digital Signatures**: Only valid voters can cast votes  
- **SHA-256 Hashing**: Prevents vote tampering  
- **Merkle Tree**: Efficient verification of votes  
- **Zero-Knowledge Proofs**: Privacy-preserving validation  
- **Blockchain**: Immutable election record  

## How It Works
1. Voter casts a ballot which is hashed with SHA-256  
2. Hash is signed with voter’s key, ensuring authenticity  
3. Votes are stored in a Merkle Tree, producing a Merkle Root  
4. Root and signatures are recorded on the blockchain  
5. Voters can verify their inclusion with Merkle Proofs without exposing all votes  

## Security
- **Integrity**: Votes cannot be altered  
- **Authenticity**: Only authorized voters can participate  
- **Anonymity**: Voter privacy is protected  
- **Transparency**: Public verifiability of the election  
- **Immutability**: Past records cannot be changed  
