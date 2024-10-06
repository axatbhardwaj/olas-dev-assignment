import unittest
import threading
import time
from queue import Queue
from agent import Agent
from handlers import handle_hello_message, handle_crypto_message
from behaviours import generate_random_message, check_erc20_balance
import dotenv
import os

dotenv.load_dotenv()


class TestIntegration(unittest.TestCase):

    def test_agent_interaction(self):
        """Test interaction between two agents."""
        agent1 = Agent(os.getenv("pvt_key_1"))
        agent2 = Agent(os.getenv("pvt_key_2"))

        # Register handlers and behaviors
        agent1.register_handler("str", handle_hello_message)
        agent1.register_handler("str", handle_crypto_message)
        agent1.register_behavior(generate_random_message)
        agent1.register_behavior(check_erc20_balance)
        agent2.register_handler("str", handle_hello_message)
        agent2.register_handler("str", handle_crypto_message)
        agent2.register_behavior(generate_random_message)
        agent2.register_behavior(check_erc20_balance)

        # Link OutBoxes and InBoxes
        agent1.OutBox = agent2.InBox
        agent2.OutBox = agent1.InBox

        # Start agents in separate threads
        threading.Thread(target=agent1.run, daemon=True).start()
        threading.Thread(target=agent2.run, daemon=True).start()

        # Give agents time to interact
        time.sleep(5)

        # Assertions (example - check if messages were processed)
        self.assertTrue(agent1.InBox.qsize() > 0)
        self.assertTrue(agent2.InBox.qsize() > 0)
