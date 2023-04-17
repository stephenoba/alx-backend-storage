#!/usr/bin/env python3
"""
Module contain schools_by_topic function
"""


def schools_by_topic(mongo_collection, topic):
    """
    Queries documents that have a specific topic

    Args
    ----
    mongo_collection: Mondo DB collection
    topic: Topic to query for

    Returns
    -------
    A List of a matching documents
    """
    return mongo_collection.find({"topics": topic})
