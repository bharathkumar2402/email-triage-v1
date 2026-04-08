from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum


class UrgencyLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class SenderIntent(str, Enum):
    REQUEST = "REQUEST"
    ALERT = "ALERT"
    FYI = "FYI"
    ESCALATION = "ESCALATION"


class EmailAction(BaseModel):
    """Agent's action"""
    urgency: UrgencyLevel
    key_action: str = Field(..., max_length=200)
    sender_intent: SenderIntent
    response: Optional[str] = Field(None, max_length=500)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class EmailObservation(BaseModel):
    """Environment observation"""
    email_id: str
    subject: str
    body: str
    sender: str
    timestamp: str
    email_chain_length: int = 0
    previous_messages: List[str] = []
    context_available: bool = True


class EmailReward(BaseModel):
    """Reward structure"""
    correctness: float
    action_relevance: float
    response_quality: float
    efficiency: float
    penalty: float = 0.0
    total: float


class StepResult(BaseModel):
    """Step result"""
    observation: EmailObservation
    reward: EmailReward
    done: bool
    info: Dict = {}