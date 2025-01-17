# Paste your version of miner.py from the clinet_mining_p
# folder here

import hashlib
import requests
import time

import sys


# TODO: Implement functionality to search for a proof

def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


def proof_of_work(last_proof):
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof


def fetch_last_proof():
    URL = 'http://localhost:5000/last_proof'
    response = requests.get(url=URL)
    data = response.json()
    return data['last_proof']


def mine_block(proof):
    URL = 'http://localhost:5000/mine'
    request = {
        "proof": proof
    }
    response = requests.post(url=URL, json=request)
    return response.json()


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        last_proof = fetch_last_proof()
        print("Calculating proof")
        start_time = time.time()
        proof = proof_of_work(last_proof)
        end_time = time.time()
        time_elapsed = end_time - start_time
        print(f"Proof calculated in {time_elapsed} seconds.")
        response = mine_block(proof)
        if response:
            if response["message"] == 'New Block Forged':
                coins_mined += 1
                print(response["message"])
                print(f'{coins_mined} coins mined.')
            else:
                print(response["message"])
        else:
            print("POST request failed.")
