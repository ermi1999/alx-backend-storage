#!/usr/bin/env python3
"""
inserts a document.
"""


def insert_school(mongo_collection, **kwargs):
    """
    inserts a document.
    """
    return mongo_collection.insert_one(kwargs).inserted_id
