#!/usr/bin/env python3
"""
Script provides some stats about Nginx logs
stored in mongodb
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    total_doc = nginx_collection.count_documents({})
    total_get = nginx_collection.count_documents({"method": "GET"})
    total_post = nginx_collection.count_documents({"method": "POST"})
    total_put = nginx_collection.count_documents({"method": "PUT"})
    total_patch = nginx_collection.count_documents({"method": "PATCH"})
    total_delete = nginx_collection.count_documents({"method": "DELETE"})
    total_get_path = nginx_collection.count_documents(
        {'method': 'GET', 'path': '/status'})

    print(f'{total_doc} logs')
    print('Methods:')
    print(f'\tmethod GET: {total_get}')
    print(f'\tmethod POST: {total_post}')
    print(f'\tmethod PUT: {total_put}')
    print(f'\tmethod PATCH: {total_patch}')
    print(f'\tmethod DELETE: {total_delete}')
    print(f'{total_get_path} status check')

    top_ips = nginx_collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    print("IPs:")
    for top_ip in top_ips:
        ip = top_ip.get("ip")
        count = top_ip.get("count")
        print(f'\t{ip}: {count}')
