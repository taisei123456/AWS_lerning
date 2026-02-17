# Amazon Q Developer (CLI) インストール手順 (EC2 / Amazon Linux 2023版)

## 1. 前提条件
* **環境:** AWS Academy Learner Lab
* **リージョン:** us-east-1 (N. Virginia)
* **OS:** Amazon Linux 2023
* **インスタンスタイプ:** t2.micro または t3.micro

## 2. インストール手順

EC2にSSH接続（Instance Connectなど）し、以下のコマンドを順に実行してください。

### ステップ 1: 準備とダウンロード
まずはホームディレクトリに移動し、必要なツール（unzip）を入れ、インストーラーをダウンロードします。

```bash
# ホームディレクトリへ移動（迷子防止）
cd ~

# 解凍ツール(unzip)のインストール
# ※Amazon Linux 2023には標準で入っていないため必須
sudo dnf install unzip -y

# インストーラーのダウンロード
curl --proto '=https' --tlsv1.2 -sSf "[https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux.zip](https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux.zip)" -o "q.zip"

# ファイルの解凍
unzip q.zip

# インストールスクリプトの実行
./install.sh

source ~/.bashrc

# バージョン確認
q --version

# ログイン開始
q login