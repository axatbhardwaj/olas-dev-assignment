from json import load
import os

from dotenv import load_dotenv

load_dotenv()

ACCEPTED_TYPES = ["hello", "crypto"]
# Define the MESSAGE_WORDS for message generation
MESSAGE_WORDS = [
    "hello",
    "sun",
    "world",
    "space",
    "moon",
    "crypto",
    "sky",
    "ocean",
    "universe",
    "human",
]

# Ethereum settings
ETH_SETTINGS = {
    "rpc_url": os.getenv("rpc_url"),
    "address_1": os.getenv("address_1"),
    "address_2": os.getenv("address_2"),
    "pvt_key_1": os.getenv("pvt_key_1"),
    "token_address": os.getenv("token_address"),
}