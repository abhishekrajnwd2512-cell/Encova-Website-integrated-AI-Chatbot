from app.config import Config

def test_config_values():
    assert Config.APP_NAME is not None
    assert Config.GEMINI_API_KEY is not None
    assert Config.MODEL is not None
    assert isinstance(Config.TEMPERATURE, float)