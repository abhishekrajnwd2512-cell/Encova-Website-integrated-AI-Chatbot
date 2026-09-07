import pytest
from app.prompt_manager import PromptManager

def test_list_prompts():
    prompt_manager = PromptManager() 

    prompts = prompt_manager.list_prompts() 

    assert len(prompts) > 0

    for prompt in prompts:
        assert prompt.endswith(".txt") 

def test_get_prompt():
    prompt_manager = PromptManager()

    prompts = prompt_manager.list_prompts()

    filename = prompts[0] 

    content = prompt_manager.get_prompt(filename) 

    assert isinstance(content, str) 
    assert content.strip() != ""

def test_missing_prompt():
    prompt_manager = PromptManager() 

    with pytest.raises(FileNotFoundError):
        prompt_manager.get_prompt("does_not_exist.txt") 


