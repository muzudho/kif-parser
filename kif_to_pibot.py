import glob
from kifu_to_pibot import convert_kifu_file_to_pibot
from kif_to_kifu import convert_kif_to_kifu_file


def convert_kif_to_pibot(kifFile):
    kifuFile, doneKifFile = convert_kif_to_kifu_file(kifFile)
    # print(f'kifu={kifuFile}')

    if kifuFile:
        pibotFile, _doneKifuFile = convert_kifu_file_to_pibot(kifuFile)
        # print(f'kifu={kifuFile} pibot={pibotFile}')
        return pibotFile, doneKifFile

    return None, None, None


def main():
    # KIFファイル一覧
    kifFiles = glob.glob("./kif/*")
    for kifFile in kifFiles:
        _pibotFile, _doneKifFile = convert_kif_to_pibot(kifFile)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
