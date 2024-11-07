import unittest
from unittest.mock import patch
from threading import Thread
from src.main import ConcreteAgent
from queue import Queue


class TestRelay(unittest.TestCase):
    def setUp(self) -> None:
        self.inbox1 = Queue()
        self.outbox1 = Queue()
        self.inbox2 = Queue()
        self.outbox2 = Queue()

        self.agent1 = ConcreteAgent(self.inbox1, self.outbox1)
        self.agent2 = ConcreteAgent(self.inbox2, self.outbox2)

        Thread(target=self.agent1.process_inbox, daemon=True).start()
        Thread(target=self.agent2.process_inbox, daemon=True).start()

    def test_message_relay_between_agents(self):
        # # Agent 1 sends a message
        message = {"type": "message", "content": "hello crypto"}
        self.outbox1.put(message)

        # Relay messages between agents
        if not self.outbox1.empty():
            message = self.outbox1.get()
            self.inbox2.put(message)

        with patch("builtins.print") as mock_print:
            if not self.inbox2.empty():
                received_message = self.inbox2.get()
                self.agent2.handle_hello(received_message)

            # Ensure the agent 2 processes the 'hello' message
            mock_print.assert_called_once_with("Filtered message (hello): hello crypto")


if __name__ == "__main__":
    unittest.main()
