import argparse
import socketserver
import threading

from common.protocol import (
    decode_message,
    encode_message,
    error_response,
    success_response,
    validate_request,
)

from .data_store import DataStore
from .game_logic import apply_answer, update_stats, validate_wager
from .question_bank import QuestionBank


class TriviaRequestHandler(socketserver.StreamRequestHandler):
    def setup(self):
        super().setup()
        self.session = {"user": None, "pending": None}

    def handle(self):
        while True:
            raw = self.rfile.readline()
            if not raw:
                break
            try:
                message = decode_message(raw.decode("utf-8"))
            except Exception as exc:
                self._send(error_response(str(exc), "bad_request"))
                continue

            is_valid, error_msg = validate_request(message)
            if not is_valid:
                self._send(error_response(error_msg, "bad_request"))
                continue

            response = self._dispatch(message)
            self._send(response)

    def _dispatch(self, message):
        msg_type = message["type"]
        if msg_type == "register":
            return self._register(message)
        if msg_type == "login":
            return self._login(message)
        if msg_type == "logout":
            return self._logout()
        if msg_type == "get_categories":
            return self._get_categories()
        if msg_type == "request_question":
            return self._request_question(message)
        if msg_type == "submit_answer":
            return self._submit_answer(message)
        if msg_type == "get_stats":
            return self._get_stats()
        if msg_type == "ping":
            return success_response({"message": "pong"})
        return error_response("Unknown request type", "bad_request")

    def _register(self, message):
        username = message["username"]
        password = message["password"]
        ok, error_msg = self.server.data_store.register_user(username, password)
        if not ok:
            return error_response(error_msg, "registration_failed")
        return success_response({"message": "registered"})

    def _login(self, message):
        username = message["username"]
        password = message["password"]
        if not self.server.data_store.authenticate(username, password):
            return error_response("Invalid credentials", "auth_failed")
        self.session["user"] = username
        return success_response({"message": "logged_in"})

    def _logout(self):
        self.session["user"] = None
        self.session["pending"] = None
        return success_response({"message": "logged_out"})

    def _get_categories(self):
        categories = self.server.question_bank.get_categories()
        return success_response({"categories": categories})

    def _request_question(self, message):
        if not self.session["user"]:
            return error_response("Not authenticated", "auth_required")
        category = message["category"]
        wager = message["wager"]
        stats = self.server.data_store.get_user_stats(self.session["user"])
        if not stats:
            return error_response("User not found", "auth_failed")

        ok, error_msg = validate_wager(stats["points"], wager)
        if not ok:
            return error_response(error_msg, "invalid_wager")

        recent_ids = self.server.data_store.get_recent_questions(
            self.session["user"],
            category,
        )
        question = self.server.question_bank.select_question(category, recent_ids)
        if not question:
            return error_response("No questions for category", "not_found")

        self.session["pending"] = {
            "question_id": question["id"],
            "wager": wager,
            "category": category,
        }
        self.server.data_store.record_question_seen(
            self.session["user"],
            category,
            question["id"],
        )

        return success_response(
            {
                "question_id": question["id"],
                "category": category,
                "question": question["question"],
                "options": question["options"],
                "points": stats["points"],
            }
        )

    def _submit_answer(self, message):
        if not self.session["user"]:
            return error_response("Not authenticated", "auth_required")
        pending = self.session["pending"]
        if not pending:
            return error_response("No pending question", "invalid_state")
        if message["question_id"] != pending["question_id"]:
            return error_response("Question mismatch", "invalid_state")

        question = self.server.question_bank.get_question(pending["question_id"])
        if not question:
            return error_response("Question not found", "not_found")

        answer_index = message["answer_index"]
        is_correct = answer_index == question["answer_index"]
        stats = self.server.data_store.get_user_stats(self.session["user"])
        new_points, delta = apply_answer(stats["points"], pending["wager"], is_correct)
        stats["points"] = new_points
        update_stats(stats, is_correct)
        self.server.data_store.update_user_stats(self.session["user"], stats)

        self.session["pending"] = None
        return success_response(
            {
                "correct": is_correct,
                "delta": delta,
                "points": new_points,
                "correct_answer": question["answer_index"],
            }
        )

    def _get_stats(self):
        if not self.session["user"]:
            return error_response("Not authenticated", "auth_required")
        stats = self.server.data_store.get_user_stats(self.session["user"])
        if not stats:
            return error_response("User not found", "auth_failed")
        return success_response({"stats": stats})

    def _send(self, message):
        payload = encode_message(message)
        self.wfile.write(payload.encode("utf-8"))


class ThreadedTriviaServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, handler_cls, data_store, question_bank):
        super().__init__(server_address, handler_cls)
        self.data_store = data_store
        self.question_bank = question_bank


def start_server(host, port, data_dir):
    users_path = f"{data_dir}/users.json"
    questions_path = f"{data_dir}/questions.json"
    data_store = DataStore(users_path)
    question_bank = QuestionBank(questions_path)
    server = ThreadedTriviaServer((host, port), TriviaRequestHandler, data_store, question_bank)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def main():
    parser = argparse.ArgumentParser(description="Trivia server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--data-dir", default="data")
    args = parser.parse_args()

    server, _ = start_server(args.host, args.port, args.data_dir)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
