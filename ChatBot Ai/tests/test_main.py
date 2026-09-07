from app.main import main

def test_main_exit(monkeypatch, capsys):

    inputs = iter([

        "1",
        "Hello",
        "exit"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()

    captured = capsys.readouterr() 

    assert "Goodbye" in captured.out
    assert "AI: i received your message!" in captured.out

def test_main_invalid_prompt(monkeypatch, capsys):

    inputs = iter([

        "99"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main()

    captured = capsys.readouterr() 

    assert "Invalid prompt choice." in captured.out

def test_main_non_number_prompt(monkeypatch, capsys):

    inputs = iter([
        "hello"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main()

    captured = capsys.readouterr()

    assert "Please enter a valid number." in captured.out

def test_main_reset(monkeypatch, capsys):

    inputs = iter([
        "1",
        "Hello",
        "/reset",
        "exit"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main()

    captured = capsys.readouterr()

    assert "Conversation has been reset" in captured.out

def test_main_export(monkeypatch, capsys):

    inputs = iter([
        "1",
        "Hello",
        "/export",
        "exit"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main()

    captured = capsys.readouterr()

    assert "Conversation exported successfully." in captured.out

def test_main_empty_message(monkeypatch, capsys):

    inputs = iter([
        "1",
        "",
        "exit"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    main()

    captured = capsys.readouterr()

    assert "Please eneter a message." in captured.out