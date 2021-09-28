import glob
from kifu_to_pibot import parse_kifu_file_to_pibot
from kif_to_kifu import convert_kif_to_kifu_file

def main():
    # KIFファイル一覧
    files = glob.glob("./kif/*")
    for file in files:
        outPath, _donePath = convert_kif_to_kifu_file(file)
        print(f'kifu={outPath}')

        if outPath:
            _outPath, _donePath = parse_kifu_file_to_pibot(outPath)

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
