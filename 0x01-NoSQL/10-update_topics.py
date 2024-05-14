#!/usr/bin/env python3
"""
updates a collection.
"""


def update_topics(mongo_collection, name, topics):
    """
    updates a collection.
    """
    mongo_collection.update_one({"name": name}, { "$set": {"topics": topics}})
