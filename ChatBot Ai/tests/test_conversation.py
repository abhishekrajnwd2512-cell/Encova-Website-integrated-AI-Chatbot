from app.conversation import Conversation 

def test_add_message():
    conversation = Conversation() 

    conversation.add_message("user", "Hello")

    history = conversation.get_history()

    assert len(history) == 1
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"

def test_reset():
    conversation = Conversation()

    conversation.add_message("user", "Hello")
    conversation.add_message("assistant", "Hi!")

    conversation.reset() 

    history = conversation.get_history() 
    assert history == [] 

def test_get_history():
    conversation = Conversation()

    conversation.add_message("user", "Hello")
    conversation.add_message("assistant", "Hi!")

    history = conversation.get_history() 

    assert len(history) == 2 
    assert history[0]["content"] == "Hello"
    assert history[1]["content"] == "Hi!"

def test_export(tmp_path):
    conversation = Conversation() 

    conversation.add_message("user", "Hello")
    conversation.add_message("assistant", "Hi!")

    filename = tmp_path / "conversation.txt"

    conversation.export(filename) 

    assert filename.exists()

    content = filename.read_text() 

    assert "user: Hello" in content
    assert "assistant: Hi!" in content 
