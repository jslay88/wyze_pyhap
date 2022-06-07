"""Wyze PyHAP, Wyze HomeKit Bridge Accessory implementation via HAP-python"""
import logging
import os


__version__ = "2.3.1" + os.getenv("VERSION_TAG", "")

logging.getLogger(__name__).addHandler(logging.NullHandler())
