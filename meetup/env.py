from dataclasses import dataclass, fields
from typing import Self

from dotenv import dotenv_values


@dataclass
class Env:
    MEETUP_COM_CLIENT_KEY: str
    MEETUP_COM_SECRET: str
    MEETUP_COM_SIGNING_KEY_ID: str
    MEETUP_COM_AUTHORIZED_MEMBER_ID: str
    MEETUP_COM_PRIVATE_KEY_PATH: str

    def __repr__(self) -> str:
        sensitive_keywords = ["KEY", "PASSWORD", "SECRET", "TOKEN"]
        return (
            type(self).__name__
            + "("
            + ", ".join(
                (
                    f"{field.name}='****'"
                    if any(kw in field.name for kw in sensitive_keywords)
                    else f"{field.name}='{getattr(self, field.name)}'"
                )
                for field in fields(self)
            )
            + ")"
        )

    @classmethod
    def get_env(cls) -> Self:
        return cls(**dotenv_values(".env"))
