"""Fleet routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from src.apps.api.auth import get_current_tenant
from src.apps.api.schemas.fleets import FleetList, FleetRead
from src.domain.services.fleet_service import FleetService

router = APIRouter(prefix="/fleets", tags=["fleets"])


@router.get("", response_model=FleetList)
def list_fleets(
    tenant=Depends(get_current_tenant),
    service: FleetService = Depends(FleetService),
) -> FleetList:
    items = list(service.list())
    return FleetList(items=[FleetRead.model_validate(f) for f in items])
