# AWS Academy Learner Lab 実践レポート：Webサーバー構築とAmazon Qの導入

## 1. 概要
就職活動用ポートフォリオの公開を目指し、AWS Academy Learner Lab環境下でEC2インスタンスを利用した静的Webサイトのホスティング環境を構築した。
また、開発効率化のためにAWSの生成AIアシスタントツール「Amazon Q Developer (CLI版)」をサーバー内に導入し、コマンドライン操作の支援環境を整えた。

## 2. アーキテクチャ
* **リージョン:** us-east-1 (N. Virginia)
* **インフラ:** Amazon EC2 (t2.micro / Amazon Linux 2023)
* **Webサーバー:** Apache HTTP Server (httpd)
* **開発ツール:** Amazon Q Developer CLI
* **構成図:**
    ```mermaid
    graph TD
        User["User (Browser)"] -->|HTTP:80| IGW[Internet Gateway]
        IGW --> VPC[VPC]
        
        subgraph VPC
            subgraph PublicSubnet["Public Subnet"]
                EC2[EC2 Instance]
                Apache[Apache Web Server]
                Q[Amazon Q CLI]
            end
        end
        
        EC2 --> Apache
        EC2 --> Q
        Apache --> HTML["/var/www/html/index.html"]
    ```

## 3. Learner Lab 環境の前提条件
本構築は、AWS Academy Learner Labの制約に基づき以下のルールを厳守して実施した。

1.  **リージョン制約:** 必ず `us-east-1` を使用する（他リージョンは使用不可）。
2.  **予算制約:** 全体予算 $100 以内で運用するため、無料利用枠対象の `t2.micro` を選定。
3.  **IAM権限:** インスタンスプロファイルには、ラボ指定の `LabRole` を使用。
4.  **リソース管理:** セッション終了後も課金（EBS料金）が継続するため、不要時はインスタンスを停止・削除する運用ルールを適用。

## 4. 構築手順

### 4-1. EC2インスタンスの起動
1.  AWSコンソール (us-east-1) からEC2を起動。
2.  **AMI:** Amazon Linux 2023
3.  **インスタンスタイプ:** t2.micro
4.  **キーペア:** vockey
5.  **ネットワーク:** HTTP (ポート80) と SSH (ポート22) を許可。
6.  **IAMロール:** `LabRole` をアタッチ（必須）。

### 4-2. Webサーバー (Apache) のセットアップ
EC2にSSH接続し、以下のコマンドでApacheをインストール・起動。

```bash
# システム更新とApacheインストール
sudo dnf update -y
sudo dnf install httpd -y

# 起動と自動起動設定
sudo systemctl start httpd
sudo systemctl enable httpd

# コンテンツ配置ディレクトリの権限設定 (ec2-userで編集可能にする)
sudo usermod -a -G apache ec2-user
sudo chown -R ec2-user:apache /var/www
sudo chmod 2775 /var/www

