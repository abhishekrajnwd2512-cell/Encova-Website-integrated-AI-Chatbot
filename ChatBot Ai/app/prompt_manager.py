import os 

class PromptManager:
    def __init__(self):
        self.prompt_directory = "prompts"

    def load_prompt(self, filename:str) -> str:
        file_path = f"{self.prompt_directory}/{filename}" 

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read() 

    def list_prompts(self) -> list:
        files =  os.listdir(self.prompt_directory)

        return[
            file for file in files 
            if file.endswith(".txt")
        ]

    def get_prompt(self, filename: str) -> str:
        return self.load_prompt(filename) 