import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FEEDBACK_FILE = os.path.join(BASE_DIR, "feedback.json")


class FeedbackStore:
    def __init__(self):
        self.data = self._load()

        if not os.path.exists(FEEDBACK_FILE):
            self.save()

    def _load(self):
        if not os.path.exists(FEEDBACK_FILE):
            return {}

        try:
            with open(FEEDBACK_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("[WARN] feedback.json is empty or corrupted. Resetting.")
            return {}
        except Exception as e:
            print(f"[ERROR] Failed to load feedback: {e}")
            return {}

    def save(self):
        os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)

        with open(FEEDBACK_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_feedback(self, query, feedback):
        query = query.strip().lower()

        if query not in self.data:
            self.data[query] = {"good": 0, "bad": 0}

        self.data[query][feedback] += 1
        self.save()

    def get_feedback(self, query):
        query = query.strip().lower()
        return self.data.get(query, {"good": 0, "bad": 0})