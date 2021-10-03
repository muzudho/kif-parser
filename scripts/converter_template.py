from remove_all_output import remove_all_output


class ConverterTemplate():
    def __init__(self):
        self.__output_folder_clean = False
        self.__output_folder_clean_echo = False

    @property
    def output_folder_clean(self):
        return self.__output_folder_clean

    @output_folder_clean.setter
    def output_folder_clean(self, enabled):
        self.__output_folder_clean = enabled

    @property
    def output_folder_clean_echo(self):
        return self.__output_folder_clean_echo

    @output_folder_clean_echo.setter
    def output_folder_clean_echo(self, enabled):
        self.__output_folder_clean_echo = enabled

    def convert(self):
        if self.__output_folder_clean:
            remove_all_output(echo=False)

        pass
