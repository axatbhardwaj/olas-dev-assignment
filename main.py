from agent import Agent
from handlers import handle_hello_message, handle_crypto_message
from behaviours import generate_random_message, check_erc20_balance
import threading
import dotenv
import os
import logging
from queue import Queue
import time
import signal

dotenv.load_dotenv()

# Global flag to indicate if the program should exit
exit_flag = False


def signal_handler(signum, frame):
    global exit_flag
    exit_flag = True


if __name__ == "__main__":
    # Initialize agents with private keys from environment variables
    private_key_1 = os.getenv("pvt_key_1")
    private_key_2 = os.getenv("pvt_key_2")

    if private_key_1 is None or private_key_2 is None:
        logging.error("Private keys are not set in the environment variables.")
        exit(1)

    # Create a shared queue for messages
    message_queue = Queue()

    agent1 = Agent(private_key=private_key_1, message_queue=message_queue)
    agent2 = Agent(private_key=private_key_2, message_queue=message_queue)

    # Correctly register handlers with "hello" and "crypto" keys
    # Changed from "str" to "hello"
    agent1.register_handler("hello", handle_hello_message)
    # Changed from "str" to "crypto"
    agent1.register_handler("crypto", handle_crypto_message)
    agent1.register_behavior(generate_random_message)

    # Changed from "str" to "hello"
    agent2.register_handler("hello", handle_hello_message)
    # Changed from "str" to "crypto"
    agent2.register_handler("crypto", handle_crypto_message)
    agent2.register_behavior(generate_random_message)

    # Link agent1's OutBox to agent2's InBox and vice versa
    agent1.OutBox = agent2.InBox
    agent2.OutBox = agent1.InBox

    # Run the agents in separate threads for concurrency
    thread1 = threading.Thread(target=agent1.run)
    thread2 = threading.Thread(target=agent2.run)
    thread1.start()
    thread2.start()

    # Function to display messages from the queue in stdout
    def display_messages():
        while not exit_flag:  # Check for exit flag
            message = message_queue.get()
            print(f"Received message: {message}")

    # Start a thread to display messages
    display_thread = threading.Thread(target=display_messages)
    display_thread.start()

    # Create separate threads for balance checking behavior
    balance_thread_1 = threading.Thread(
        target=check_erc20_balance, args=(agent1,))
    balance_thread_2 = threading.Thread(
        target=check_erc20_balance, args=(agent2,))
    balance_thread_1.start()
    balance_thread_2.start()

    # Register signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    # Keep the main thread alive until exit signal
    while not exit_flag:
        time.sleep(1)

    # Signal the agent threads to stop
    agent1.stop()
    agent2.stop()

    # Wait for the threads to finish
    thread1.join()
    thread2.join()
    display_thread.join()
    balance_thread_1.join()
    balance_thread_2.join()

    print("Exiting gracefully...")
