# kif-parser

WIP KIFパーサー

## KIF から KIFU へ変換

1. 📂`kif` に `*.kif` ファイルをたくさん入れてください
2. ターミナルで `python.exe kif-to-kifu.py` コマンドを実行してください
3. UTF-8形式に変換して 📂`kifu` ファイルに変換されます
4. 読み終えた `kif/*.kif` ファイルは、 `kif-done/*.kif` へ移動されます

## KIFU から KIF へ変換

1. 📂`kifu` に `*.kifu` ファイルをたくさん入れてください
2. ターミナルで `python.exe kifu-to-kif.py` コマンドを実行してください
3. Shift-JIS形式に変換して 📂`kif` ファイルに変換されます
4. 読み終えた `kifu/*.kifu` ファイルは、 `kifu-done/*.kifu` へ移動されます

## KIFU から PIBOT へ変換

1. 📂`kifu` に `*.kifu` ファイルをたくさん入れてください
2. ターミナルで `python.exe kifu-to-pibot.py` コマンドを実行してください
3. JSON形式に変換して 📂`pibot` ファイルに変換されます
4. 読み終えた `kifu/*.kifu` ファイルは、 `kifu-done/*.kifu` へ移動されます
