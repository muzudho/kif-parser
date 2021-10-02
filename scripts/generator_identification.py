import re


class GeneratorIdentification():
    """棋譜を生成したソフトらしさを類推します"""

    def __init__(self):
        # Example: `   1 ７六歩(77)        ( 0:00/00:00:00)` の `( 0:00/00:00:00)` の部分を当てにいきます
        self._shogi_gui_time_stamp = re.compile(
            r"^.*\(\s\d:\d{2}/\d{2}:\d{2}:\d{2}\)$")

        pass

    def read_all_text(self, text):
        """テキストを読込ませてください"""

        shogi_gui_time_stamp_flag = False

        lines = text.split('\n')
        for line in lines:
            result = self._shogi_gui_time_stamp.match(line)
            if result:
                shogi_gui_time_stamp_flag = True
            pass

        shogi_dokoro = 1
        shogi_gui = 0

        if shogi_gui_time_stamp_flag:
            shogi_gui += 10

        return shogi_dokoro, shogi_gui


generator_identification = GeneratorIdentification()
