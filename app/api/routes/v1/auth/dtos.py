from pydantic import BaseModel


class Token(BaseModel):
    """
    Token response.

    Attributes:
        access_token (str | None): Acess token.
        token_type (str | None): Type of token.
    """

    access_token: str
    token_type: str = "bearer"
