from src.dto.base_dto import *

from pathlib import Path
import json
import os
from loguru import logger
from time import time
import shutil
import csv



class DataService:
    
    def __init__(self):
        self.fs_route = Path("tmp_file_system")
        self.save_route = Path("reports")
        
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
    
    def get_report(self, report_id) -> ReportDTO:
        with open(self.fs_route.joinpath(str(report_id)).joinpath('report_info.txt'), 'r') as file:
            data = json.loads(file.read())
            return ReportDTO(
                    id_           = report_id,
                    name          = data['name'],
                    description   = data['description'],
                    edit_time     = data['edit_time'],
                    markdown_list = self.__get_audio_list(report_id)
                )
    
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
    
    def edit_markup(
        self,
        report_id,
        markup_dto:MarkdownDTO
    ):
        
        with open(self.fs_route.joinpath(report_id).joinpath('decode').joinpath(f'{markup_dto.markup_id}.txt'), 'w') as file:
            file.write(
                markup_dto.model_dump_json()
            )
        
    # Функция для сохранения ReportDTO в CSV
    def get_csv(report: ReportDTO, filename: str):
        # Определяем заголовки столбцов
        fieldnames = ["markup_id", "start_time", "end_time", "deep", "step", "comment", "audio_path", "raw_text"]
        
        # Открываем файл для записи
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Записываем заголовки
            writer.writeheader()
            
            # Записываем данные из markdown_list
            for markdown in report.markdown_list:
                writer.writerow(markdown.dict())
