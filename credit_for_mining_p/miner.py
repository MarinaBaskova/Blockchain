import hashlib
import requests
import json
import sys
from uuid import uuid4
​


def get_last_proof():
    response = requests.get("http://localhost:5000/last_block")
    # response = requests.get(url=node + "/lastproof")
    last_proof = response.json()
    return last_proof["proof"]


def create_new_block(found_proof, recipient_id):
    response = requests.post('http://localhost:5000/mine',
                             json={'proof': found_proof, "recipient_id": recipient_id})
    res_message = response.json()
    return res_message["message"]


def proof_of_work(last_proof):
    """
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    block_string = json.dumps(last_proof, sort_keys=True).encode()
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


def get_id():
    try:
        f = open("my_id.txt", "r")
        id = f.read()
        if id:
            f.close()
            return id
    except:
        f = open("my_id.txt", "w")
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
        return id


​
​
recipient_id = get_id()

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"
    ​
    coins_mined = 0
    # # Run forever until interrupted
    while True:
        last_proof = get_last_proof()
        print("Start mining the proof")
        found_proof = proof_of_work(last_proof)
        print("Finished mining the proof")
        res_message = create_new_block(found_proof, recipient_id)
        if res_message == "New Block Forged":
            coins_mined += 1
            print(res_message)
        else:
            print(res_message)
