### Update `README.md`:

# olas-dev-assignment

## Overview

This project implements an autonomous agent in Python that interacts with the Ethereum blockchain. The agent is designed to continuously consume messages, emit messages, register handlers for processing various message types, and execute proactive behaviors based on its internal state and local time.

## Features

- **Message Handling**: The agent can receive messages from an inbox and process them using registered handlers.
- **Proactive Behavior**: The agent generates random 2-word messages at regular intervals and checks the ERC-20 token balance of a specified Ethereum address.
- **Ethereum Interaction**: Using the `web3.py` library, the agent can check token balances and transfer tokens between addresses based on message content.
- **Inter-Agent Communication**: Two instances of the agent can communicate with each other, where the inbox of one agent serves as the outbox of another.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/axatbhardwaj/olas-dev-assignment.git
   cd olas-dev-assignment
   ```

2. **Create Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:
   - Update the `rpc_url`, `token_address`, `address_1`, `address_2`, and `pvt_key_1` in the `settings.py` file with your actual Ethereum details.
   - The `settings.py` file is used for configuring the project settings.
   - The `abi.py` file is present in the `common` directory and contains the ERC-20 Token ABI.
   - Optionally, set up a dedicated [Tenderly](https://tenderly.co/) fork for safe testing.

## Usage

1. **Run the Agent**:
   Execute the script to start the agent instances. They will begin communicating with each other and interacting with the Ethereum blockchain.

```bash
python -m src.main
```

2. **Monitor Output**:
   The agents will print their activities to stdout, including generated messages, token balance checks, and transfer confirmations.

## Testing

- Unit tests are provided to validate individual components of the agent.
- Integration tests ensure that the agents communicate and process messages correctly.

To run the tests, use:

```bash
python -m unittest
```

## Acknowledgments

- [Tenderly](https://tenderly.co/) for providing a platform to test and debug Ethereum smart contracts.
- [web3.py](https://web3py.readthedocs.io/en/stable/) for simplifying Ethereum interactions in Python.
- look at example.env for the environment variables required.
