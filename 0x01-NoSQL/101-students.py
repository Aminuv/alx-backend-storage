#!/usr/bin/env python3
"""
    The top students
"""


def top_students(mongo_collection):
    """ returns all students """
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
