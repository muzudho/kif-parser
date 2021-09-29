# kif-parser

WIP KIFパーサー、コンバーター  

**DANGER:** このパーサーは、このプロジェクトの各📂フォルダーに入れたファイルを壊し得ます。棋譜ファイルはバックアップを取って使ってください。  

![20210929shogi7-kif.png](docs/img/20210929shogi7-kif-50per.png)  
👆　.kif file (kif ←→ kifu), (kif → PIBOT)  

![20210929shogi8-kifu.png](docs/img/20210929shogi8-kifu-50per.png)  
👆　.kifu file (kifu ←→ kif), (kifu → PIBOT)  

![20210930shogi10-pibot-50per.png](docs/img/20210930shogi10-pibot-50per.png)  
👆　PIBOT (.json file. Unofficial format, Not permanent save format. Work in progress)  

## KIF から KIFU へ変換

1. 注意。消えると困るオリジナルの棋譜ファイルは 別のところに保存しておいてください
2. 📂`kif` に `*.kif` ファイルをたくさん入れてください
3. ターミナルで `python.exe kif_to_kifu.py` コマンドを実行してください
4. UTF-8形式に変換して 📂`kifu` へ出力されます
5. 読み終えた `kif/*.kif` ファイルは、 `kif-done/*.kif` へ移動されます

## KIFU から KIF へ変換

1. 注意。消えると困るオリジナルの棋譜ファイルは 別のところに保存しておいてください
2. 📂`kifu` に `*.kifu` ファイルをたくさん入れてください
3. ターミナルで `python.exe kifu_to_kif.py` コマンドを実行してください
4. Shift-JIS形式に変換して 📂`kif` へ出力されます
5. 読み終えた `kifu/*.kifu` ファイルは、 `kifu-done/*.kifu` へ移動されます

## KIF から PIBOT へ変換

1. 注意。消えると困るオリジナルの棋譜ファイルは 別のところに保存しておいてください
2. 📂`kif` に `*.kif` ファイルをたくさん入れてください
3. ターミナルで `python.exe kif_to_pibot.py` コマンドを実行してください
4. JSON形式に変換して 📂`pibot` へ出力されます
5. 読み終えた `kif/*.kif` ファイルは、 `kif-done/*.kif` へ移動されます
6. PIBOT ファイル形式は永続保存に適しません。使い終わったら削除しましょう

## KIFU から PIBOT へ変換

1. 注意。消えると困るオリジナルの棋譜ファイルは 別のところに保存しておいてください
2. 📂`kifu` に `*.kifu` ファイルをたくさん入れてください
3. ターミナルで `python.exe kifu_to_pibot.py` コマンドを実行してください
4. JSON形式に変換して 📂`pibot` へ出力されます
5. 読み終えた `kifu/*.kifu` ファイルは、 `kifu-done/*.kifu` へ移動されます
6. PIBOT ファイル形式は永続保存に適しません。使い終わったら削除しましょう

## PIBOT から KIF へ変換

1. 注意。消えると困るオリジナルの棋譜ファイルは 別のところに保存しておいてください
2. 📂`pibot` に `*.json` ファイルをたくさん入れてください
3. ターミナルで `python.exe pibot_to_kif.py` コマンドを実行してください
4. KIF形式に変換して 📂`kif` へ出力されます
5. 読み終えた `pibot/*.json` ファイルは、 `pibot-done/*.json` へ移動されます
6. PIBOT ファイル形式は永続保存に適しません。使い終わったら削除しましょう

## PIBOT から KIFU へ変換

1. 注意。消えると困るオリジナルの棋譜ファイルは 別のところに保存しておいてください
2. 📂`pibot` に `*.json` ファイルをたくさん入れてください
3. ターミナルで `python.exe pibot_to_kifu.py` コマンドを実行してください
4. KIFU形式に変換して 📂`kifu` へ出力されます
5. 読み終えた `pibot/*.json` ファイルは、 `pibot-done/*.json` へ移動されます
6. PIBOT ファイル形式は永続保存に適しません。使い終わったら削除しましょう

## Documents

📖　[KIF形式を調べようぜ（＾～＾）？](https://crieit.net/drafts/6150ffc21e0de)  
📖　[将棋の符号](https://crieit.net/drafts/615192ae93d14)  

## 開発者用

### 動作テスト KIF -> PIBOT -> KIF

(KIF -> PIBOT)、(PIBOT -> KIF) 変換が壊れていないかテストします  

1. 注意。消えると困るオリジナルの棋譜ファイルは 別のところに保存しておいてください
2. 📂`kif` に `*.kif` ファイルをたくさん入れてください
3. ターミナルで `python.exe test_kif.py` コマンドを実行してください
4. KIF を PIBOT へ変換し、 PIBOT から KIF を復元するテストが行われます。  
   成功すれば、読み終えた `kif/*.kif` ファイルは、 📂`kif-done` へファイルが移動します
5. PIBOT ファイル形式は永続保存に適しません。使い終わったら削除しましょう

### 動作テスト KIFU -> PIBOT -> KIFU

(KIFU -> PIBOT)、(PIBOT -> KIFU) 変換が壊れていないかテストします  

1. 注意。消えると困るオリジナルの棋譜ファイルは 別のところに保存しておいてください
2. 📂`kifu` に `*.kifu` ファイルをたくさん入れてください
3. ターミナルで `python.exe test_kifu.py` コマンドを実行してください
4. KIFU を PIBOT へ変換し、 PIBOT から KIFU を復元するテストが行われます。  
   成功すれば、読み終えた `kifu/*.kifu` ファイルは、 📂`kifu-done` へファイルが移動します
5. PIBOT ファイル形式は永続保存に適しません。使い終わったら削除しましょう
