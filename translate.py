import argparse
from scripts.change_place import change_place
from scripts.copy_file import copy_file
from scripts.reversible_convert_kif_to_pivot import ReversibleConvertKifToPivot
from scripts.reversible_convert_kifu_to_pivot import ReversibleConvertKifuToPivot
from scripts.reversible_convert_pivot_to_kif import ReversibleConvertPivotToKif
from scripts.reversible_convert_pivot_to_kifu import ReversibleConvertPivotToKifu


class Translator():
    def __init__(self, source, destination, source_template, destination_template, debug=False):
        self._source = source
        self._destination = destination

        # 入力のジェネレーターを示します
        self._source_template = source_template

        # 出力のジェネレーターを示します
        self._destination_template = destination_template

        self._debug = debug

    def translate_file(self, input_file):
        """WIP 未テスト"""
        to_pivot, from_pivot = Translator._do_it_before_translation(
            source=self._source, destination=self._destination, template=self._destination_template,
            debug=self._debug)
        # TODO 処理
        Translator._translate_file_in_loop(
            input_file, to_pivot, from_pivot, self._debug)

        Translator._do_it_after_translation(from_pivot)

    def translate_files_in_folder(self):
        to_pivot, from_pivot = Translator._do_it_before_translation(
            source=self._source, destination=self._destination, template=self._destination_template,
            debug=self._debug)

        # フォルダー一括処理
        for input_file in to_pivot.outside_input_files():
            Translator._translate_file_in_loop(
                input_file, to_pivot, from_pivot, self._debug)

        Translator._do_it_after_translation(from_pivot)

    @classmethod
    def _do_it_before_translation(clazz, source, destination, template, debug=False):
        """翻訳前にやること"""
        # to-pivot
        if source == 'kifu':
            # KIFUファイルをPIVOTへ変換します
            to_pivot = ReversibleConvertKifuToPivot(
                debug=debug, last_layer_folder='temporary/output-pivot', no_remove_output_pivot=True, template_name=template)
        else:
            # KIFファイルをPIVOTへ変換します
            to_pivot = ReversibleConvertKifToPivot(
                debug=debug, last_layer_folder='temporary/output-pivot', no_remove_output_pivot=True, template_name=template)

        # from-pivot
        if destination == 'kifu':
            # PIVOTファイルをKIFUへ変換します
            from_pivot = ReversibleConvertPivotToKifu(
                debug=debug, first_layer_folder='temporary/output-pivot', template_name=template)
        else:
            # PIVOTファイルをKIFへ変換します
            from_pivot = ReversibleConvertPivotToKif(
                debug=debug, first_layer_folder='temporary/output-pivot', template_name=template)

        # 最終フォルダーを掃除
        to_pivot.clean_last_layer_folder()
        from_pivot.clean_last_layer_folder()

        return to_pivot, from_pivot

    @classmethod
    def _translate_file_in_loop(clazz, input_file, to_pivot, from_pivot, debug=False):
        if debug:
            print(f"[DEBUG] translate.py _translate_file_in_loop(): to_pivot")

        # 入力フォルダ―にあるファイルを、レイヤー２フォルダーにコピーします
        next_file = change_place(to_pivot.layer2_folder, input_file)
        copy_file(input_file, next_file, debug=debug)

        # レイヤー２フォルダーにあるファイルを往復翻訳します
        object_file = to_pivot.round_trip_translate(next_file)
        if not object_file:
            return

        if debug:
            print(f"[DEBUG] translate.py _translate_file_in_loop(): from_pivot")

        # 入力フォルダ―にあるファイルを、レイヤー２フォルダーにコピーします
        next_file = change_place(from_pivot.layer2_folder, object_file)
        copy_file(object_file, next_file, debug=debug)

        # レイヤー２フォルダーにあるファイルを往復翻訳します
        _final_file = from_pivot.round_trip_translate(next_file)

    @classmethod
    def _do_it_after_translation(clazz, from_pivot):
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
        '-t', '--template', default='', help='Destination file Style. ""(Default) or "shogidokoro" or "shogigui".')
    args = parser.parse_args()

    print(f"--debug {args.debug}")
    print(f"-s {args.source}")
    print(f"-d {args.destination}")
    print(f"-t {args.template}")

    # TODO source_template を自動判定したい
    translator = Translator(source=args.source, destination=args.destination,
                            source_template="",
                            destination_template=args.template, debug=args.debug)
    translator.translate_files_in_folder()
