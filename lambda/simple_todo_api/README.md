# Simple Todo API (Lambda)

AWS Lambda で簡単に構築できる、最小構成の ToDo API です。

- API Gateway (HTTP API)
- Lambda (Python 3.12)
- DynamoDB

## できること

- `POST /tasks`: タスク作成
- `GET /tasks`: タスク一覧
- `GET /tasks/{id}`: タスク詳細
- `DELETE /tasks/{id}`: タスク削除

## デプロイ手順 (AWS SAM)

事前に AWS CLI と AWS SAM CLI のセットアップを済ませてください。

```bash
pip install -r requirements.txt
```

```bash
cd lambda/simple_todo_api
sam build
sam deploy --guided
```

`sam deploy --guided` の初回実行時は、スタック名とリージョンを入力してください。

## 動作確認

デプロイ完了時に出力される `ApiBaseUrl` を使ってテストします。

```bash
# 1) タスク作成
curl -X POST "${ApiBaseUrl}/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title":"Lambdaを学習する"}'

# 2) 一覧取得
curl "${ApiBaseUrl}/tasks"

# 3) 詳細取得（<task_id>は作成時のid）
curl "${ApiBaseUrl}/tasks/<task_id>"

# 4) 削除
curl -X DELETE "${ApiBaseUrl}/tasks/<task_id>"
```

## 補足

- 学習用のシンプル実装です。
- 本番用途では、入力バリデーションの強化、認証 (Cognito/JWT)、監査ログ、CORS設計などを追加してください。
