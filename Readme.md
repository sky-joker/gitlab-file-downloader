# gitlab-file-downloader

GitLabのリポジトリにあるファイルをダウンロードするツール

## 必要要件

* requests
* python >= 3.6

## 使い方

### Token発行

以下の手順でGitLabユーザーのTokenを生成します。

[![](./img/create_gitlab_token.gif)](./img/create_gitlab_token.gif)

### 設定ファイルの作成

Tokenを設定するファイルを作成します。  
コマンドで直接Tokenを引数で渡す場合は設定ファイルの作成は不要です。

```
$ vi ~/.gitlab
[settings]
token = gpSQeGAKah1JvdXQjCEi
```

### ファイルのダウンロード

以下の例では `example.txt` をダウンロードしています。
ダウンロードするファイルパスはリポジトリ内のカレントパスで指定してください。

```
$ ./gitlab-file-downloader.py -s 192.168.0.115 -p example -f lib/app/example.txt
$ ls
example.txt         gitlab-file-downloader.py   venv
```

ブランチも指定可能です。  
以下は `devel` ブランチにある `example.txt` をダウンロードしています。

```
$ ./gitlab-file-downloader.py -s 192.168.0.115 -p example -f lib/app/example.txt -b devel
```
