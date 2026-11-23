import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from SERVER.persistence.database import SessionLocal, engine, init_db
from SERVER.persistence.models import Message, Session as SessionModel


async def main():
    await init_db()

    # 1) Traegt die Verbindung das PRAGMA?
    async with engine.connect() as conn:
        value = (await conn.execute(text("PRAGMA foreign_keys"))).scalar()
    print("1) PRAGMA foreign_keys =", value, "(erwartet: 1)")

    # 2) Waise: Nachricht ohne passende Session
    async with SessionLocal() as session:
        session.add(Message(session_id="gibt-es-nicht", role="user", content="test"))
        try:
            await session.commit()
            print("2) FEHLER: Commit ging durch -> FK wird NICHT erzwungen")
        except IntegrityError as exc:
            print("2) OK: IntegrityError ->", type(exc.orig).__name__)
        await session.rollback()

    # 3) Cascade: Session direkt per SQL loeschen, Nachrichten muessen mitgehen
    async with SessionLocal() as session:
        s = SessionModel(id="test-cascade", user_id="test")
        s.messages.append(Message(role="user", content="hallo"))
        session.add(s)
        await session.commit()

    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM sessions WHERE id = :sid"), {"sid": "test-cascade"})
        left = (await conn.execute(
            text("SELECT count(*) FROM messages WHERE session_id = :sid"), {"sid": "test-cascade"}
        )).scalar()
    print("3) Nachrichten nach DELETE der Session:", left, "(erwartet: 0)")


asyncio.run(main())