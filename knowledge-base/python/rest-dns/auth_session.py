import uuid
import time

SESSIONS = {}

SESSION_TTL = 120  # 2 minutos


def create_session(username, user_data):
    session_id = str(uuid.uuid4())

    SESSIONS[session_id] = {
        "username": username,
        "user": user_data,
        "created": time.time()
    }

    return session_id


def get_session(session_id):
    session = SESSIONS.get(session_id)

    if not session:
        return None

    if time.time() - session["created"] > SESSION_TTL:
        del SESSIONS[session_id]
        return None

    return session


def delete_session(session_id):
    if session_id in SESSIONS:
        del SESSIONS[session_id]
        