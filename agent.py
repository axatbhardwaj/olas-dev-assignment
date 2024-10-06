import logging
from typing import Callable, List, Any
from queue import Queue

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Agent:
    def __init__(self, private_key: str):
        self.InBox: Queue = Queue()
        self.OutBox: Queue = Queue()
        self.handlers: dict = {}
        self.behaviors: List[Callable] = []
        self.private_key = private_key
        logging.info("Agent initialized")

    def register_handler(self, message_type: str, handler_function: Callable):
        self.handlers[message_type] = handler_function
        logging.info(f"Handler registered for message type: {message_type}")

    def register_behavior(self, behavior_function: Callable):
        self.behaviors.append(behavior_function)
        logging.info("Behavior registered")

    def process_message(self, message: Any):
        message_type = type(message).__name__
        logging.info(f"Processing message of type: {message_type}")
        if message_type in self.handlers:
            handler = self.handlers[message_type]
            logging.info(f"Invoking handler for message type: {message_type}")
            if handler.__code__.co_argcount == 1:
                handler(message)
            else:
                handler(message, self.private_key)
            logging.info(f"Handler executed for message type: {message_type}")
        else:
            logging.warning(
                f"No handler found for message type: {message_type}")

    def run(self):
        logging.info("Agent started running")
        while True:
            if not self.InBox.empty():
                message = self.InBox.get()
                logging.info("Message retrieved from InBox")
                self.process_message(message)
            for behavior in self.behaviors:
                behavior(self)
                logging.info("Behavior executed")
