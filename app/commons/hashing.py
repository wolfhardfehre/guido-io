import hashlib


def md5_hash(query: str):
    md5 = hashlib.md5()
    md5.update(query.encode('utf-8'))
    return md5.hexdigest()
