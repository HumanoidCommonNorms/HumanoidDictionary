# Humanoid Dictionary

人型ロボット開発に必要な用語の辞書です。

用語は、[**リンク**](https://humanoidcommonnorms.github.io/HumanoidDictionary/) を参照してください。


## ルール

* 英名／日本語名 または略語で同じ意味の用語がある場合、下記の順番で記載します。

1. 英名
1. 日本語名
1. 略語

また、記事事態はマークダウンの@import機能を利用して、他のファイルを読み込みます。

## 追加方法

### ツールで追加する場合

scriptフォルダの"dic_converter.py"を使用して、自動で追加することができます。

1. 追加用の用語が入ったファイルを作成する
   1. 参考ファイル：script/data.tsv
   2. ヘッダーはdic_converterのバージョンによって変わる可能性があるので、最新のバージョンを確認してください。
1. 下記のコマンドを実行する

    ```python
    # 実行コマンド例
    cd script
    dic_converter.py data.tsv -t ../
    ```

1. VS codeで、Markdown Preview Enhancedを使用して、index.mdをプレビューする
1. プレビュー画面より、Export->HTML->HTML(offline)を選択して、index.htmlを生成する

### 手作業で追加する場合

1. template.mdを追加したい語句の名前に書き換える
1. 頭文字のフォルダに格納する
1. 記事の内容を記載する
1. _toc.mdに追加した語句のリンクを追加する
1. index.mdをhtmlに変換する
