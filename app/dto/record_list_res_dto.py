from pydantic import BaseModel
from pyparsing import List

class RecordList(BaseModel):
    records: List[int]
    message: str

    def addRecord(self, record: int):
        self.records.append(record)

    def setMessage(self, message: str):
        self.message = message




