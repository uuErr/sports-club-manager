import os
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, text

from app import db, main
from app.db_schema import SCHEMA_DDL


@pytest.fixture
def booking_engine(tmp_path, monkeypatch):
    # An optional MySQL run uses an isolated database initialized with install.sql.
    url = os.getenv("SPORTS_BOOKING_TEST_MYSQL_URL")
    engine = create_engine(url or f"sqlite:///{tmp_path / 'booking.sqlite3'}")
    if url is None:
        with engine.begin() as conn:
            for statement in SCHEMA_DDL:
                conn.exec_driver_sql(statement)
    monkeypatch.setattr(db, "engine", engine)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.mark.parametrize(("same_member", "capacity", "second_status"), [(False, 10, 2), (True, 11, 1)])
def test_concurrent_booking(booking_engine, same_member, capacity, second_status):
    tag = uuid4().hex
    users = []
    tokens = []
    with booking_engine.begin() as conn:
        for index in range(11):
            token = f"{tag}-{index}"
            user = conn.execute(
                text("insert into users(username, password, state) values (:name, 'test', 2)"),
                {"name": token},
            ).lastrowid
            conn.execute(
                text("insert into tokens(user_id, token) values (:uid, :token)"),
                {"uid": user, "token": token},
            )
            users.append(user)
            tokens.append(token)
        action_id = conn.execute(
            text("insert into actions(title, max_num, state) values (:title, :capacity, 2)"),
            {"title": tag, "capacity": capacity},
        ).lastrowid
        conn.execute(
            text("insert into records(user_id, action_id, state, borrow) values (:uid, :aid, 0, 0)"),
            [{"uid": user, "aid": action_id} for user in users[:9]],
        )

    first_at_insert, second_at_gate, release_first = Event(), Event(), Event()

    def pause_before_insert(conn, cursor, statement, params, context, executemany):
        sql = statement.strip().lower()
        if sql.startswith("insert into records"):
            if first_at_insert.is_set():
                # Without serialization the second request also decides to insert.
                second_at_gate.set()
            else:
                first_at_insert.set()
                assert release_first.wait(timeout=8), "first booking was never released"
        elif first_at_insert.is_set() and (sql == "begin immediate" or sql.endswith("for update")):
            second_at_gate.set()

    def book(token):
        with TestClient(main.app) as client:
            response = client.post("/api/action/attendAction", params={"token": token, "action_id": action_id})
        assert response.status_code == 200
        return response.json()["status"]

    event.listen(booking_engine, "before_cursor_execute", pause_before_insert)
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(book, tokens[9])
            try:
                assert first_at_insert.wait(timeout=5), "first request did not reach INSERT"
                second = pool.submit(book, tokens[9 if same_member else 10])
                assert second_at_gate.wait(timeout=5), "second request did not reach the booking check"
            finally:
                release_first.set()
            statuses = [first.result(timeout=8), second.result(timeout=8)]
        with booking_engine.connect() as conn:
            enrolled = conn.execute(
                text("select user_id from records where action_id=:aid order by ID"), {"aid": action_id}
            ).scalars().all()
        assert (statuses, enrolled) == ([3, second_status], users[:10])
    finally:
        event.remove(booking_engine, "before_cursor_execute", pause_before_insert)
        with booking_engine.begin() as conn:
            conn.execute(text("delete from records where action_id=:aid"), {"aid": action_id})
            conn.execute(text("delete from actions where ID=:aid"), {"aid": action_id})
            for user in users:
                conn.execute(text("delete from tokens where user_id=:uid"), {"uid": user})
                conn.execute(text("delete from users where ID=:uid"), {"uid": user})
