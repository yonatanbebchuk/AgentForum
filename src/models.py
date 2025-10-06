from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MessageType(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    BROADCAST = "broadcast"


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"


class Stock(BaseModel):
    symbol: str
    price: float
    volume: int = 0


class Portfolio(BaseModel):
    cash: float = 100000.0
    holdings: Dict[str, int] = Field(default_factory=dict)  # symbol -> quantity


class Transaction(BaseModel):
    id: str
    agent_id: str
    transaction_type: TransactionType
    symbol: str
    quantity: int
    price: float
    timestamp: datetime = Field(default_factory=datetime.now)


class Message(BaseModel):
    id: str
    from_agent: str
    to_agent: Optional[str] = None  # None for broadcast
    message_type: MessageType
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class Memory(BaseModel):
    agent_id: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)


class LLMCall(BaseModel):
    id: str
    agent_id: str
    prompt: str
    response: str
    model: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    id: str
    agent_id: str
    tool_name: str
    arguments: Dict[str, Any]
    result: Any
    timestamp: datetime = Field(default_factory=datetime.now)


class InvestmentOpportunity(BaseModel):
    symbol: str
    description: str
    expected_return: float
    risk_level: str
    insider_info: bool = False  # Track if this is insider information
    source: Optional[str] = None  # Who shared this info
