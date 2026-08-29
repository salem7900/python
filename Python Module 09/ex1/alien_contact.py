#!/usr/bin/env python3
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional
from enum import Enum


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_contact_id_prefix(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id must start with 'AC'")
        return self

    @model_validator(mode="after")
    def check_verification(self) -> "AlienContact":
        if self.contact_type is ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        return self

    @model_validator(mode="after")
    def check_telepathic_witness(self) -> "AlienContact":
        if (self.contact_type is ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError("Telepathic contact "
                             "requires at least 3 witnesses")
        return self

    @model_validator(mode="after")
    def check_strong_signals(self) -> "AlienContact":
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should include messages")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)

    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime.fromisoformat("2024-03-10T22:15:00"),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=True,
    )

    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: '{contact.message_received}'")

    print("\n" + "=" * 40)

    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime.fromisoformat("2024-03-11T03:00:00"),
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=6.0,
            duration_minutes=20,
            witness_count=1,
            is_verified=False,
        )
    except ValidationError as exc:
        for error in exc.errors():
            msg = str(error["msg"])
            prefix = "Value error, "
            if msg.startswith(prefix):
                msg = msg[len(prefix):]
            print(msg)


if __name__ == "__main__":
    main()
