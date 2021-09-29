import hashlib

def create_sha256(binaryData):
    """SHA256のハッシュ値
    Parameters
    ----------
    """
    return hashlib.sha256(binaryData).hexdigest()
