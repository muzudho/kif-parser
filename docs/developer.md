# kif-parser 開発者向けドキュメント


## 動作テスト .kif変換

(Copy: input->kif) (Convert: kif->kifu->pivot)、(Convert: pivot->kifu->kif) 変換が壊れていないかテストします  

1. 📂`input` フォルダーに 📄`*.kif` ファイルをたくさん入れてください
2. ターミナルで `python.exe test_kif.py` コマンドを実行してください
3. 変換が壊れていれば、標準出力にメッセージが出ます。問題がなければメッセージは出力されません
4. ゴミファイルが溜まっているので消すために、`python.exe remove_all_temporary.py` コマンドを実行してください

## 動作テスト .kifu変換

(Copy: input->kifu) (Convert kifu->pivot)、(Convert: pivot->kifu) 変換が壊れていないかテストします  

1. 📂`input` に `*.kifu` ファイルをたくさん入れてください
2. ターミナルで `python.exe test_kifu.py` コマンドを実行してください
3. 変換が壊れていれば、標準出力にメッセージが出ます。問題がなければメッセージは出力されません
4. ゴミファイルが溜まっているので消すために、`python.exe remove_all_temporary.py` コマンドを実行してください

## デバッグモード

コマンドライン引数に `-h` を付けて、ヘルプがあるものは何か用意がある。引数に `--debug` を付けるとデバッグモード。  

## 危険な操作 - 入力ファイルを全部消す

**DANGER** 📂`input` フォルダーの中身を消すコマンドです  

1. ターミナルで `python.exe remove_all_input_danger.py` コマンドを実行してください
2. 📂`input` フォルダーの中の 📄`*.kif` ファイルは削除されます
3. 📂`input` フォルダーの中の 📄`*.kifu` ファイルは削除されます
4. 📂`input` フォルダーの中の 📄`*.json` ファイルは削除されます
5. 📂`input` フォルダーの中の 📄`*.toml` ファイルは削除されます

## 危険な操作 - 出力フォルダーの内容を、入力フォルダーへ移動

**DANGER** 📂`input` フォルダーの中身を上書きするコマンドです  

1. ターミナルで `python.exe move_output_to_input_danger.py` コマンドを実行してください
2. 📂`output` フォルダーの中の (📄`*.kif`, 📄`*.kifu`, 📄`*.json`, 📄`*.toml`)ファイルを 📂`input` へ移動します

## 危険な操作 - テストデータ フォルダーの内容を、入力フォルダーへコピー

**DANGER** 📂`input` フォルダーの中身を上書きするコマンドです  

1. ターミナルで `python.exe copy_test_data_to_input_danger.py` コマンドを実行してください
2. 📂`test_data` フォルダーの中の (📄`*.kif`, 📄`*.kifu`, 📄`*.json`, 📄`*.toml`)ファイルを 📂`input` へコピーします

## PIVOT 仕様

### row_type - 行の型

|行の型|説明|
|---|---|
|comment|コメント行|
|explanation|指し手へのコメント行|
|bookmark|しおり|
|player|対局者の手番、対局者名行|
|variationLabel|変化手順のジャンプ先ラベル|
|result|どちらの勝ち、といった終局時のメッセージ行。盤面作成時などには無いこともある|
|appendix|無視して構わない。元の `.kif` ファイルには無かったが、付加した情報。0行目として付加する|
