import json
import tempfile
import unittest

from server.question_bank import QuestionBank


class QuestionBankTests(unittest.TestCase):
    def _write_questions(self, path):
        data = [
            {
                "id": "q1",
                "category": "Science",
                "question": "Q1",
                "options": ["a", "b"],
                "answer_index": 0,
            },
            {
                "id": "q2",
                "category": "Science",
                "question": "Q2",
                "options": ["a", "b"],
                "answer_index": 1,
            },
        ]
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle)

    def test_select_question_avoids_recent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            questions_path = f"{temp_dir}/questions.json"
            self._write_questions(questions_path)
            bank = QuestionBank(questions_path)
            question = bank.select_question("Science", recent_ids=["q1"])
            self.assertIsNotNone(question)
            self.assertEqual(question["id"], "q2")

    def test_select_question_fallback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            questions_path = f"{temp_dir}/questions.json"
            self._write_questions(questions_path)
            bank = QuestionBank(questions_path)
            question = bank.select_question("Science", recent_ids=["q1", "q2"])
            self.assertIsNotNone(question)
            self.assertIn(question["id"], {"q1", "q2"})


if __name__ == "__main__":
    unittest.main()
