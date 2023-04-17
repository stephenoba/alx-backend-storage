#!/usr/bin/env python3
"""
Module contains insert_school function
"""


def insert_school(mongo_collection, **kwargs):
    """
    inserts a new document in a collection

    Args
    ----
    mongo_collection: Mongo DB collection
    kwargs: Arguments for document to be inserted

    Returns
    -------
    The ID of the newly inserted document
    """
    doc = mongo_collection.insert_one(kwargs)
    return doc.inserted_id
