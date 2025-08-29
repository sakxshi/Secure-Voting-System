import hashlib
import json
import random
import time
import datetime
import zero_knowledge_proof
import zkp
from uuid import uuid4

#EESHAAN GAUTHAM RAO - 2022B4A70881H
#AKSHAT AGARWALA - 2022B4A71003H
#SAKSHI SINHA - 2022A4PS1136H
#BHASKAR MISHRA - 2021B4A72427H

party = {'Democratic Party': [], 'Republican Party': [], 'Others': []}

class Voting_Blockchain(object):
    # Constructor
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.users = {}
        self.vote_history = {}
        self.node_ctr = 1
        self.prop_ctr = 1

    # Create user
    def create_voter(self):
        print()
        self.mine = 0
        try:
            uid = self.node_ctr
            miner = str(input("Enter the name of the voter: "))
            
            self.node_ctr = self.node_ctr + 1
            
            self.users[uid] = {
                'ID': uid,
                'Name': miner,
                'Voted': False,
                'Party Voted': None,
            }
            self.mine = 1
            print("The node was added to the blockchain\n")
            print(self.users[uid]['Name'] + "'s ID is " +
                  str(self.users[uid]['ID']) + "\n")
        except:
            print("Enter the correct format of data required to add a new node!\n")

    # Create New Block
    def create_new_block(self, previous_hash=None):
        ZKP = zero_knowledge_proof.ZKP(self.hash(self.transactions[:3]))
        print(self.transactions[:3])
        if (len(self.chain) == 0):
            block = {
                "Header": {
                    "Index": len(self.chain) + 1,
                    "Timestamp": datetime.datetime.now(),
                    "ZKP root": ZKP.getRootHash(),
                    "previous_hash": 0,
                },
                "Transaction": self.transactions[:3]  # 3 transactions
            }
        else:
            block = {
                "Header": {
                    "Index": len(self.chain) + 1,
                    "Timestamp": datetime.datetime.now(),
                    "ZKP root": ZKP.getRootHash(),
                    "previous_hash": self.hash(self.chain[-1]['Header']),
                },
                "Transaction": self.transactions[:3]  # 3 transactions
            }

        self.chain.append(block)
        del self.transactions[:3]
        return block

    # Create transaction
    def create_vote(self):
        try:
            print("You can vote the following parties: " )
            print(list(party.keys()))
            voter_id = int(input("\nEnter the Voter ID: "))
            party_name = input("Enter the Pary Name: ")
           
            if (not self.verify_transaction(voter_id, party_name)):
                print("\nThis Vote is not valid\n")
                return
            print("\nThis Vote is added and validated\n")
            trans = {
                "Transaction_ID": str(uuid4()).replace('-', ''),
                "Timestamp": datetime.datetime.now(),
                "Voter ID": voter_id,
                "Party Name": party_name,
                
            }
            self.transactions.append(trans)
            self.users[voter_id]['Voted'] = True
            self.users[voter_id]['Party Voted'] = party_name
            party[party_name].append(voter_id)

            if (len(self.transactions) == 3):
                self.mine_block()
                print("\nCreating a new block\n")
        except:
            print("Enter the correct format of data required to add a new transaction!\n")

    # Validate Transaction
    def verify_transaction(self, voter_id, party_name):
        if (party_name not in party):
            print("You cannot vote a party which does not exist")
            return False
        if(self.users[voter_id]['Voted'] == True):
            print("You have already voted")
            return False
        return True

    # Validate Chain
    def validate_chain(self):
        if (len(self.chain) == 0):
            return False
        previous_block = self.chain[0]
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            print("\nHash of Header of Block " + str(i-1) + " : " +
                  str(self.hash(previous_block['Header'])))
            print("Hash of Previous Block's Header stored in Block " + str(i) + " : ",
                  current_block['Header']['previous_hash'])
            if (current_block['Header']['previous_hash'] != self.hash(previous_block['Header'])):
                return False
            previous_block = current_block
        return True

    # Print Blockchain
    def print_blockchain(self):
        print()
        if (len(self.chain) == 0):
            print("Blockchain is empty, please add more transactions :)\n")
            return
        for i in range(len(self.chain)):
            print("Block", i, ":")
            print("Header: ", self.chain[i]['Header'])
            print("Transactions: ")
            for j in range(len(self.chain[i]['Transaction'])):
                print(self.chain[i]['Transaction'][j])
            print()
        print()

    
    def print_party_history(self, pid):
        try:
            print()
            if(pid not in party):
                print("Party does not exist\n")
                return
            print("Party Name: ", pid)
            print("Total Votes: ", len(party[pid]))
            print("Voters: ")
            print(party[pid])
            print()

        except:
            print("\nPlease enter the correct inputs!\n")

    # Hash Function

    def hash(self, block):
        strg = json.dumps(block, sort_keys=True, default=str).encode()
        return hashlib.sha256(strg).hexdigest()

    
    def mine_block(self):
        mini = 100000
        for i in self.users.keys():
            n = random.randint(1, 10)
            self.users[i]['wait-time'] = n
            mini = min(mini, n)

        print("\n-------------------Acheiving consensus-------------------\n")
        time.sleep(mini)

        for i in self.users.keys():
            if (self.users[i]['wait-time'] == mini):
                print(str(
                    self.users[i]['Name']) + " has won, thus the leader for this round of consensus will mine the block.\n")
                self.create_new_block()
                break            

    # Print Users
    def viewUser(self):
        print()
        for i in self.users.keys():
            print("User ID: ", i)
            print("Name: ", self.users[i]['Name'])
            print("Voted: ", self.users[i]['Voted'])
            print("Party Voted: ", self.users[i]['Party Voted'])
            print()
        print()


if __name__ == '__main__':
    mine = Voting_Blockchain()
    while True:
        print("1. Create a new voter")
        print("2. Create a new vote")
        print("3. Print the blockchain")
        print("4. Print the party history")
        print("5. Print the users")
        print("6. Validate Blockchain")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if (choice == '1'):
            mine.create_voter()
        elif (choice == '2'):
            mine.create_vote()
        elif (choice == '3'):
            mine.print_blockchain()
        elif (choice == '4'):
            pid = input("Enter the Party Name: ")
            mine.print_party_history(pid)
        elif (choice == '5'):
            mine.viewUser()
        elif (choice == '6'):
            if (mine.validate_chain()):
                print("\nThe Blockchain is valid!\n")
            else:
                print("\nThe Blockchain is not valid!\n")
        elif (choice == '7'):
            print("Hope you had fun voting!!")
            break
        else:
            print("Invalid choice")
