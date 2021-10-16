import argparse

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    """
    Example
    -------
    `translate.py -s "./input/20211002_223506_KifuwarabeW31B22vsKifuwarabeW31B22[shogigui].kifu" -d "./output/20211002_223506_KifuwarabeW31B22vsKifuwarabeW31B22[shogidokoro].kifu" -t "shogidokoro"`
    """

    # Description
    parser = argparse.ArgumentParser(
        description='Translate .kifu file from -s to -d.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '-s', '--source', help='Translate from x.')
    parser.add_argument(
        '-d', '--destination', help='Translate to x.')
    parser.add_argument(
        '-t', '--template', default='shogidokoro', help='.kifu Style. "shogidokoro"(Default) or "shogigui".')
    args = parser.parse_args()

    print(f"-s {args.source}")
    print(f"-d {args.destination}")
    print(f"-t {args.template}")
