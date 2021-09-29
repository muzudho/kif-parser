import os
import glob
import json
from collections import OrderedDict
import pprint

def convert_pibot_to_kifu(pibotFile):
    # basename
    basename = os.path.basename(pibotFile)
    _stem, extention = os.path.splitext(basename)
    if extention.lower() != '.json':
        return None, None

    with open(pibotFile) as f:
        text = f.read()
        data = json.loads(text)
        pprint.pprint(data, width=40)

    # TODO pibotFile を pibot-done へ移動したい

    # TODO kifuファイルを出力したい
    return None, None

def main():
    # KIFファイル一覧
    pibotFiles = glob.glob("./pibot/*")
    for pibotFile in pibotFiles:
        _kifuFile, _doneKifuFile = convert_pibot_to_kifu(pibotFile)

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
