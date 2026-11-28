from week01.database import init_db, save_message, get_history, delete_history

TEST_SESSION = "pytest_user" 

def test_save_and_get_history():
    init_db()
    delete_history(TEST_SESSION)  # Ensure a clean state before the test
    save_message(TEST_SESSION, "user", "Hello, this is a test message.")
    save_message(TEST_SESSION, "assistant", "Hello, this is a test reply.")

    history = get_history(TEST_SESSION)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello, this is a test message."
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Hello, this is a test reply."

    delete_history(TEST_SESSION)  # Clean up after the test


def test_sliding_window_history():
    init_db()
    delete_history(TEST_SESSION)  # Ensure a clean state before the test
    save_message(TEST_SESSION, "user", "Hello, this is a test message.")
    save_message(TEST_SESSION, "assistant", "Hello, this is a test reply.")
    save_message(TEST_SESSION, "user", "You can change the content of this message.")
    save_message(TEST_SESSION, "assistant", "Yes, I can help you with that. What would you like to change?")

    history = get_history(TEST_SESSION, limit=2)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"
    assert history[0]["content"] == "You can change the content of this message."
    assert history[1]["content"] == "Yes, I can help you with that. What would you like to change?"
    delete_history(TEST_SESSION)  # Clean up after the test

def test_delete_history():
    init_db()
    delete_history(TEST_SESSION)  # Ensure a clean state before the test
    save_message(TEST_SESSION, "user", "Hello, this is a test message.")
    save_message(TEST_SESSION, "assistant", "Hello, this is a test reply.")

    delete_history(TEST_SESSION)
    history = get_history(TEST_SESSION)
    assert len(history) == 0  # History should be empty after deletion
