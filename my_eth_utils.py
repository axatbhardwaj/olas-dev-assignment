from web3 import Web3
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_web3_provider(tenderly_fork_url: str) -> Web3:
    try:
        provider = Web3(Web3.HTTPProvider(tenderly_fork_url))
        if provider.is_connected():
            logging.info("Connected to Web3 provider")
        else:
            logging.error("Failed to connect to Web3 provider")
        return provider
    except Exception as e:
        logging.error(f"Error in get_web3_provider: {e}")
        raise


def get_erc20_contract(w3: Web3, contract_abi: str, contract_address: str):
    try:
        checksum_address = Web3.to_checksum_address(contract_address)
        contract = w3.eth.contract(address=checksum_address, abi=contract_abi)
        logging.info("ERC20 contract obtained")
        return contract
    except Exception as e:
        logging.error(f"Error in get_erc20_contract: {e}")
        raise


def check_balance(w3: Web3, contract, address: str) -> int:
    try:
        balance = contract.functions.balanceOf(address).call()
        logging.info(f"Balance for address {address}: {balance}")
        return balance
    except Exception as e:
        logging.error(f"Error in check_balance: {e}")
        raise


def transfer_tokens(w3, contract, source_address, destination_address, amount, private_key):
    # Log the private key retrieval
    logging.info("Retrieving private key for signing the transaction.")

    # Validate the private key
    if private_key is None:
        logging.error("Private key is None. Cannot sign the transaction.")
        raise ValueError("Private key cannot be None.")

    # Retrieve the current nonce for the source address
    nonce = w3.eth.get_transaction_count(source_address)
    logging.info(f"Retrieved nonce for {source_address}: {nonce}")

    # Prepare the transaction for transferring tokens from the contract
    transaction = contract.functions.transfer(
        destination_address,
        amount
    ).build_transaction({
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': nonce,
        'chainId': 1
    })

    try:
        # Sign the transaction
        signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
        logging.info("Transaction signed successfully.")

        # Send the transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logging.info(f"Transaction sent successfully. TX Hash: {
                     tx_hash.hex()}")
        return tx_hash
    except ValueError as e:
        logging.error(f"Error sending transaction: {e}")
        if 'nonce too low' in str(e):
            # Retry with the correct nonce
            nonce = w3.eth.get_transaction_count(source_address)
            logging.info(f"Retrying with updated nonce for {
                         source_address}: {nonce}")
            transaction['nonce'] = nonce
            signed_tx = w3.eth.account.sign_transaction(
                transaction, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            logging.info(f"Transaction sent successfully on retry. TX Hash: {
                         tx_hash.hex()}")
            return tx_hash
        else:
            raise
