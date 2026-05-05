import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FEEDBACK_FILE = os.path.join(BASE_DIR, "feedback.json")

def __init__(self):
    self.data = self._load()

    # Ensure file exists
    if not os.path.exists(FEEDBACK_FILE):
        self.save()