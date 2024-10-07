# Olas Dev Academy Autonomous Agent

This project implements an autonomous agent as part of the Olas Dev Academy enrollment competency assessment. The agent demonstrates asynchronous communication, reactive and proactive behaviors, and interaction with an Ethereum ERC-20 token contract.

## Functionality

The agent exhibits the following key features:

- **Random Message Generation:** Generates random two-word messages every 2 seconds from a predefined list of words.
- **Message Filtering:** Filters messages containing the keywords "hello" and "crypto".
- **"Hello" Message Handling:** Prints "hello" messages to the console.
- **"Crypto" Message Handling:** If the message contains "crypto", the agent interacts with an ERC-20 token contract on a Tenderly fork. It checks the balance of a source address and, if sufficient, transfers 1 token to a target address.
- **Agent Interaction:** Two agent instances are run, with the `OutBox` of one linked to the `InBox` of the other, enabling bidirectional communication.
- **Message Identification:** Each message has a unique ID and sender information, allowing agents to distinguish their own messages from those sent by other agents.
- **ERC-20 Balance Checking:** Periodically checks and prints the ERC-20 token balance of the source Ethereum addresses.

## Architecture

The project follows a modular design:

- **`agent.py`:** Defines the core `Agent` class, responsible for managing the `InBox`, `OutBox`, message handlers, and behaviors.
- **`handlers.py`:** Contains the functions to handle different message types (`handle_hello_message`, `handle_crypto_message`).
- **`behaviours.py`:** Contains the functions for proactive behaviors (`generate_random_message`, `check_erc20_balance`).
- **`my_eth_utils.py`:** Provides utility functions for interacting with the Ethereum blockchain (`get_web3_provider`, `get_erc20_contract`, `check_balance`, `transfer_tokens`).

## Running the Project

1.  **Setup**

    - Create a virtual environment: `python3 -m venv .venv`
    - Activate the environment: `source .venv/bin/activate`
    - Install dependencies: `pip install -r requirements.txt`

2.  **Configuration**

    - Create a dedicated Tenderly fork and obtain the RPC URL.
    - Set environment variables:
      - `rpc_url`: Your Tenderly fork's RPC URL.
      - `pvt_key_1`: Your private key for the source address for agent 1.
      - `pvt_key_2`: Your private key for the source address for agent 2.
      - `reciver_address`: Your target address for the token transfer.

3.  **Execution**

    - Run the `main.py` script: `python main.py`

## Testing

- Unit tests: `python -m unittest tests/test_agent.py`
- Integration tests: `python -m unittest tests/test_integration.py`

## Notes

- This implementation uses `web3.py` for Ethereum interaction.
- Private keys and RPC URLs are retrieved from environment variables for security.
- The project includes unit and integration tests to ensure functionality.
- Logging is implemented to track events and agent state.
- Error handling is included to improve robustness.
- The `check_erc20_balance` behavior runs in a separate thread to ensure it's executed every 10 seconds.
- The program can exit gracefully with Ctrl+C, allowing threads to finish their tasks.
