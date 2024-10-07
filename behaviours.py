import random
import time
import logging
from queue import Empty

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

    while not agent.stop_event.is_set():
        message_content = f"{random.choice(words)} {random.choice(words)}"
        message = {"sender": agent.id, "content": message_content}
        logging.info(f"Generated message: {message}")
        agent.OutBox.put(message)
        logging.info("Message put in OutBox")
        time.sleep(2)
        logging.info("Sleeping for 2 seconds")

        try:
            # Attempt to get a message from the queue (non-blocking)
            received_message = agent.InBox.get_nowait()
            if received_message == "EXIT":
                break  # Exit the loop if poison pill is received
        except Empty:
            pass  # Continue if no message is available


def check_erc20_balance(agent):
    w3 = get_web3_provider(tenderly_fork_url)
    contract_address = os.getenv("contract_address")
    contract = get_erc20_contract(w3, contract_abi, contract_address)
    account = Account.from_key(agent.private_key)
    address = account.address

    while not agent.stop_event.is_set():
        balance = check_balance(w3, contract, address)
        logging.info(f"ERC-20 token balance for address {address}: {balance}")
        time.sleep(10)

        try:
            received_message = agent.InBox.get_nowait()
            if received_message == "EXIT":
                break
        except Empty:
            pass
