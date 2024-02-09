#!/usr/bin/env python3
"""
Main file
"""

import logging

get_logger = __import__('filtered_logger').get_logger
main = __import__('filtered_logger').main

main()