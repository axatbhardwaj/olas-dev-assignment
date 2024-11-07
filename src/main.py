import time
from queue import Queue
from threading import Thread
from src.agent_behaviour import ConcreteAgent


def setUpTask():
    # Create message queues
    inbox1 = Queue()
    outbox1 = Queue()
    inbox2 = Queue()
    outbox2 = Queue()

    # Instantiate agents
    agent1 = ConcreteAgent(inbox1, outbox1)
    agent2 = ConcreteAgent(inbox2, outbox2)

    # Start processing messages in threads
    Thread(target=agent1.process_inbox, daemon=True).start()
    Thread(target=agent2.process_inbox, daemon=True).start()

    # Start the agents' behaviors
    Thread(target=agent1.start, daemon=True).start()
    Thread(target=agent2.start, daemon=True).start()

    # Connect the agents' inboxes and outboxes
    while True:
        # Relay messages between agents
        if not outbox1.empty():
            message = outbox1.get()
            inbox2.put(message)

        if not outbox2.empty():
            message = outbox2.get()
            inbox1.put(message)

        time.sleep(1)


if __name__ == "__main__":
    setUpTask()
