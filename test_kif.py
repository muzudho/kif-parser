import glob
from scripts.test_lib import create_sha256
from kif_to_pibot import convert_kif_to_pibot

def main():
    # KIFファイル一覧
    kifFiles = glob.glob("./kif/*")
    for kifFile in kifFiles:

        # 読み取り専用、バイナリ
        with open(kifFile, 'rb') as f:
            kifBinary = f.read()

            # print(binaryData)

            # ファイルをバイナリ形式で読み込んで SHA256 生成
            kifSha256 = create_sha256(kifBinary)
            print(f"kifSha256={kifSha256}")

            # kif -> pibot 変換
            _pibotFile, _doneKifFile = convert_kif_to_pibot(kifFile)

            # TODO pibot -> kif 変換

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
