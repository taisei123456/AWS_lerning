# CloudFormationハンズオン: EC2とセキュリティグループの安全な構築

このハンズオンでは、AWS Academy Learner Labの制約（予算 `$100`、`us-east-1` 限定）の範囲内で、安全にEC2インスタンスとセキュリティグループを構築・削除する手順を学びます。

## 1. テンプレートファイル（YAML）の作成

以下のコードをコピーし、`learner-lab-ec2.yaml` というファイル名で保存してください。

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'AWS Academy Learner Lab: Basic EC2 and Security Group'

Resources:
  # 1. セキュリティグループの作成 (SSHアクセスのみ許可)
  LabSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow SSH access for Learner Lab
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0 # 学習用のため全開放。実務では自分のIPに制限します

  # 2. EC2インスタンスの作成
  LabEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      # 鉄則: 予算枯渇を防ぐため、低コストな無料枠レベルを指定
      InstanceType: t2.micro
      # 鉄則: us-east-1 (N. Virginia) の最新Amazon Linux 2023を指定
      ImageId: '{{resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64}}'
      SecurityGroupIds:
        - !GetAtt LabSecurityGroup.GroupId
      Tags:
        - Key: Name
          Value: LearnerLab-CFn-Handson

Outputs:
  InstanceId:
    Description: The Instance ID of the EC2 instance
    Value: !Ref LabEC2Instance
```

> [!WARNING]
> **注意（IAM権限について）**
> Learner Labでは新規のIAMロール作成が制限されています。EC2に権限（S3アクセスなど）を付与する場合は、新規作成ではなく、既存の `LabRole` のARNをテンプレート内で指定してください。

## 2. テンプレートのデプロイ（AWSマネジメントコンソール編）

1. コンソール右上のリージョンが **米国東部（バージニア北部）`us-east-1`** であることを確認します。  
   （東京リージョンは利用不可です）
2. 検索バーで「CloudFormation」と検索し、サービス画面を開きます。
3. **[スタックの作成] > [新しいリソースを使用（標準）]** をクリックします。
4. 「テンプレートの準備」で **[既存のテンプレートを選択]** を選びます。
5. 「テンプレートの指定」で **[テンプレートファイルのアップロード]** を選び、先ほど保存した `learner-lab-ec2.yaml` をアップロードして「次へ」をクリックします。
6. 「スタックの名前」に任意の名前（例: `MyFirstLabStack`）を入力し、「次へ」をクリックします。
7. 「スタックオプションの設定」は変更せず、一番下までスクロールして「次へ」をクリックします。
8. レビュー画面を確認し、右下の **[送信（Submit）]** をクリックします。
9. ステータスが `CREATE_IN_PROGRESS` から `CREATE_COMPLETE` に変われば構築完了です。EC2画面でインスタンスが起動していることを確認しましょう。

## 3. 【超重要】リソースの削除（クリーンアップ）

Learner Labは「4時間」などのセッション時間が切れると自動ログアウトされますが、作成したEC2インスタンスは裏で動き続け、限られた `$100` の予算を消費し続けます。  
学習終了後は、必ず以下の手順で削除してください。

1. CloudFormationのコンソール画面を開きます。
2. 作成したスタック（例: `MyFirstLabStack`）を選択します。
3. 右上の **[削除（Delete）]** をクリックします。
4. ステータスが `DELETE_COMPLETE` になり、スタックが消えたことを確認します。  
   （EC2とセキュリティグループも自動的に削除されます）