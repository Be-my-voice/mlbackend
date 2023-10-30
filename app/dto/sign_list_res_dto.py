from pydantic import BaseModel
from pyparsing import List

class SignRecord(BaseModel):
    name: str
    number_of_records: int


class SignRecordList(BaseModel):
    records: List[SignRecord]
    message: str = ""

    def addRecord(self, record: SignRecord):
        self.records.append(record)

    def setMessage(self, message: str):
        self.message = message




