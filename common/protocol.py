import json


MAX_MESSAGE_BYTES = 32_000


class ProtocolError(ValueError):
    pass


def encode_message(message):
    payload = json.dumps(message, separators=(",", ":"))
    return f"{payload}\n"


def decode_message(raw_line):
    if raw_line is None:
        raise ProtocolError("Empty input")
    if len(raw_line) > MAX_MESSAGE_BYTES:
        raise ProtocolError("Message too large")
    raw_line = raw_line.strip()
    if not raw_line:
        raise ProtocolError("Empty input")
    try:
        return json.loads(raw_line)
    except json.JSONDecodeError as exc:
        raise ProtocolError("Invalid JSON") from exc


def validate_request(message):
    if not isinstance(message, dict):
        return False, "Message must be an object"
    msg_type = message.get("type")
    if not msg_type or not isinstance(msg_type, str):
        return False, "Missing or invalid type"

    required_fields = {
        "register": ["username", "password"],
        "login": ["username", "password"],
        "logout": [],
        "get_categories": [],
        "request_question": ["category", "wager"],
        "submit_answer": ["question_id", "answer_index"],
        "get_stats": [],
        "ping": [],
    }

    if msg_type not in required_fields:
        return False, "Unknown request type"

    for field in required_fields[msg_type]:
        if field not in message:
            return False, f"Missing field: {field}"

    return True, ""


def success_response(data=None):
    payload = {"status": "ok"}
    if data:
        payload.update(data)
    return payload


def error_response(message, code="error"):
    return {"status": "error", "code": code, "message": message}
