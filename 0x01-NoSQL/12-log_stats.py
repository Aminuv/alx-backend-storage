#!/usr/bin/env python3
"""
    script that provides some stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient

def print_nginx_request_logs(collection):
    print(f"{collection.count_documents({})} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{count} status check")

def run():
    """ return """
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)

if __name__ == '__main__':
    run()
