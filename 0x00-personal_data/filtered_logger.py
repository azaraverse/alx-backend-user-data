#!/usr/bin/env python3
""" PII Obfuscation """
import logging
from typing import List
import re


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """ Returns a log message while obfuscation PII

    Args:
        fields: All fields in the message to obfuscate
        redaction: string representing obfuscated fields
        message: the log line
        separator: character that separates all fields in the log line
    """
    for field in fields:
        regex = fr'(?<={field}=)[^{separator}]*'
        message = re.sub(regex, redaction, message)
    return message
