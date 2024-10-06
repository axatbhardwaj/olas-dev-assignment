import unittest
from unittest.mock import patch, Mock
from queue import Queue
from agent import Agent
from handlers import handle_hello_message, handle_crypto_message
from behaviours import generate_random_message, check_erc20_balance
import dotenv
import os

dotenv.load_dotenv()


class TestAgent(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.agent = Agent(os.getenv("pvt_key_1")
                           )  # Initialize with a dummy private key

    def test_register_handler(self):
        """Test handler registration."""
        self.agent.register_handler("str", handle_hello_message)
        self.assertIn("str", self.agent.handlers)

    def test_register_behavior(self):
        """Test behavior registration."""
        self.agent.register_behavior(generate_random_message)
        self.assertIn(generate_random_message, self.agent.behaviors)

    @patch("handlers.get_web3_provider")
    @patch("handlers.get_erc20_contract")
    @patch("handlers.check_balance")
    @patch("handlers.transfer_tokens")
    def test_handle_crypto_message(self, mock_transfer, mock_check_balance,
                                   mock_get_contract, mock_get_provider):
        """Test crypto message handling."""
        mock_get_provider.return_value = Mock()  # Mock provider
        mock_get_contract.return_value = Mock()  # Mock contract
        mock_check_balance.return_value = 10  # Sufficient balance
        self.agent.register_handler("str", handle_crypto_message)
        self.agent.process_message("crypto test")
        mock_transfer.assert_called_once()  # Transfer should be called

    @patch("behaviours.get_web3_provider")
    @patch("behaviours.get_erc20_contract")
    @patch("behaviours.check_balance")
    def test_check_erc20_balance(self, mock_check_balance, mock_get_contract,
                                 mock_get_provider):
        """Test ERC-20 balance checking."""
        mock_get_provider.return_value = Mock()  # Mock provider
        mock_get_contract.return_value = Mock()  # Mock contract
        check_erc20_balance(self.agent)
        mock_check_balance.assert_called_once()  # assert_checed_once(est_generate_random_message(self):
        """Test random message generation."""
        with patch.object(self.agent.OutBox, 'put') as mock_put:
            generate_random_message(self.agent)
            mock_put.assert_called_once()  # Put should be called
