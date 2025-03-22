from src.dto.base_dto import *

from pathlib import Path
import json
import os
from loguru import logger
from time import time
import shutil



class DataService:
    
    def __init__(self):
        self.fs_route = Path("tmp_file_system")
        
    def add_report(self, pure_report_dto:ReportDTO):
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
        os.mkdir(self.fs_route.joinpath(pure_report_dto.id_).joinpath('meta'))
        
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
                            markdown_list = self.__get_audio_list(id_)
                        )
                    )
            except Exception as e:
                logger.warning(f'get_reports_list: {e}')
        return reports
    
    def add_audio(
        self,
        markup_dto:MarkdownDTO,
        report_id:str
    ):
        # try:
            with open(self.fs_route.joinpath(report_id).joinpath('decode').joinpath(f'{markup_dto.markup_id}.txt'), 'w') as file:
                file.write(
                    markup_dto.model_dump_json()
                )
            shutil.copyfile(
                markup_dto.audio_path,
                self.fs_route.joinpath(report_id).joinpath('tracks').joinpath(f'{markup_dto.markup_id}.wav')
            )
        # except Exception as e:
        #     print(e)
            
    def __get_audio_list(self, report_id) -> list[MarkdownDTO]:
        audio_list = []
        for file_name in os.listdir(self.fs_route.joinpath(report_id).joinpath('decode')):
            with open(self.fs_route.joinpath(report_id).joinpath('decode').joinpath(file_name)) as file:
                try:
                    audio_list.append(
                        MarkdownDTO.model_validate_json(file.read())
                    )
                except Exception as e:
                    logger.error(
                        f'__get_audio_list: {e}'
                    )
        return audio_list