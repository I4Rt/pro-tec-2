from pydantic import BaseModel

class MarkdownDTO(BaseModel):
    start_time:str
    end_time:  str
    deep:      float
    step:      str
    comment:   str


class PureReportDTO(BaseModel):
    id_:         str
    name:        str
    description: str
    edit_time:   str
    
class ReportDTO(PureReportDTO):
    markdown_list: list[MarkdownDTO]
    class Config:
        arbitrary_types_allowed = True
    