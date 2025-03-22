from src.services.data_service import DataService
from src.components_view.data_page_view import DataPageView
from src.components_view.report_page_view import ReportPageView
from src.dto.base_dto import *
from src.widgets.text_edit_widget import TextEditWidget
import flet as ft

from time import time, sleep
from datetime import datetime

from loguru import logger

import os
from pathlib import Path

class App:
    def __init__(
        self,
        root: ft.Page, 
        data_service:DataService,
    ):
        self.picked_report_id = None
        self.tew = None # text edit widget
        
        self.__data_service = data_service
        
        self.root = root
        self.root.title = "desktop-app"
        self.root.theme_mode = ft.ThemeMode.DARK
        
        self.root.appbar = ft.AppBar(
            title=ft.Text(""),
            center_title=True,
            bgcolor=ft.Colors.BLACK12,
        )
        
        self.data_view   = DataPageView()
        self.report_view = None
        
        self.file_picker = ft.FilePicker(
            on_result=self.on_dialog_result
        )
 
        

    def init(self):
        reports = self.__data_service.get_reports_list()
        for report in reports:
            self.data_view.table.add_col_row(
                report,
                open_function = self.open_report(report),
                del_function  = lambda e: e
            )
        self.data_view.button.on_click = lambda e: self.add_report(e)
        self.root.add(self.data_view.get_view())
        
        
    
    
    def open_report(self, report_dto:ReportDTO):
        def inner(e):
            print('open function')
            self.root.overlay.clear()
            self.root.overlay.extend(
                [self.file_picker]
            )
            
            self.report_view = ReportPageView(
                report_dto,
                edit_function=self.edit_markup,
                back_function=self.back_function,
                add_audo_function= self.pick_file(report_dto.id_)
            )
            self.root.clean()
            self.root.add(self.report_view.get_view())
            
            self.root.update()
            print('finished')
        return inner
    
    def add_report(self, e):
        id_ = str(int(time() * 100))
        name = f'Замеры произведенные в соответствии с {time()}'
        edit_time=str(datetime.now())
        
        report = ReportDTO(
            id_ = id_,
            name= name,
            edit_time = edit_time,
            markdown_list = [],
            description = ''
        )
        
        self.__data_service.add_report(
            report
        )
        
        self.data_view.table.add_col_row(
            report,
            open_function = self.open_report(report),
            del_function  = lambda e: e
        )
        
        self.root.clean()
        self.root.add(self.data_view.get_view())
        
    def back_function(self, e):
        self.root.clean()
        self.root.add(self.data_view.get_view())
    
    
    def pick_file(self, report_id:str):
        def inner(e):
            self.root.overlay.clear()
            self.root.overlay.extend(
                [self.file_picker]
            )
            self.root.update()
            self.file_picker.pick_files(allow_multiple=True)
            self.picked_report_id = report_id
        return inner
    
    def edit_markup(
        self,
        text: str
    ):
        def save_(e):
            print(self.tew.plain_text.value)
            
        
        def clear_overlay(e):
            self.root.overlay.clear()
            self.root.update()
            
        self.tew = TextEditWidget(
            text,
            save_function=save_,
            back_function=clear_overlay
        )
        
        
        
            
        def iner(e):
            
            self.root.overlay.clear()
            self.root.overlay.append(
                self.tew.get_view()
            )
            self.root.update()
        return iner
        
    def on_dialog_result(self, e: ft.FilePickerResultEvent):
        print(self.picked_report_id)
        
        
        self.root.overlay.append(
            ft.Container(
                ft.Row(
                    [
                        ft.Column(
                            [
                            ft.ProgressRing(width=16, height=16, stroke_width = 3)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                bgcolor=ft.colors.BLACK12
            )
        )
        
        
        
        self.root.update()
        if e.files is not None:
            for file in e.files:
                print(file.path)
                
                markup_dto = MarkdownDTO(
                    markup_id=str(int(time() * 100)),
                    start_time='start',
                    end_time='end',
                    deep=time()%100,
                    step='step',
                    comment='123 '*int(time()%10), 
                    audio_path=r'C:\Users\Марков Владимир\Documents\GitHub\pro-tec-2\converted.wav',
                    raw_text=file.path
                )
                self.__data_service.add_audio(
                    markup_dto,
                    str(self.picked_report_id),
                )
                self.report_view.report_state.markdown_list.append(markup_dto)
                sleep(0.5)
            
        
        
        self.picked_report_id = None
        
        self.report_view.update_table()
        self.root.clean()
        self.root.add(self.report_view.get_view())
        self.root.overlay.clear()
        self.root.update()