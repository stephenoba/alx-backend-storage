#!/usr/bin/env python3
"""
Module  contains  function list_all
"""


def list_all(mongo_collection):
    """
    list all documents in a collection

    Args
    ----
    mongo_collection: A mongodb collection

    Returns
    -------
    Returns a list of all documents in collection
    """
    return mongo_collection.find()
