from google.adk.runners import InMemoryRunner

from agent import create_agent
from main import SESSION_ID, USER_ID, ensure_session


def test_ensure_session_creates_and_reuses_session():
    agent = create_agent()
    runner = InMemoryRunner(agent=agent)

    first_session = ensure_session(runner)
    second_session = ensure_session(runner)

    assert first_session is not None
    assert second_session is not None
    assert first_session.id == SESSION_ID
    assert second_session.id == SESSION_ID
    assert first_session.user_id == USER_ID
    assert second_session.user_id == USER_ID
