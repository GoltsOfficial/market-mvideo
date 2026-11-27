from fastapi import APIRouter, HTTPException
from enum import Enum
from schemas import *


router = APIRouter(prefix="/plans", tags=["plans"])


_plans: dict[int, Plan] = {}
_next_id: int = 1

class Tags(Enum):
    plans = "plans"


@router.get("/palns", response_model=list[Plan], tags=[Tags.plans])
def list_plans():
    return list(_plans.values())


@router.post("/plans", response_model=Plan, status_code=201, tags=[Tags.plans])
def create_plan(payload: PlanCreate):
    global _next_id

    plan = Plan(id=_next_id, title=payload.title, done=payload.done)
    _plans[_next_id] = plan
    _next_id += 1
    return plan


@router.get("/plans/{plan_id}", response_model=Plan, tags=[Tags.plans])
def get_plan(plan_id: int):
    plan = _plans.get(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.patch("/plans/{plan_id}", response_model=Plan, tags=[Tags.plans])
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


@router.delete("/plans/{plan_id}", status_code=204, tags=[Tags.plans])
def delete_plan(plan_id: int):
    if plan_id not in _plans:
        raise HTTPException(status_code=404, detail="Plan not found")
    del _plans[plan_id]
