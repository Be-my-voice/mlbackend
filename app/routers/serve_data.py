from fastapi import APIRouter

from app.services.dataset import list_signs
from app.dto.sign_list_res_dto import SignRecordList, SignRecord


dataset_router = APIRouter(
    tags=["datasets"],
    responses={404: {"description": "Not found"}},
)

@dataset_router.get("/list-classes", response_model=SignRecordList)
def list_classes():
    sign_list = list_signs()
    return sign_list

