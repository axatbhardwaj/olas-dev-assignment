from agent import Agent
from handlers import handle_hello_message, handle_crypto_message
from behaviours import generate_random_message, check_erc20_balance
import threading
from queue import Queue, Empty
import dotenv
import os
import logging
import time
import signal

dotenv.load_dotenv()

# Global flag to indicate if the program should exit
exit_flag = False


def signal_handler(signum, frame):
    global exit_flag
    exit_flag = True
    raise KeyboardInterrupt()


if __name__ == "__main__":
    private_key_1 = os.getenv("pvt_key_1")
    private_key_2 = os.getenv("pvt_key_2")

    if private_key_1 is None or private_key_2 is None:
        logging.error("Private keys are not set in the environment variables.")
        exit(1)

    message_queue = Queue()

    agent1 = Agent(private_key=private_key_1, message_queue=message_queue)
    agent2 = Agent(private_key=private_key_2, message_queue=message_queue)

    agent1.register_handler("hello", handle_hello_message)
    agent1.register_handler("crypto", handle_crypto_message)
    agent1.register_behavior(generate_random_message)

    agent2.register_handler("hello", handle_hello_message)
    agent2.register_handler("crypto", handle_crypto_message)
    agent2.register_behavior(generate_random_message)

    agent1.OutBox = agent2.InBox
    agent2.OutBox = agent1.InBox

    agent1_thread = threading.Thread(target=agent1.run)
    agent2_thread = threading.Thread(target=agent2.run)
    agent1_thread.start()
    agent2_thread.start()

    def display_messages():
        while not exit_flag:
            try:
                message = message_queue.get(timeout=1)
                print(f"Received message: {message}")
            except Empty:
                continue
            except KeyboardInterrupt:
                break

    display_thread = threading.Thread(target=display_messages)
    display_thread.start()

    balance_thread_1 = threading.Thread(
        target=check_erc20_balance, args=(agent1,))
    balance_thread_2 = threading.Thread(
        target=check_erc20_balance, args=(agent2,))
    balance_thread_1.start()
    balance_thread_2.start()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        while not exit_flag:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting immediately...")
        agent1.stop_event.set()
        agent2.stop_event.set()
        agent1_thread.join()
        agent2_thread.join()
        balance_thread_1.join()
        balance_thread_2.join()
        display_thread.join()
        logging.info("Exiting...")
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
    finally:
        logging.info("Exiting...")
