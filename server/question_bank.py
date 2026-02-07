import json
import random


class QuestionBank:
    def __init__(self, questions_path, rng=None):
        self.questions_path = questions_path
        self.rng = rng or random.Random()
        self._questions = self._load_questions()
        self._by_id = {question["id"]: question for question in self._questions}

    def _load_questions(self):
        with open(self.questions_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("Questions file must contain a list")
        return data

    def get_categories(self):
        return sorted({question["category"] for question in self._questions})

    def get_question(self, question_id):
        return self._by_id.get(question_id)

    def select_question(self, category, recent_ids):
        candidates = [q for q in self._questions if q["category"] == category]
        if not candidates:
            return None
        filtered = [q for q in candidates if q["id"] not in recent_ids]
        pool = filtered if filtered else candidates
        return self.rng.choice(pool)
