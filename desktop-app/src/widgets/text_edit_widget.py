import flet as ft
from datetime import datetime
from src.dto.base_dto import *
from loguru import logger

class TextEditWidget:
    WIDTH    = 1000
    HEIGHT   = 500
    
    FC_WIDTH = 500 - 60
    SC_WIDTH = 300 - 30
    TC_WIDTH = 200 
    
    def __init__(
            self,
            report_id:str,
            markup_dto:MarkdownDTO,
            save_function,
            back_function
    ):
        logger.error(f'{markup_dto.markup_id} {markup_dto.raw_text}')
        self.report_id = report_id
        self.markup_dto = markup_dto
        self.plain_text = ft.TextField(
            value=markup_dto.raw_text,
            height=200,
            min_lines=10,
            multiline=True,
            bgcolor=ft.colors.WHITE24,
        )
        self.save_button = ft.ElevatedButton(
            text="save",
            icon=ft.icons.ARROW_BACK,
            on_click=save_function,
            bgcolor=ft.colors.GREEN_ACCENT
        )
        
        self.back_button = ft.ElevatedButton(
            text="back",
            icon=ft.icons.ARROW_BACK,
            on_click=back_function
        )
        
        
    def get_view(self):
        return ft.Container(
            ft.Row(
                [
                    ft.Column(
                        [
                        ft.Container(
                            ft.Column(
                                [
                                    self.plain_text,
                                    ft.Row(
                                        [
                                            self.save_button,
                                            self.back_button
                                        ],
                                        alignment=ft.MainAxisAlignment.END
                                    )
                                ],
                                expand=True
                            ),
                            padding=20,
                            bgcolor=ft.colors.WHITE,
                            border_radius=10,
                            width=400,
                            height=300
                            
                        ),
                        
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.colors.BLACK12
        )