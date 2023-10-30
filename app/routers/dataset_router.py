from fastapi import APIRouter

from app.services.dataset_service import list_signs, list_records, read_record
from app.dto.sign_list_res_dto import SignRecordList
from app.dto.record_list_res_dto import RecordList
from app.dto.record_landmarks_dto import JsonLandmarkRes
from app.dto.add_record_dto import AddRecord


dataset_router = APIRouter(
    tags=["datasets"],
    responses={404: {"description": "Not found"}},
)

@dataset_router.get("/list-classes", response_model=SignRecordList)
def list_classes():
    sign_list = list_signs()
    return sign_list

@dataset_router.get("/list-records/{class_name}", response_model=RecordList)
def list_classes(class_name):
    if(class_name == ""):
        record_list = RecordList(records=[], message="")
        record_list.setMessage("Invalid sign name")
        return record_list
    
    record_list = list_records(class_name)
    # record_list = RecordList()
    return record_list


@dataset_router.get("/record/{class_name}/{id}", response_model=JsonLandmarkRes)
def list_classes(class_name, id):
    return read_record(class_name, id)


@dataset_router.post("add-record")
def add_record(record: AddRecord):
    pass

