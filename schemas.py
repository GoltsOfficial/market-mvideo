from pydantic import BaseModel, Field


class PlanCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class PlanUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    done: bool = False


class Plan(BaseModel):
    id: int
    title: str
    done: bool
