# conversation_memory.py

class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, user_input, response):
        self.history.append({
            "user": user_input,
            "response": response
        })

    def get_context(self, last_n=3):
        return self.history[-last_n:]

    def reset(self):
        self.history = []