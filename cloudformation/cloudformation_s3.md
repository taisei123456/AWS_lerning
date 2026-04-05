# CloudFormationハンズオン: S3バケットの作成とファイルアップロード

このハンズオンでは、以下の役割分担を学びます。

- CloudFormation: インフラ（器）を作る
- CLIやコンソール: ファイル配置などの中身を操作する

## 1. CloudFormationでS3バケットを作成する

以下のコードをコピーし、`learner-lab-s3.yaml` というファイル名で保存してください。

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'AWS Academy Learner Lab: Basic S3 Bucket'

Resources:
  LabS3Bucket:
    Type: AWS::S3::Bucket
    # 注意: S3のバケット名は世界中で一意（重複不可）です。
    # ここでは名前を明示的に指定せず、AWSにランダムでユニークな名前を自動生成させます。

Outputs:
  BucketName:
    Description: "自動生成されたS3バケットの名前"
    Value: !Ref LabS3Bucket
```

### デプロイ手順

1. コンソール右上が `us-east-1 (N. Virginia)` であることを確認します。
2. CloudFormation画面で `learner-lab-s3.yaml` をアップロードし、スタックを作成します（スタック名例: `MyLabS3Stack`）。
3. ステータスが `CREATE_COMPLETE` になったら、「出力（Outputs）」タブを確認します。
4. 自動生成された `BucketName`（例: `mylabs3stack-labs3bucket-1a2b3c4d5e`）の値をコピーして控えます。

## 2. 動画ファイルをアップロードする

作成されたバケットに、テスト用の小さな動画ファイル（数MB程度のMP4など）をアップロードします。  
予算節約のため、巨大なファイルは避けてください。

### A. マネジメントコンソールから行う場合

1. 検索バーから「S3」を開き、先ほど作成されたバケット名をクリックします。
2. 「アップロード」を押し、PC内の動画ファイルを追加してアップロードを実行します。

### B. AWS CLIから行う場合

> [!WARNING]
> Learner Labの制約により、`aws configure` は使えません。必ず「AWS Details」から取得した一時クレデンシャルを `~/.aws/credentials` に設定してから実行してください。

```bash
# --region us-east-1 を必ず付与します
aws s3 cp ./your-video.mp4 s3://<先ほどコピーしたバケット名>/ --region us-east-1
```

## 3. 【超重要】リソースの削除（S3特有の罠）

S3とCloudFormationを組み合わせる場合、**ファイルが残っているS3バケットはCloudFormationから削除できません**。  
そのままスタック削除を行うと `DELETE_FAILED` になります。

必ず次の2ステップで削除してください。

1. 中身を空にする: S3コンソールで対象バケットを選択し、「空にする（Empty）」を実行して動画ファイルを完全に削除します。
2. スタックを削除する: バケットが空であることを確認してから、CloudFormation画面でスタック（例: `MyLabS3Stack`）を削除します。