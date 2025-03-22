from src.dto.base_dto import *

from pathlib import Path
import json
import os
from loguru import logger



class DataService:
    
    def __init__(self):
        self.fs_route = Path("tmp_file_system")
        
    def add_report(self, pure_report_dto:PureReportDTO):
        os.mkdir(self.fs_route.joinpath(pure_report_dto.id_))
        with open(self.fs_route.joinpath(pure_report_dto.id_).joinpath('report_info.txt'), 'w') as file:
            file.write(
                json.dumps(
                    {
                        'name': pure_report_dto.name,
                        'description': pure_report_dto.description,
                        'edit_time': pure_report_dto.edit_time
                    }
                )
            )
        os.mkdir(self.fs_route.joinpath(pure_report_dto.id_).joinpath('tracks'))
        os.mkdir(self.fs_route.joinpath(pure_report_dto.id_).joinpath('decode'))
        
    def get_reports_list(self) -> list[ReportDTO]:
        reports = []
        print(os.listdir(self.fs_route))
        for id_ in os.listdir(self.fs_route):
            try:
                with open(self.fs_route.joinpath(str(id_)).joinpath('report_info.txt'), 'r') as file:
                    data = json.loads(file.read())
                    reports.append(
                        ReportDTO(
                            id_           = id_,
                            name          = data['name'],
                            description   = data['description'],
                            edit_time     = data['edit_time'],
                            markdown_list = []
                        )
                    )
            except Exception as e:
                logger.warning(f'get_reports_list: {e}')
        return reports