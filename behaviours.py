import random
import time
import logging

from eth_account import Account
from my_eth_utils import get_web3_provider, get_erc20_contract, check_balance
import json
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

# Load the ABI from the JSON file
with open("abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)

tenderly_fork_url = os.getenv("rpc_url")
logging.info(f"Tenderly fork URL: {tenderly_fork_url}")


def generate_random_message(agent):
    words = [
        "hello",
        "sun",
        "world",
        "space",
        "moon",
        "crypto",
        "sky",
        "ocean",
        "universe",
        "human",
    ]
    message_content = f"{random.choice(words)} {random.choice(words)}"
    message = {"sender": agent.id, "content": message_content}
    logging.info(f"Generated message: {message}")
    agent.OutBox.put(message)
    logging.info("Message put in OutBox")
    time.sleep(2)
    logging.info("Sleeping for 2 seconds")


def check_erc20_balance(agent):
    # Implement the behavior to check ERC-20 token balance
    w3 = get_web3_provider(tenderly_fork_url)
    contract_address = os.getenv("contract_address")
    contract = get_erc20_contract(w3, contract_abi, contract_address)
    # Ensure the address is in the correct format
    account = Account.from_key(agent.private_key)
    address = account.address
    balance = check_balance(w3, contract, address)
    logging.info(f"ERC-20 token balance for address {address}: {balance}")
    time.sleep(10)
