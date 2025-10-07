import uuid
from datetime import datetime
from typing import Dict, List, Optional

from models import Message, MessageType


class MessageBus:
    """Handles communication between agents"""

    def __init__(self):
        self.messages: List[Message] = []
        self.agent_inboxes: Dict[str, List[Message]] = {}

    def register_agent(self, agent_id: str):
        """Register an agent to receive messages"""
        if agent_id not in self.agent_inboxes:
            self.agent_inboxes[agent_id] = []

    def send_message(
        self,
        from_agent: str,
        content: str,
        to_agent: Optional[str] = None,
        message_type: MessageType = MessageType.PRIVATE,
    ) -> Message:
        """Send a message from one agent to another or broadcast"""
        message = Message(
            id=str(uuid.uuid4()),
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            content=content,
            timestamp=datetime.now(),
        )

        self.messages.append(message)

        # Deliver to recipients
        if message_type == MessageType.BROADCAST:
            for agent_id in self.agent_inboxes:
                if agent_id != from_agent:
                    self.agent_inboxes[agent_id].append(message)
        elif to_agent and to_agent in self.agent_inboxes:
            self.agent_inboxes[to_agent].append(message)

        return message

    def get_messages(self, agent_id: str, clear: bool = True) -> List[Message]:
        """Get messages for an agent"""
        if agent_id not in self.agent_inboxes:
            return []

        messages = self.agent_inboxes[agent_id].copy()
        if clear:
            self.agent_inboxes[agent_id].clear()
        return messages

    def get_all_messages(self) -> List[Message]:
        """Get all messages in the system (for monitoring)"""
        return self.messages.copy()
