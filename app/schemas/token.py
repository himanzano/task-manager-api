from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    model_config = ConfigDict(extra="forbid")


class TokenPayload(BaseModel):
    sub: str | None = None

    model_config = ConfigDict(extra="forbid")
