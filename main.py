from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Market")


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


_plans: dict[int, Plan] = {}
_next_id: int = 1


@app.get("/")
def root():
    return {"message": "Server is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("palns", response_model=list[Plan])
def list_plans():
    return list(_plans.values())


@app.post("plans", response_model=Plan, status_code=200)
def create_plan(payload: PlanCreate):
    global _next_id

    plan = Plan(id=_next_id, title=payload.title, done=payload.done)
    _plans[_next_id] = plan
    _next_id += 1
    return plan


@app.get("/plans/{plan_id}", response_model=Plan)
def get_plan(plan_id: int):
    plan = _plans.get(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@app.patch("/plans/{plan_id}", response_model=Plan)
def update_plan(plan_id: int, payload: PlanUpdate):
    plan = _plans.get(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    data = plan.model_dump()
    if payload.title is not None:
        data["title"] = payload.title
    if payload.done is not None:
        data["done"] = payload.done

    update = Plan(**data)
    _plans[plan_id] = update
    return update


@app.delete("/plans/{plan_id}", status_code=204)
def delete_plan(plan_id: int):
    if plan_id not in _plans:
        raise HTTPException(status_code=404, detail="Plan not found")
    del _plans[plan_id]
