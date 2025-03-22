import flet as ft
from src.widgets.table_values_widget import TableValuesWidget
from time import time
from datetime import datetime
from src.dto.base_dto import *
from loguru import logger

class ReportPageView:
    def __init__(self, report_dto: ReportDTO, edit_function, back_function, add_audo_function):
        
        self.report_state = report_dto
        
        self.id_field = ft.Text(str(f'id: {report_dto.id_}'), width=200)
        self.name_field = ft.TextField(
            value=report_dto.name, 
            width=700, 
            bgcolor=ft.colors.WHITE24,
        )
        self.description_field=ft.TextField(
            value=report_dto.description,
            width=1000,
            height=100,
            min_lines=3,
            bgcolor=ft.colors.WHITE24,
            multiline=True,
        )
        self.back_button = ft.ElevatedButton(
            text="назад",
            icon=ft.icons.ARROW_BACK,
            on_click=back_function
        )
        
        self.select_files_button = ft.ElevatedButton(
            text="Добавить",
            icon=ft.icons.UPLOAD_FILE,
            on_click=add_audo_function,
            bgcolor=ft.colors.GREEN_ACCENT,
            col=ft.colors.WHITE
        )
        
        self.values_table = TableValuesWidget()
        self.__edit_function = edit_function
        
        for markup in self.report_state.markdown_list:
            logger.warning(markup.markup_id)
            self.values_table.add_col_row(
                markup.markup_id,
                start_time=markup.start_time,
                end_time=markup.end_time,
                deep=markup.deep,
                step=markup.step,
                comment=markup.comment,
                edit_function = lambda e: self.__edit_function(self.report_state.id_, markup),
                del_function  = lambda e: e
            )
        
    def update_table(self):
        self.values_table = TableValuesWidget()
        for markup in self.report_state.markdown_list:
            logger.warning(markup.markup_id)
            self.values_table.add_col_row(
                markup.markup_id,
                start_time=markup.start_time,
                end_time=markup.end_time,
                deep=markup.deep,
                step=markup.step,
                comment=markup.comment,
                edit_function = lambda e: self.__edit_function(self.report_state.id_, markup),
                del_function  = lambda e: e
            )
        
        

    def get_view(self):
        return ft.Row(
            [
                ft.Column(   
                    [
                        ft.Row(
                            [
                                self.back_button, 
                            ],
                            width=1000,
                            alignment=ft.MainAxisAlignment.END
                        ),
                        
                        ft.Row(
                            [
                                self.id_field,
                                self.name_field    
                            ],
                            width=1000,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        self.description_field,
                        ft.Row(
                            [
                                self.select_files_button, 
                            ],
                            width=1000,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        self.values_table.get_view()
                        
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )