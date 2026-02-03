# AWS Learner Lab: S3 Trigger Lambda Hands-on

AWS Academy Learner Lab環境を利用して構築した、S3へのファイルアップロードをトリガーとするサーバーレス・データ処理システムの学習記録です。

## 📖 概要

S3バケットにテキストファイルがアップロードされたことを検知し、Lambda関数を自動起動させます。Lambdaはアップロードされたファイルの中身（テキスト）を読み取り、CloudWatch Logsに出力します。

## アーキテクチャ

```
User -> S3 Bucket (Upload) -> Lambda Function (Trigger & Read) -> CloudWatch Logs (Output)
```

## ⚠️ Learner Lab 環境の前提条件

このハンズオンは AWS Academy Learner Lab の制約下で実行しています。

- Region: us-east-1 (N. Virginia) 限定
- IAM Role: LabRole (既存のロール) を使用
- Budget: $100 (Free Tier優先構成)

## 🛠 構築手順

### 1. S3バケットの作成

- サービス: S3
- バケット名: learner-lab-lambda-trigger-[任意の名前]
- リージョン: us-east-1
- 設定: デフォルト設定のまま作成

### 2. Lambda関数の作成

- サービス: Lambda
- 関数名: S3EventHandler
- ランタイム: Python 3.12
- 実行ロール (重要):
  - Learner LabではIAMロールの作成権限がないため、「既存のロールを使用する」を選択。
  - LabRole を指定する。

### 3. トリガーの設定

- Lambda関数の設定画面で「トリガーを追加」を選択。
- ソースとして作成したS3バケットを指定。
- イベントタイプ: All object create events (作成イベントすべて)

### 4. 実装コード (Python)

boto3 ライブラリを使用して、イベント情報からバケット名とキーを取得し、オブジェクトの実データを読み込む処理です。

```python
import json
import urllib.parse
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # 1. イベントからバケット名とファイル名を取得
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # 2. S3からファイルの実データを取得
        response = s3.get_object(Bucket=bucket, Key=key)
        
        # 3. 中身を読み取ってデコード（テキストファイル前提）
        content = response['Body'].read().decode('utf-8')
        
        print(f"--- File Content Start ---")
        print(content)
        print(f"--- File Content End ---")
        
        return f"Successfully read {key} from {bucket}"

    except Exception as e:
        print(e)
        print(f"Error getting object {key} from bucket {bucket}.")
        raise e
```

## 🧪 動作確認結果

### テスト手順

- ローカルPCで test.txt を作成（内容: Hello AWS Learner Lab!）。
- S3バケットへアップロード。
- CloudWatch Logs でログストリームを確認。

### 実行ログ (CloudWatch Logs)

正常にファイルの中身が読み取れていることを確認。

```
2026-02-01T15:42:50.790Z
--- File Content Start ---

2026-02-01T15:42:50.790Z
Hello AWS Learner Lab!

2026-02-01T15:42:50.790Z
--- File Content End ---
```

## 📝 学んだこと

- **LabRoleの重要性:** Learner LabではIAM権限が制限されているため、標準の LabRole を使用する必要がある。
- **イベント駆動:** ポーリング（監視）ではなく、イベント発生時にのみコンピュートリソースが起動するため、コスト効率が良い。
- **コールドスタート:** 最初の実行時には Init Duration が発生し、実行環境の準備に時間がかかることがログから確認できた。
