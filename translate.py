import argparse
from scripts.change_place import change_place
from scripts.copy_file import copy_file
from scripts.reversible_convert_kif_to_pivot import ReversibleConvertKifToPivot
from scripts.reversible_convert_kifu_to_pivot import ReversibleConvertKifuToPivot
from scripts.reversible_convert_pivot_to_kif import ReversibleConvertPivotToKif
from scripts.reversible_convert_pivot_to_kifu import ReversibleConvertPivotToKifu


def translate(source, destination, template, debug):
    if debug:
        print(f"[DEBUG] translate.py translate(): to_pivot")

    if source == 'kifu':
        # KIFUファイルをPIVOTへ変換します
        to_pivot = ReversibleConvertKifuToPivot(
            debug=debug, last_layer_folder='temporary/output-pivot', no_remove_output_pivot=True, template_name=template)
    else:
        # KIFファイルをPIVOTへ変換します
        to_pivot = ReversibleConvertKifToPivot(
            debug=debug, last_layer_folder='temporary/output-pivot', no_remove_output_pivot=True, template_name=template)

    to_pivot.clean_last_layer_folder()

    for input_file in to_pivot.outside_input_files():
        copy = change_place(to_pivot.layer2_folder, input_file)
        copy_file(input_file, copy, debug=debug)

    for input_file in to_pivot.target_files():
        to_pivot.round_trip_translate(input_file)
    to_pivot.clean_temporary()

    if debug:
        print(f"[DEBUG] translate.py translate(): from_pivot")

    if destination == 'kifu':
        # PIVOTファイルをKIFUへ変換します
        from_pivot = ReversibleConvertPivotToKifu(
            debug=debug, first_layer_folder='temporary/output-pivot', template_name=template)
    else:
        # PIVOTファイルをKIFへ変換します
        from_pivot = ReversibleConvertPivotToKif(
            debug=debug, first_layer_folder='temporary/output-pivot', template_name=template)

    from_pivot.clean_last_layer_folder()

    for input_file in from_pivot.outside_input_files():
        # 入力フォルダ―にあるファイルを、レイヤー２フォルダーにコピーします
        next_file = change_place(from_pivot.layer2_folder, input_file)
        copy_file(input_file, next_file, debug=debug)

        # レイヤー２フォルダーにあるファイルを往復翻訳します
        from_pivot.round_trip_translate(next_file)

    from_pivot.clean_temporary()


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

    translate(source=args.source, destination=args.destination,
              template=args.template, debug=args.debug)
