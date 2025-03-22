from pydantic import BaseModel

class MarkdownDTO(BaseModel):
    markup_id:  str
    start_time: str
    end_time:   str
    deep:       float
    step:       str
    comment:    str
    audio_path: str
    raw_text:   str


class PureReportDTO(BaseModel):
    id_:         str
    name:        str
    description: str
    edit_time:   str
    
class ReportDTO(PureReportDTO):
    markdown_list: list[MarkdownDTO]
    class Config:
        arbitrary_types_allowed = True
    