import argparse
from scripts.reversible_convert_kif_to_pivot import reversible_convert_kif_to_pivot
from scripts.reversible_convert_kifu_to_pivot import reversible_convert_kifu_to_pivot

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    """
    Example
    -------
    `translate.py -s kifu -d kifu -t "shogidokoro" --debug`
    👆 inputフォルダーの中にあるKIFUファイルを shogidokoroのKIFUファイル形式に変換して outputフォルダーへ出力します。
    --debug フラグを付けると temporaryフォルダーの中に変換過程のファイルが残ります
    """

    # Description
    parser = argparse.ArgumentParser(
        description='Translate .kifu file from -s to -d.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    parser.add_argument(
        '-s', '--source', default='kif', help='Translate from x. "kif"(Default) or "kifu".')
    parser.add_argument(
        '-d', '--destination', default='kif', help='Translate to x. "kif"(Default) or "kifu".')
    parser.add_argument(
        '-t', '--template', default='', help='.kifu Style. ""(Default) or "shogidokoro" or "shogigui".')
    args = parser.parse_args()

    print(f"--debug {args.debug}")
    print(f"-s {args.source}")
    print(f"-d {args.destination}")
    print(f"-t {args.template}")

    if args.source == 'kifu':
        # KIFUファイルをPIVOTへ変換します
        reversible_convert_kifu_to_pivot(
            debug=args.debug, last_layer_folder='./temporary/output-pivot', no_remove_output_pivot=True, template_name=args.template)
    else:
        # KIFファイルをPIVOTへ変換します
        reversible_convert_kif_to_pivot(
            debug=args.debug, last_layer_folder='./temporary/output-pivot', no_remove_output_pivot=True, template_name=args.template)