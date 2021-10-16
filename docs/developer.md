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

## 一時ファイルを全部消す

テンポラリー フォルダーの中のものは、よく上書き、削除されるので、壊されたくないものは置かないでください  

1. 注意。消えると困るオリジナルの棋譜ファイルは 別のところに保存しておいてください
2. ターミナルで `python.exe debug.py --rmtmp` コマンドを実行してください

## 出力ファイルを全部消す

📂`output` フォルダーに、消されてこまるファイルを置かないでください  

1. ターミナルで `python.exe debug.py --rmout` コマンドを実行してください
2. 📂`output` フォルダーの中の 📄`*.kif` ファイルは削除されます
3. 📂`output` フォルダーの中の 📄`*.kifu` ファイルは削除されます
4. 📂`output` フォルダーの中の 📄`*.json` ファイルは削除されます
5. 📂`output` フォルダーの中の 📄`*.toml` ファイルは削除されます

## 動作テスト .kif変換

(Copy: input->kif) (Convert: kif->kifu->pivot)、(Convert: pivot->kifu->kif) 変換が壊れていないかテストします  

1. 📂`input` フォルダーに 📄`*.kif` ファイルをたくさん入れてください
2. ターミナルで `python.exe test_kif.py` コマンドを実行してください
3. 変換が壊れていれば、標準出力にメッセージが出ます。問題がなければメッセージは出力されません
4. ゴミファイルが溜まっているので消すために、`python.exe debug.py --rmtmp` コマンドを実行してください

## 動作テスト .kifu変換

(Copy: input->kifu) (Convert kifu->pivot)、(Convert: pivot->kifu) 変換が壊れていないかテストします  

1. 📂`input` に `*.kifu` ファイルをたくさん入れてください
2. ターミナルで `python.exe test_kifu.py` コマンドを実行してください
3. 変換が壊れていれば、標準出力にメッセージが出ます。問題がなければメッセージは出力されません
4. ゴミファイルが溜まっているので消すために、`python.exe debug.py --rmtmp` コマンドを実行してください

## デバッグモード

コマンドライン引数に `-h` を付けて、ヘルプがあるものは何か用意がある。引数に `--debug` を付けるとデバッグモード。  

## 危険な操作 - 入力ファイルを全部消す

**DANGER** 📂`input` フォルダーの中身を消すコマンドです  

1. ターミナルで `python.exe debug.py --rmin` コマンドを実行してください
2. 📂`input` フォルダーの中の 📄`*.kif` ファイルは削除されます
3. 📂`input` フォルダーの中の 📄`*.kifu` ファイルは削除されます
4. 📂`input` フォルダーの中の 📄`*.json` ファイルは削除されます
5. 📂`input` フォルダーの中の 📄`*.toml` ファイルは削除されます

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
