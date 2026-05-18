from pydantic import BaseModel, EmailStr, Field
from abc import ABC, abstractmethod


class NotificationPayload(BaseModel):
    """The Notification model represents the data structure for sending notifications."""
    user_id: int
    email: EmailStr
    message: str = Field(..., max_length=255)
    phone_number: str = Field(..., pattern=r"^\+\d{1,15}$")

# Dependency Inversion Principle (DIP)

class NotificationChannel(ABC):
    """Abstract base class for notification channels."""
    
    @abstractmethod
    def send(self, payload: NotificationPayload) -> bool:
        pass

class EmailChannel(NotificationChannel):

    def send(self, payload: NotificationPayload) -> bool:
        print(f"Sending email to {payload.email}: {payload.message}")
        # Here you would integrate with an actual email service
        return True
    
class SMSChannel(NotificationChannel):

    def send(self, payload: NotificationPayload) -> bool:
        print(f"Sending SMS to {payload.phone_number}: {payload.message}")
        # Here you would integrate with an actual SMS service
        return True
    
# The Core Notification Service (Single Responsibility)\

class NotificationService:
    def __init__(self, channels: list[NotificationChannel]):
        self.channels = channels

    def broadcast(self, payload: NotificationPayload):
        print(f"Broadcasting notification to user {payload.user_id}...")
        for channel in self.channels:
            if not channel.send(payload):
                print(f"Failed to send notification via {channel.__class__.__name__}")
        print("Notification broadcast completed successfully.")

# Example Usage

from pydantic import ValidationError

user1_channels = [EmailChannel(), SMSChannel()]
user1_notification = NotificationService(channels=user1_channels)

try:
    payload = NotificationPayload(
        user_id=123,
        email="test@gmail.com",
        message="Your order has been shipped!",
        phone_number="+1234567890"
    )
    user1_notification.broadcast(payload)
    
except ValidationError as e:
    print("Validation error:", e)