"""Workload routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from src.apps.api.auth import get_current_tenant
from src.apps.api.schemas.workloads import WorkloadCreate, WorkloadList, WorkloadRead
from src.domain.services.workload_service import WorkloadService

router = APIRouter(prefix="/workloads", tags=["workloads"])


@router.post("", response_model=WorkloadRead, status_code=201)
def create_workload(
    payload: WorkloadCreate,
    tenant=Depends(get_current_tenant),
    service: WorkloadService = Depends(WorkloadService),
) -> WorkloadRead:
    try:
        return service.create(
            tenant_id=tenant.tenant_id,
            name=payload.name,
            description=payload.description,
            tags_json=payload.tags_json,
            artifact_id=payload.artifact_id,
            fleet_template_id=payload.fleet_template_id,
            schedule_rules_json=payload.schedule_rules_json,
            user_preferences_json=payload.user_preferences_json,
            manual_runtime_seconds=payload.manual_runtime_seconds,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=WorkloadList)
def list_workloads(
    tenant=Depends(get_current_tenant),
    service: WorkloadService = Depends(WorkloadService),
) -> WorkloadList:
    items = list(service.list(tenant_id=tenant.tenant_id))
    return WorkloadList(items=items)


@router.get("/{workload_id}", response_model=WorkloadRead)
def get_workload(
    workload_id: int,
    tenant=Depends(get_current_tenant),
    service: WorkloadService = Depends(WorkloadService),
) -> WorkloadRead:
    workload = service.get(tenant_id=tenant.tenant_id, workload_id=workload_id)
    if workload is None:
        raise HTTPException(status_code=404, detail="Not found")
    return workload
