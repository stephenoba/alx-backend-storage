#!/usr/bin/env python3
"""
Module contains function update_topics"""


def update_topics(mongo_collection, name, topics):
    """
    Update the documents that matches name with topics

    Args
    ----
    mongo_collection: Mongo DB collection
    name: name of ducument
    topics: Topic to update document with

    Returns
    -------
    None
    """
    return mongo_collection.update_one({"name": name}, {"$set": {"topics": topics}})
