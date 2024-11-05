
# Parent Agent class
class Agent:
    def __init__(self, inbox, outbox):
        self.inbox = inbox
        self.outbox = outbox
        self.handlers = {}

    # Parent has info of all handlers
    def register_handler(self, message_type, handler):
        self.handlers[message_type] = handler

    # Setting Outbox message
    def emit_message(self, message):
        self.outbox.put(message)

    # Process Inbox message
    def process_inbox(self):
        while True:
            message = self.inbox.get()
            if message is None:  # Shutdown signal
                break
            message_type = message.get('type')
            if message_type in self.handlers:
                self.handlers[message_type](message)
