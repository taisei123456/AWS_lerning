import json
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TABLE_NAME", "TodoTasks")
table = dynamodb.Table(TABLE_NAME)


def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, ensure_ascii=False),
    }


def _to_json_compatible(value):
    if isinstance(value, list):
        return [_to_json_compatible(v) for v in value]
    if isinstance(value, dict):
        return {k: _to_json_compatible(v) for k, v in value.items()}
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    return value


def _parse_body(event: dict) -> dict:
    body = event.get("body")
    if body is None:
        return {}
    if event.get("isBase64Encoded"):
        return {}
    if isinstance(body, str):
        body = body.strip()
        return json.loads(body) if body else {}
    if isinstance(body, dict):
        return body
    return {}


def create_task(event: dict) -> dict:
    try:
        payload = _parse_body(event)
    except json.JSONDecodeError:
        return _response(400, {"message": "Invalid JSON body."})

    title = str(payload.get("title", "")).strip()
    if not title:
        return _response(400, {"message": "title is required."})

    task_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    item = {
        "id": task_id,
        "title": title,
        "done": False,
        "createdAt": now,
    }

    table.put_item(Item=item)
    return _response(201, {"task": item})


def list_tasks() -> dict:
    result = table.scan()
    items = _to_json_compatible(result.get("Items", []))
    items.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
    return _response(200, {"tasks": items})


def get_task(task_id: str) -> dict:
    try:
        result = table.get_item(Key={"id": task_id})
    except ClientError as exc:
        return _response(500, {"message": "Failed to fetch task.", "error": str(exc)})

    item = result.get("Item")
    if not item:
        return _response(404, {"message": "Task not found."})

    return _response(200, {"task": _to_json_compatible(item)})


def delete_task(task_id: str) -> dict:
    try:
        response = table.delete_item(
            Key={"id": task_id},
            ConditionExpression="attribute_exists(id)",
            ReturnValues="ALL_OLD",
        )
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code")
        if error_code == "ConditionalCheckFailedException":
            return _response(404, {"message": "Task not found."})
        return _response(500, {"message": "Failed to delete task.", "error": str(exc)})

    deleted = response.get("Attributes", {})
    return _response(200, {"deleted": _to_json_compatible(deleted)})


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method")
    if not method:
        method = event.get("httpMethod")

    raw_path = event.get("rawPath") or event.get("path", "")
    path_parameters = event.get("pathParameters") or {}

    if raw_path.endswith("/tasks") and method == "POST":
        return create_task(event)

    if raw_path.endswith("/tasks") and method == "GET":
        return list_tasks()

    task_id = path_parameters.get("id")
    if task_id and method == "GET":
        return get_task(task_id)

    if task_id and method == "DELETE":
        return delete_task(task_id)

    return _response(404, {"message": "Route not found."})
