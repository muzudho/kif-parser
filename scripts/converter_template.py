import glob
import shutil
import os
import sys
from remove_all_output import remove_all_output


class ConverterTemplate():
    def __init__(self):
        self._last_layer_folder_clean = False
        self._last_layer_folder_clean_echo = False
        self._firlst_layer_file_pattern = None
        self._layer2_folder = None

    @property
    def last_layer_folder_clean(self):
        return self._last_layer_folder_clean

    @last_layer_folder_clean.setter
    def last_layer_folder_clean(self, enabled):
        self._last_layer_folder_clean = enabled

    @property
    def last_layer_folder_clean_echo(self):
        return self._last_layer_folder_clean_echo

    @last_layer_folder_clean_echo.setter
    def last_layer_folder_clean_echo(self, enabled):
        self._last_layer_folder_clean_echo = enabled

    @property
    def firlst_layer_file_pattern(self):
        return self._firlst_layer_file_pattern

    @firlst_layer_file_pattern.setter
    def firlst_layer_file_pattern(self, file_pattern):
        self._firlst_layer_file_pattern = file_pattern

    @property
    def layer2_folder(self):
        return self._layer2_folder

    @layer2_folder.setter
    def layer2_folder(self, layer2_folder):
        self._layer2_folder = layer2_folder

    def convert_before_loop(self):
        # 1. 出力フォルダーを空っぽにします
        if self._last_layer_folder_clean:
            remove_all_output(echo=False)

        if self.firlst_layer_file_pattern is None or self.layer2_folder is None:
            return

        # 2. inputフォルダーにある ? ファイルを layer2_folder へコピーします
        self.__copy_files_to_folder(
            self.firlst_layer_file_pattern, self.layer2_folder)

        pass

    def __copy_files_to_folder(self, input_file_pattern, output_folder):

        input_files = glob.glob(input_file_pattern)
        for input_file in input_files:
            # basename
            try:
                basename = os.path.basename(input_file)
            except:
                print(
                    f"Error: input_file={input_file} except={sys.exc_info()[0]}")
                raise

            copy_file = os.path.join(output_folder, basename)
            shutil.copyfile(input_file, copy_file)
