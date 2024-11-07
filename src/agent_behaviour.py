import asyncio
from web3 import Web3
import random

from .agent import Agent

from common.abi import ERC20_ABI
from src.settings import ETH_SETTINGS, ACCEPTED_TYPES, MESSAGE_WORDS
from datetime import datetime


class ConcreteAgent(Agent):

    # Constructor with its Inbox and Outbox
    def __init__(self, inbox, outbox):
        super().__init__(inbox, outbox)
        # print rpc url
        # print(f"RPC URL: {ETH_SETTINGS['rpc_url']}")
        self.w3 = Web3(Web3.HTTPProvider(ETH_SETTINGS["rpc_url"]))
        # if not self.w3.isConnected(): kill the program
        if not self.w3.is_connected():
            print("Web3 connection failed. Exiting...")
            exit(1)
        self.token_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(ETH_SETTINGS["token_address"]),
            abi=ERC20_ABI,
        )
        self.register_handler("hello", self.handle_hello)
        self.register_handler("crypto", self.handle_crypto)

    # "hello" keyword handler
    def handle_hello(self, message_content):
        print(f"Filtered message (hello): {message_content['content']}")

    # "crypto" keyword & transfer ERC20 handler
    def handle_crypto(self, message_content):
        print(f"Filtered message (crypto): {message_content['content']}")
        print("Transferring ERC-20 token...")
        self.transfer_token()

    # "random message generator" behaviour

    async def generate_random_message(self):
        while True:
            message_content = (
                f"{random.choice(MESSAGE_WORDS)} {random.choice(MESSAGE_WORDS)}"
            )
            type = "message"
            for i in range(len(ACCEPTED_TYPES)):
                if ACCEPTED_TYPES[i] in message_content:
                    type = ACCEPTED_TYPES[i]
                    break
            self.emit_message({"type": type, "content": message_content})
            print(
                f"Generated message:|| {message_content} || at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            # Generates random 2-word messages every 2 seconds.
            await asyncio.sleep(2)

    # "ERC20 balance checker" behaviour
    async def check_balance(self):
        while True:
            balance = self.token_contract.functions.balanceOf(
                self.w3.to_checksum_address(ETH_SETTINGS["address_1"])
            ).call()
            decimals = self.token_contract.functions.decimals().call()
            balance_in_tokens = balance / (10**decimals)
            print(
                f"ERC-20 Token Balance: {balance_in_tokens} tokens at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            # Checks the ERC-20 token balance of an ethereum address every 10 seconds
            await asyncio.sleep(10)

    # transfer token based on current balance
    def transfer_token(self):
        balance = self.token_contract.functions.balanceOf(
            self.w3.to_checksum_address(ETH_SETTINGS["address_1"])
        ).call()
        one_unit = 1 * 10 ** (self.token_contract.functions.decimals().call())
        if balance >= one_unit:
            nonce = self.w3.eth.get_transaction_count(ETH_SETTINGS["address_1"])
            tx = self.token_contract.functions.transfer(
                ETH_SETTINGS["address_2"], one_unit
            ).build_transaction(
                {
                    "nonce": nonce,
                    "gas": 2000000,
                    "gasPrice": self.w3.eth.gas_price,
                    "chainId": self.w3.eth.chain_id,
                }
            )
            signed_tx = self.w3.eth.account.sign_transaction(
                tx, ETH_SETTINGS["pvt_key_1"]
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            _ = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Token transfer sent! Transaction hash: {self.w3.to_hex(tx_hash)}")
        else:
            print("Not enough tokens to transfer.")

    # starts running behaviours continuously
    def start(self):
        # Start behavior tasks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self.generate_random_message())
        loop.create_task(self.check_balance())
        loop.run_forever()
