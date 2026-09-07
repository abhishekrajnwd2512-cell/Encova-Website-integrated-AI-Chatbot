import logging
from app import logging_config
from app.conversation import Conversation 
from app.prompt_manager import PromptManager
from app.config import Config
import os 
from app.usage_tracker import UsageTracker
from datetime import datetime 
from app.gemini_client import generate_streaming_response, create_chat 


def main():
    print(f"{Config.APP_NAME} is starting...")
    logging.info("Application started") 

    conversation = Conversation()
    prompt_manager = PromptManager()
    usage_tracker = UsageTracker()

    os.makedirs("exports", exist_ok=True) 

    prompts = prompt_manager.list_prompts() 

    print("Available Prompts:")

    for index, prompt in enumerate(prompts, start=1):
        print(f"{index}.{prompt}") 

    while True:
        try:
            choice = int(input("Choose A Prompt: "))
        
            if choice < 1 or choice > len(prompts):
                logging.warning(f"Invalid prompt choice: {choice}")
                print("Invalid prompt choice. Please choose a number from 1 to 3.")
                continue

            break

        except ValueError:
            logging.error("User entered an invalid prompt choice")
            print("Please enter a valid number.")
    
    selected_filename = prompts[choice - 1] 
    logging.info(f"User selected prompt: {selected_filename}")

    system_prompt = prompt_manager.get_prompt(selected_filename)

    conversation.add_message("system", system_prompt)

    chat = create_chat(system_prompt)

    print("\nChat started! Type 'exit' to quit.\n ") 

    while True:
        user_input = input("You: ")

        if not user_input.strip():
            print("Please eneter a message.")
            continue 

        if user_input.strip().lower() == "exit":
            print("Goodbye")
            break 

        if user_input.strip().lower() == "/reset":
            conversation.reset()
            conversation.add_message("system", system_prompt)
            chat = create_chat(system_prompt)
            print("Conversation has been reset", conversation.get_history())
            continue

        if user_input.strip().lower() == "/export":
            timestap = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"exports/conversation_{timestap}.txt"
            conversation.export(filename)
            print("Conversation exported successfully.")
            continue 

    
        conversation.add_message("user", user_input)

        response = generate_streaming_response(
            chat,
            user_input,
            usage_tracker        
            )
        
        conversation.add_message("assistant", response)

if __name__ == "__main__":
    main() 