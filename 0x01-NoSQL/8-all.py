#!/usr/bin/env python3
"""
returns all documents in a collection.
"""


def list_all(mongo_collection):
    """
    function for getting all documents in a collection.
    """
    return mongo_collection.find()
