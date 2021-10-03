import hashlib


def create_sha256(binary_data):
    """SHA256のハッシュ値
    Parameters
    ----------
    binary_data : binary
        バイナリー形式
    """
    return hashlib.sha256(binary_data).hexdigest()


def create_sha256_by_file_path(file):
    """SHA256のハッシュ値
    Parameters
    ----------
    file : str
        ファイル パス
    """

    # 読み取り専用、バイナリ
    with open(file, 'rb') as f:
        binary_data = f.read()

    # print(binary_data)

    return create_sha256(binary_data)
