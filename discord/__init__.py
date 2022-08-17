"""
A work in progress discord wrapper built from scratch
"""

from sys import version_info

if version_info < (3, 9):
	raise Exception("Python >= 3.9 is required.")

from .api.intents import Intents
from .client import Client
from .embeds import Embed
from .message import Message
