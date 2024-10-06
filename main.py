from agent import Agent
from handlers import handle_hello_message, handle_crypto_message
from behaviours import generate_random_message, check_erc20_balance
import threading
import dotenv
import os
import logging

dotenv.load_dotenv()

if __name__ == "__main__":
    # Initialize agents with private keys from environment variables
    private_key_1 = os.getenv("pvt_key_1")
    private_key_2 = os.getenv("pvt_key_2")

    if private_key_1 is None or private_key_2 is None:
        logging.error("Private keys are not set in the environment variables.")
        exit(1)

    agent1 = Agent(private_key=private_key_1)
    agent2 = Agent(private_key=private_key_2)

    agent1.register_handler("str", handle_hello_message)
    agent1.register_handler("str", handle_crypto_message)
    agent1.register_behavior(generate_random_message)
    agent1.register_behavior(check_erc20_balance)

    agent2.register_handler("str", handle_hello_message)
    agent2.register_handler("str", handle_crypto_message)
    agent2.register_behavior(generate_random_message)
    agent2.register_behavior(check_erc20_balance)

    # Link agent1's OutBox to agent2's InBox and vice versa
    agent1.OutBox = agent2.InBox
    agent2.OutBox = agent1.InBox

    # Run the agents using threads for concurrency
    threading.Thread(target=agent1.run).start()
    threading.Thread(target=agent2.run).start()
