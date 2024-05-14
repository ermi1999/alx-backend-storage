#!/usr/bin/env python3
"""
find a scpecific topic in a document.
"""


def schools_by_topic(mongo_collection, topic):
    """
    find a scpecific topic in a document.
    """
    return mongo_collection.find({"topics": topic})
