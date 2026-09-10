from typing import Annotated

from fastapi import Depends, HTTPException, Request

from app.messaging.rabbitmq import RabbitClient


def get_rabbit(request: Request) -> RabbitClient:
    rabbit = getattr(request.app.state, "rabbit", None)

    if rabbit is None:
        raise HTTPException(
            status_code=503,
            detail="RabbitMQ is not available",
        )

    return rabbit


RabbitDep = Annotated[
    RabbitClient,
    Depends(get_rabbit),
]
