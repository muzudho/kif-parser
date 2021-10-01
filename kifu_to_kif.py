import glob
import shutil
import os
import codecs


def copy_kifu_from_input(output_folder='temporary/kifu'):
    """inputフォルダーにある `*.kifu` ファイルを kifuフォルダーへコピーします"""

    input_files = glob.glob("./input/*.kifu")
    for input_file in input_files:
        # basename
        try:
            basename = os.path.basename(input_file)
        except:
            print(f"Error: input_file={input_file} except={sys.exc_info()[0]}")
            raise

        copy_file = os.path.join(output_folder, basename)
        shutil.copyfile(input_file, copy_file)


def convert_kifu_to_kif(kifu_file, output_folder='temporary/kif', done_folder='temporary/kifu-done'):
    """(1) kifu_file(*.kifu)ファイルを読み取ります
    (2) *.kifファイルを kif フォルダーへ生成します
    (3) 読み終えた *.kifuファイルは done_folder フォルダーへ移動します

    Returns
    -------
    str
        新しいパス。
        KIFUファイルでなかったなら空文字列
    """

    kif_file = ""

    # シフトJISエンコードのテキストファイルの読み込み
    with codecs.open(kifu_file, "r", encoding='utf-8') as f:

        # basename
        try:
            basename = os.path.basename(kifu_file)
        except:
            print(f"Error: kifu_file={kifu_file} except={sys.exc_info()[0]}")
            raise

        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kifu':
            return ""

        # New file
        kif_file = os.path.join(output_folder, f"{stem}.kif")

        with codecs.open(kif_file, "w", encoding='shift_jis') as fOut:

            # UTF-8形式に変換して保存
            for row in f:
                fOut.write(row)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    doneKifuFile = shutil.move(kifu_file, os.path.join(done_folder, basename))
    return kif_file, doneKifuFile


def main():
    copy_kifu_from_input()

    # KIFUファイル一覧
    kifu_files = glob.glob("./temporary/kifu/*.kifu")
    for kifu_file in kifu_files:
        _kifFile, _donePath = convert_kifu_to_kif(
            kifu_file, output_folder='output')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
