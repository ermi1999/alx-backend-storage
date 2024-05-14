#!/usr/bin/env python3
"""
finds some log status.
"""
from pymongo import MongoClient


if __name__ == "__main__":
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
    status_checks = collection.count_documents(
            {"method": "GET", "path": "/status"})

    print("{} logs".format(logs))
    print("Methods:")
    for key, value in methods.items():
        print("\tmethod {}: {}".format(key, value))
    print("{} status check".format(status_checks))

    sorted_ips = collection.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    print("IPs:")
    i = 0
    for s in sorted_ips:
        if i == 10:
            break
        print(f"\t{s.get('_id')}: {s.get('count')}")
        i += 1
