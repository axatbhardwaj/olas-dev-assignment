import logging
import time
from typing import Callable, List, Any
from queue import Queue
import uuid
import concurrent.futures

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Agent:
    def __init__(self, private_key: str, message_queue: Queue):
        self.id = uuid.uuid4()  # Unique ID for the agent
        self.InBox: Queue = Queue()
        self.OutBox: Queue = message_queue  # Shared queue for output
        self.handlers: dict = {}
        self.behaviors: List[Callable] = []
        self.private_key = private_key
        self.sent_message_ids = set()  # To store IDs of sent messages
        logging.info("Agent initialized")

    def register_handler(self, message_type: str, handler_function: Callable):
        self.handlers[message_type] = lambda message: handler_function(
            message, self.private_key
        )
        logging.info(f"Handler registered for message type: {message_type}")

    def register_behavior(self, behavior_function: Callable):
        self.behaviors.append(behavior_function)
        logging.info("Behavior registered")

    def process_message(self, message: Any):
        # Check if the message was not sent by this agent
        if message["sender"] != self.id:
            logging.info(
                f"Processing message of type: {
                    type(message['content']).__name__}"
            )
            if "hello" in message["content"]:
                self.handlers["hello"](message["content"])
            elif "crypto" in message["content"]:
                self.handlers["crypto"](message["content"])
        else:
            logging.info("Ignoring message sent by self.")

    def run(self):
        logging.info("Agent started running")
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                if not self.InBox.empty():
                    message = self.InBox.get()
                    logging.info("Message retrieved from InBox")
                    self.process_message(message)
                for behavior in self.behaviors:
                    executor.submit(behavior, self)
                logging.info("Behaviors executed")
                time.sleep(2)
