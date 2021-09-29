import glob
from scripts.test_lib import create_sha256

def main():
    # KIFファイル一覧
    files = glob.glob("./kif/*")
    for file in files:

        # 読み取り専用、バイナリ
        with open(file, 'rb') as f:
            binaryData = f.read()

            # print(binaryData)

            # ファイルをバイナリ形式で読み込んで SHA256 生成
            sha256 = create_sha256(binaryData)
            print(f"sha256={sha256}")

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
