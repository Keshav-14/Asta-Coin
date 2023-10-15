# importing libraries
import astaCoin
from flask import Flask, jsonify, request
from uuid import uuid4


# Creating the Web App
app = Flask(__name__)


# Creating an address for the node on the port 5000
node_address = str(uuid4()).replace('-', '')


# Creating the Blockchain
blockchain_object = astaCoin.Blockchain()


# Mining a New Block
@app.route('/mineBlock', methods=['GET'])
def mineBlock():
    
    '''
    * Function for mining the Block 
    * 1st find the proof of work for the current block
    * then create the block and add it to the chain
    * here this function return the actually mined block in json format and a http success code 
    * this is just for ui interaction
    '''
    
    previous_block = blockchain_object.getPreviousBlock()
    previous_proof = previous_block['proof']
    proof = blockchain_object.proofOfWork(previous_proof)
    previous_hash = blockchain_object.hash(previous_block)
    blockchain_object.addTransaction(sender=node_address, receiver='Keshava', amount=5)
    mined_block = blockchain_object.createBlock(proof, previous_hash)
    response = {
        'message' : 'Congratulations, You just mined a block!',
        'index' : mined_block['index'],
        'timestamp' : mined_block['timeStamp'],
        'proof' : mined_block['proof'],
        'previousHash' : mined_block['previousHash'],
        'transactions' : mined_block['transactions'],
    }
    
    return jsonify(response), 200 #(HTTP success code)

    
# Getting the Full Blockchain to display in the postman User Interface
@app.route('/getChain', methods=['GET'])
def getChain():
    
    '''this function will return the current chain that is present in this block'''
    
    response = {
        'Chain' : blockchain_object.chain,
        'Length of Chain' :  len(blockchain_object.chain)
    }
    return jsonify(response), 200


# Checking whether the chain is valid or not!
@app.route('/isValid', methods=['GET'])
def isValid():
    
    '''Verifies whether the chain is valid or not'''
    
    is_valid = blockchain_object.isChainValid(blockchain_object.chain)
    response = {}
    if is_valid:
        response['message'] = "The BlockChain is Valid!"
    else:
        response['message'] = "The Blockchain is Not Valid"
    return jsonify(response), 200


# Adding new transactions to the blockchain
@app.route('/addTransaction', methods=['POST'])
def addTransaction():
    
    '''Adds a transaction to the blockchain'''
    
    json_response = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json_response for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400  # http error code
    index = blockchain_object.addTransaction(json_response['sender'], json_response['receiver'], json_response['amount'])
    response = {
        'message' : f'This transaction will be added to the block #{index}',
        }
    return jsonify(response), 201   # http status code successfully created the transaction


# Decentralizing the blockchain

# Creating the new node in the network
@app.route('/connectNode', methods=['POST'])
def connectNode():
    
    '''This Function will be useful in connecting the newly created or deployed node to the decentralized network'''

    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No Nodes", 400 # http error code
    for node in nodes:
        blockchain_object.addNode(node)
    response = {
            'message': 'All the nodes are now connected',
            'Number of Nodes in the Blockchain' : len(blockchain_object.nodes),
            'Total Nodes in the Blockchain' : list(blockchain_object.nodes),   
        }
    
    return jsonify(response), 201    # http success code

# Replacing the chain by the longest chain is needed!
@app.route('/replaceChain',methods=['GET'])
def replaceChain():
    is_replaced = blockchain_object.replaceChain()
    if is_replaced:
        response = {
                'message': 'The nodes had different chains so the chain was replaced by the longest one!',
                'new chain' : blockchain_object.chain,
            }
    else:
        response = {
                'message' : 'All Good, This chain is the longest one!',
                'actual chain' : blockchain_object.chain,
            }
        
    return jsonify(response), 200   # http success code
# Running the App
app.run(host='0.0.0.0', port=5000)
