from src.services.data_service import DataService
import flet as ft
from src.components_view.data_page_view import DataPageView
from src.components_view.report_page_view import ReportPageView
from time import time
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
        
        self.__data_service = data_service
        
        self.root = root
        self.root.title = "desktop-app"
        self.root.theme_mode = ft.ThemeMode.DARK
        
        self.root.appbar = ft.AppBar(
            title=ft.Text("отчеты"),
            center_title=True,
            bgcolor=ft.Colors.BLACK12,
        )
        
        self.data_view   = DataPageView()
        self.report_view = None

    def init(self):
        reports = self.__data_service.get_reports_list()
        for report in reports:
            self.data_view.table.add_col_row(
                id   = report['id'],
                name = report['name'],
                edit_time=report['edit_time'],
                open_function = self.open_report(report),
                del_function  = lambda e: e
            )
        self.data_view.button.on_click = lambda e: self.add_report(e)
        self.root.add(self.data_view.get_view())
        # self.root.add(self.report_view.get_view())
    
    
    def open_report(self, info_dict):
        def inner(e):
            print('open function')
            self.report_view = ReportPageView(
                id_=info_dict['id'],
                name=info_dict['name'],
                description=info_dict['description'],
                back_function=self.back_function
            )
            self.root.clean()
            self.root.add(self.report_view.get_view())
            print('finished')
        return inner
    
    def add_report(self, e):
        id_ = int(time() * 100)
        name = f'Замеры произведенные в соответствии с {time()}'
        edit_time=str(datetime.now())
        
        report = {
            'id':   id_,
            'name': name,
            'edit_time': edit_time,
            'description': ''
            
        }
        
        self.__data_service.add_report(
            id_,
            name,
            last_edit_time=edit_time
        )
        
        self.data_view.table.add_col_row(
            id   = id_,
            name = name,
            edit_time=edit_time,
            open_function = self.open_report(report),
            del_function  = lambda e: e
        )
        
        self.root.clean()
        self.root.add(self.data_view.get_view())
        
    def back_function(self, e):
        self.root.clean()
        self.root.add(self.data_view.get_view())