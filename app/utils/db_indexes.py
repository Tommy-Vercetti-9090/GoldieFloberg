import pymongo


def indexes(db):
    db["User"].create_index("email", unique=True)
    db["Profile"].create_index("user_id", unique=True)
