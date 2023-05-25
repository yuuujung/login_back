from pydantic import BaseModel, Field


class RegisterArgument(BaseModel):
    user_id: str = Field(..., max_length=50)
    user_pw: str = Field(..., max_length=200)
    # user_nm: str = Field(..., max_length=50)
