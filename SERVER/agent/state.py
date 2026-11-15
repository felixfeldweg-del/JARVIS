from dataclasses import dataclass, field 
from datetime import datetime, timezone
from enum import enum 
from typing import Literal
from uuid import uuid4

class AgentStatus(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    WAITING_FOR_TOOL = "waiting_for_tool"
    LISTENING = "listening"
    ERROR = "error"
    CLOSED = "closed"

@dataclass
class Message:
    role: Literal["system", "user", "asistant", "tool"]
    content: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class AgentSate:
    user_id: str
    session_id: str = field(
        default_factory= lambda: str(uuid4())
    )

    status: AgentStatus = AgentStatus.IDLE
    messages: list[Message] = field(default_factory=list)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_message(self, role: Literal["system", "user", "asistant", "tool"], content: str):
        message = Message(role=role, content=content)

        self.messages.append(message)
        self.updated_at = datetime.now(timezone.utc)

    def set_status(self, status: AgentStatus):
        self.status = status 
        self.updated_at = datetime.now(timezone.utc)
