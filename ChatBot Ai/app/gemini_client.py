from google import genai
from google.genai import types 
from app.config import Config 
import logging
from app.usage_tracker import UsageTracker
import time

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def create_chat(system_prompt: str):
    chat = client.chats.create(
        model=Config.MODEL,
        config=types.GenerateContentConfig(
            system_instruction= system_prompt
        )
    )

    return chat 

def generate_response(chat, user_input: str) -> str:
    try:
        response = chat.send_message(
            user_input
    )
        return response.text
    except Exception as e:
        logging.error(f"Gemini error: {e}")

        if "429" in str(e):
            print("⚠️ Gemini API quota exceeded. Please try again later.")
        else:
            print(f"Error: {e}")
    
def generate_streaming_response(chat, user_input: str, usage_tracker):
    try:
        start_time = time.time() 

        response = chat.send_message_stream(
            user_input
        )

        request_time = time.time()

        final_chunk = None
        full_response = ""

        print("AI: ", end="")

        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_response += chunk.text

            final_chunk = chunk

        end_time = time.time()
        print(f"\nResponse Time: {end_time - start_time:.2f} Seconds")
        print(f"Time to start streaming: {request_time - start_time:.2f} Seconds")
        print()

        usage = final_chunk.usage_metadata

        usage_tracker.add_usage(
            usage.prompt_token_count or 0,
            usage.candidates_token_count or 0,
            usage.thoughts_token_count or 0,
            usage.total_token_count or 0
        )

        usage_tracker.calculate_cost()

        print("Usage:")
        print(f"Input tokens: {usage.prompt_token_count}")
        print(f"Output tokens: {usage.candidates_token_count}")
        print(f"Thought tokens: {usage.thoughts_token_count}")
        print(f"Total tokens: {usage.total_token_count}")

        print()
        print("Session Total:")
        print(f"Input tokens: {usage_tracker.input_tokens}")
        print(f"Output tokens: {usage_tracker.output_tokens}")
        print(f"Thought tokens: {usage_tracker.thought_tokens}")
        print(f"Total tokens: {usage_tracker.total_tokens}")

        print(f"Input cost: ${usage_tracker.input_cost:.6f}")
        print(f"Output cost: ${usage_tracker.output_cost:.6f}")
        print(f"Total cost: ${usage_tracker.total_cost:.6f}")

        return full_response

    except Exception as e:
        logging.error(f"Gemini streaming error: {e}")

        if "429" in str(e):
            print("⚠️ Gemini API quota exceeded. Please try again later.")
        else:
            print("Sorry, I couldn't generate a response right now.")

if __name__ == "__main__":
    chat = create_chat("You are a helpful assistant. ")

    print(f"Model: {Config.MODEL}")

    start_time = time.time()

    answer = generate_response(
        chat,
        "hey"
    )

    end_time = time.time()

    print(f"AI: {answer}")
    print(f"Response Time: {end_time - start_time:.2f} Seconds")

    answer = generate_response(
        chat,
        "hey"
        )
    
    end_time = time.time()
    
    print(f"AI: {answer}")
    print(f"Response Time: {end_time - start_time:.2f} Seconds")

    answer = generate_response(
        chat,
        "hey"
            )
        
    end_time = time.time()
        
    print(f"AI: {answer}")
    print(f"Response Time: {end_time - start_time:.2f} Seconds")
        
    