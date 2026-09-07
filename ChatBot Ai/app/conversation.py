class Conversation:
    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str) -> None:
        message = {
            "role":role,
            "content":content
        }

        self.messages.append(message) 

    def get_history(self) -> list:
        return self.messages 

    def reset(self) -> None:
        self.messages.clear() 

    def export(self, filename: str) -> None:
        with open(filename, "w") as file:
            for message in self.messages:
                file.write(f"{message['role']}: {message['content']}\n")

    
