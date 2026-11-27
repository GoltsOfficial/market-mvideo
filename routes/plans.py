"""CRUD API-роутер для управления планами [PLANS]."""

from fastapi import APIRouter, HTTPException
from enum import Enum

from schemas import *

router = APIRouter(prefix="/plans", tags=["plans"])

_plans: dict[int, Plan] = {}
_next_id: int = 1


class Tags(Enum):
    plans = "plans"


@router.get(
    "/palns",
    response_model=list[Plan],
    tags=[Tags.plans],
    summary="Get all plans available",
    response_description="List of all plans available"
)
def list_plans():
    """
    Get all plans available

    :param:
    - **id**: unique plan identifier
    - **title**: plan title
    - **done**: whether plan is done

    :return:
    - **list**: list of plans available
    """
    return list(_plans.values())


@router.post(
    "/plans",
    response_model=Plan,
    status_code=201,
    tags=[Tags.plans],
    summary="Create a new plan",
    response_description="Created a new plan"
)
def create_plan(payload: PlanCreate):
    """
    Create a new plan

    :param payload:
    - **title**: each plan must have a title
    - **done**: whether plan is done (default: False)

    :return:
    - **Plan**: the created plan with assigned **id**
    """
    global _next_id

    plan = Plan(id=_next_id, title=payload.title, done=payload.done)
    _plans[_next_id] = plan
    _next_id += 1
    return plan


@router.get(
    "/plans/{plan_id}",
    response_model=Plan,
    tags=[Tags.plans],
    summary="Get a plan",
    response_description="Get a plan of assigned **id**"
)
def get_plan(plan_id: int):
    """
    Get a plan

    :param plan_id:
    - **plan_id**: unique plan identifier

    :return:
    - **Plan**: the plan
    - **404**: if the plan does not found
    """
    plan = _plans.get(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.patch(
    "/plans/{plan_id}",
    response_model=Plan,
    tags=[Tags.plans],
    summary="Update a plan",
    response_description="Updated a plan with assigned **id**"
)
def update_plan(plan_id: int, payload: PlanUpdate):
    """
    Update a plan

    :param plan_id:
    - **plan_id**: unique plan identifier

    :param payload:
    - **title**: new plan title (optional)
    - **done**: plan new completion status (optional)

    :return:
    - **Plan**: the updated plan
    - **404**: if the plan does not found
    """
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


@router.delete(
    "/plans/{plan_id}",
    status_code=204,
    tags=[Tags.plans],
    summary="Delete a plan",
    response_description="Delete a plan of assigned **id**"
)
def delete_plan(plan_id: int):
    """
    Delete a plan

    :param plan_id:
    - **plan_id**: unique plan identifier

    :return:
    - **204**: on successfully deleted plan
    - **404**: if the plan does not found
    """
    if plan_id not in _plans:
        raise HTTPException(status_code=404, detail="Plan not found")
    del _plans[plan_id]
