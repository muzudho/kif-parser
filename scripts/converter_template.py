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
        self._layer2_file_pattern = None

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

    @property
    def layer2_file_pattern(self):
        return self._layer2_file_pattern

    @layer2_file_pattern.setter
    def layer2_file_pattern(self, file_pattern):
        self._layer2_file_pattern = file_pattern

    def list_layer2_files(self):
        """layer2_folder へコピーした棋譜ファイルへのパスの一覧を返します"""
        layer2_files = glob.glob(self.layer2_file_pattern)
        return layer2_files
