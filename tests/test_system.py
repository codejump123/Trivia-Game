import json
import socket
import tempfile
import time
import unittest

from common.protocol import decode_message, encode_message
from server.server import start_server


class SystemTests(unittest.TestCase):
    def _write_questions(self, path):
        data = [
            {
                "id": "q1",
                "category": "Science",
                "question": "What is 2+2?",
                "options": ["3", "4"],
                "answer_index": 1,
            }
        ]
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle)

    def _send(self, writer, reader, payload):
        writer.write(encode_message(payload))
        writer.flush()
        return decode_message(reader.readline())

    def test_end_to_end_flow(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            users_path = f"{temp_dir}/users.json"
            questions_path = f"{temp_dir}/questions.json"
            with open(users_path, "w", encoding="utf-8") as handle:
                json.dump({}, handle)
            self._write_questions(questions_path)

            server, _ = start_server("127.0.0.1", 0, temp_dir)
            host, port = server.server_address

            time.sleep(0.1)
            sock = socket.create_connection((host, port))
            reader = sock.makefile("r")
            writer = sock.makefile("w")
            try:
                response = self._send(
                    writer,
                    reader,
                    {"type": "register", "username": "alex", "password": "pass"},
                )
                self.assertEqual(response["status"], "ok")

                response = self._send(
                    writer,
                    reader,
                    {"type": "login", "username": "alex", "password": "pass"},
                )
                self.assertEqual(response["status"], "ok")

                response = self._send(writer, reader, {"type": "get_categories"})
                self.assertEqual(response["status"], "ok")
                self.assertIn("Science", response["categories"])

                response = self._send(
                    writer,
                    reader,
                    {"type": "request_question", "category": "Science", "wager": 10},
                )
                self.assertEqual(response["status"], "ok")
                question_id = response["question_id"]

                response = self._send(
                    writer,
                    reader,
                    {
                        "type": "submit_answer",
                        "question_id": question_id,
                        "answer_index": 1,
                    },
                )
                self.assertEqual(response["status"], "ok")
                self.assertTrue(response["correct"])
            finally:
                reader.close()
                writer.close()
                sock.close()
                server.shutdown()
                server.server_close()


if __name__ == "__main__":
    unittest.main()
