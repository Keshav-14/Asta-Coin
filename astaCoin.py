# importing Libraries
import datetime as dt
import hashlib as hl
import json

class Blockchain:
    
    def __init__(self):
        
        self.chain = []
        
        '''
        * Mining the genesis block 
        * initiating the proof and the previous hash with an arbitrary values
        '''
        
        self.createBlock(proof = 1, previous_hash = '0')
    
    # Building the Blockchain

    def createBlock(self, proof, previous_hash):
        
        '''
        * Create a block and add it to the blockchain
        * proof => proof of work
        * previous_hash => hash of the previous Block
        '''
        
        block = {
            # defining the structure of the block
            'index' : len(self.chain) + 1,
            'timeStamp' : str(dt.datetime.now()),
            'proof' : proof,
            'previousHash' : previous_hash,
        }
        self.chain.append(block);
        return block
    
    def getPreviousBlock(self):
        
        '''
        * Returns the Last Block(previous block to the block that is 
                                 going to be mined) in the chain
        '''
        
        return self.chain[-1]
    
    def proofOfWork(self, previous_proof):
        
        '''
        * Function to return the proof of work
        * finds the proof with trial and error method
        * proof should be challenging at the same time should be simple to verify
        * increasing the leading zeros in the hash we can increase the 
                difficulty level in finding the proof
        * previous_proof => proof of the previously mined block
        '''
        
        new_proof = 1
        check_proof = False
        while check_proof is False :
            hash_operation = hl.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation [:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof
    
    def hash(self, block):
        
        '''Returns the hash of the block'''
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hl.sha256(encoded_block).hexdigest()
    
    
    def isChainValid(self, chain):
        
        '''
        !!!!!!!!!!!!!!
        Why am i passing the chain as a parameter ? if i just wanna access i can directly access using self.chain !
        but why am i passing?
        !!!!!!!!!!!!!!
        '''
        
        '''
        * Verifies whether the previous block hash value in the block 
            is equal to the actual hash value of the previous block or not
        '''
        
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block['previousHash'] != self.hash(previous_block) : 
                return False
            previous_proof = previous_block['proof']
            current_block_proof = current_block['proof']
            hash_operation = hl.sha256(str(current_block_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = current_block
            block_index += 1
        
        return True   
