# kif-parser 開発者向けドキュメント

![20211016blog6.png](./docs/img/20211016blog6.png)  
👆 PIVOTファイルの例  

## KIF から KIFU へ変換（またその逆）

1. 📂`input` フォルダーに 📄`*.kif` ファイルをたくさん入れてください
2. ターミナルで `python.exe debug.py --tool kif2kifu` コマンドを実行してください
3. 📄`input/*.kif` は UTF-8形式に変換して 📂`output` へ 📄`*.kifu` が出力されます

同様に、逆の操作として `python.exe debug --tool kifu2kif` というコマンドがあります  


## KIF から PIVOT へ変換

1. 📂`input` フォルダーに `*.kif` ファイルをたくさん入れてください
2. ターミナルで `python.exe debug.py --tool kif2pivot` コマンドを実行してください
3. JSON形式に変換して 📂`output` へ 📄`*[kifu-pivot].json` （PIVOT）が出力されます

同様に、逆の操作として `python.exe debug.py --tool kifu2pivot` というコマンドがあります

## PIVOT から KIF へ変換

1. 📂`input` フォルダーに `*[kifu-pivot].json` 形式のPIVOTファイルをたくさん入れてください
2. ターミナルで `python.exe debug.py --tool pivot2kif` コマンドを実行してください
3. KIF形式に変換して 📂`output` へ 📄`*.kif` が出力されます

同様に、逆の操作として `python.exe debug.py --tool pivot2kifu` というコマンドがあります

# 以前の記事

`*_danger.py` は 📂`input` フォルダーの内容を破壊します。誤ってダブルクリックすることのないようにしましょう。  

リリース時に必要なフォルダー階層は以下の通りです  

```plain
/kif-parser
    /input
        # ここに *.kif, *.kifu, *.toml, `*[kifu-pivot].json` のいずれかを置きます
    /output
        # ここに変換後のファイルが出力されます。スクリプト実行時にここに置いてある棋譜ファイルは削除されます
    /scripts
        # このなかに ファイルを変換するプログラムが大量に入っています
    /temporary # このフォルダーの下で棋譜ファイルのコピー、編集、削除が行われます
        /from-pivot
            /kif
            /kifu
            /pivot
            /toml
            /object # 中間ファイル
            /reverse-kif # 可逆変換テスト
            /reverse-kifu
            /reverse-pivot
            /reverse-toml
        /no-pivot
            # (from-pivotと同様)
        /output-pivot
            # 入力フォルダ―としても利用されます
        /to-pivot
            # (from-pivotと同様)

    debug.py
    LICENSE
```

## (WIP) PIVOT から TOML へ変換

```shell
# もし、 .kif を .toml に変換したいなら
pip install tomli
```

## デバッグモード

コマンドライン引数に `-h` を付けて、ヘルプがあるものは何か用意がある。引数に `--debug` を付けるとデバッグモード。  


## PIVOT 仕様

### row_type - 行の型

|行の型|説明|
|---|---|
|comment|コメント行|
|explain|指し手へのコメント行|
|bookmark|しおり|
|startTime|開始日時の行|
|endTime|終了日時の行|
|handicap|手合い割の行|
|player|対局者の手番、対局者名行|
|variationLabel|変化手順のジャンプ先ラベル|
|result|どちらの勝ち、といった終局時のメッセージ行。盤面作成時などには無いこともある|
|metadata|無視して構わない。元の `.kif` ファイルには無かったが、付加した情報。0行目として付加する|
