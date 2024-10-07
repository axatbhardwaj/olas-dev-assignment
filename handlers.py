import json
import logging
import os
import sys
from dotenv import load_dotenv
from eth_account import Account
from my_eth_utils import (
    get_web3_provider,
    get_erc20_contract,
    check_balance,
    transfer_tokens,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

load_dotenv()

# Load the ABI from the JSON file
with open("abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)

tenderly_fork_url = os.getenv("rpc_url")
logging.info(f"Tenderly fork URL: {tenderly_fork_url}")


def handle_hello_message(message: str, private_key: str):
    logging.info(f"Received 'hello' message: {message}")


def handle_crypto_message(message: str, private_key: str):
    logging.info(f"Received 'crypto' message: {message}")
    w3 = get_web3_provider(tenderly_fork_url)
    contract_address = os.getenv("contract_address")
    contract = get_erc20_contract(w3, contract_abi, contract_address)

    # Derive the source address from the private key
    account = Account.from_key(private_key)
    source_address = account.address

    target_address = os.getenv("reciver_address")

    # balance = check_balance(w3, contract, source_address)
    balance = balance = contract.functions.balanceOf(source_address).call()

    if balance > 0:
        transfer_tokens(w3, contract, source_address,
                        target_address, 1, private_key)
        logging.info("1 token transferred successfully!")
    else:
        logging.warning("Insufficient balance to transfer tokens.")
