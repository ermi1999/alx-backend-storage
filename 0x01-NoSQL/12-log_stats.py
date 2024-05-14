#!/usr/bin/env python3
"""
finds some log status.
"""
from pymongo import MongoClient


client = MongoClient('mongodb://127.0.0.1:27017')
collection = client.logs.nginx

logs = collection.estimated_document_count()
methods = {
        "GET": collection.count_documents({"method": "GET"}),
        "POST": collection.count_documents({"method": "POST"}),
        "PUT": collection.count_documents({"method": "PUT"}),
        "PATCH": collection.count_documents({"method": "PATCH"}),
        "DELETE": collection.count_documents({"method": "DELETE"})
    }
status_checks = collection.count_documents({"method": "GET", "path": "/status"})

print("{} logs".format(logs))
print("Methods:")
for key, value in methods.items():
    print("\tmethod {}: {}".format(key, value))
print("{} status check".format(status_checks))
