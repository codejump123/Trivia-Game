import json
import threading

from .auth import hash_password, verify_password


DEFAULT_POINTS = 100
RECENT_QUESTIONS_LIMIT = 5


class DataStore:
    def __init__(self, users_path):
        self.users_path = users_path
        self._lock = threading.RLock()
        self._users = self._load_json(self.users_path, default={})

    def _load_json(self, path, default):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError:
            return default

    def _save_users(self):
        with open(self.users_path, "w", encoding="utf-8") as handle:
            json.dump(self._users, handle, indent=2, sort_keys=True)

    def register_user(self, username, password):
        with self._lock:
            if username in self._users:
                return False, "Username already exists"
            salt, pw_hash = hash_password(password)
            self._users[username] = {
                "salt": salt,
                "password_hash": pw_hash,
                "stats": {
                    "points": DEFAULT_POINTS,
                    "games_played": 0,
                    "correct_answers": 0,
                    "incorrect_answers": 0,
                },
                "recent_questions": {},
            }
            self._save_users()
            return True, ""

    def authenticate(self, username, password):
        with self._lock:
            user = self._users.get(username)
            if not user:
                return False
            return verify_password(password, user["salt"], user["password_hash"])

    def get_user_stats(self, username):
        with self._lock:
            user = self._users.get(username)
            if not user:
                return None
            return json.loads(json.dumps(user["stats"]))

    def update_user_stats(self, username, stats):
        with self._lock:
            if username not in self._users:
                return False
            self._users[username]["stats"] = stats
            self._save_users()
            return True

    def record_question_seen(self, username, category, question_id):
        with self._lock:
            user = self._users.get(username)
            if not user:
                return
            recent = user["recent_questions"].setdefault(category, [])
            if question_id in recent:
                recent.remove(question_id)
            recent.insert(0, question_id)
            user["recent_questions"][category] = recent[:RECENT_QUESTIONS_LIMIT]
            self._save_users()

    def get_recent_questions(self, username, category):
        with self._lock:
            user = self._users.get(username)
            if not user:
                return []
            return list(user["recent_questions"].get(category, []))
