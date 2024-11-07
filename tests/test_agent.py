import unittest
from unittest.mock import patch
from queue import Queue
from src.main import ConcreteAgent


class TestConcreteAgent(unittest.TestCase):
    def setUp(self):
        inbox = Queue()
        outbox = Queue()
        self.agent = ConcreteAgent(inbox, outbox)

    @patch("builtins.print")
    def test_handle_hello(self, mock_print):
        # Simulate receiving a message containing "hello"
        message = {"type": "hello", "content": "hello world"}
        self.agent.handle_hello(message)

        # Check if the print function was called with the correct message
        mock_print.assert_called_once_with("Filtered message (hello): hello world")


if __name__ == "__main__":
    unittest.main()
