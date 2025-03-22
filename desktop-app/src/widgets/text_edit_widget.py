import flet as ft
from datetime import datetime
from src.dto.base_dto import *
class TextEditWidget:
    WIDTH    = 1000
    HEIGHT   = 500
    
    FC_WIDTH = 500 - 60
    SC_WIDTH = 300 - 30
    TC_WIDTH = 200 
    
    def __init__(
            self,
            text:str,
            save_function,
            back_function
        ):
        self.plain_text = ft.TextField(
            value=text,
            height=200,
            min_lines=4,
            bgcolor=ft.colors.WHITE24
        )
        self.save_button = ft.ElevatedButton(
            text="save",
            icon=ft.icons.ARROW_BACK,
            on_click=save_function,
            bgcolor=ft.colors.GREEN_900
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
                                alignment=ft.MainAxisAlignment.SPACE_AROUND
                            ),
                            padding=20,
                            bgcolor=ft.colors.BLACK,
                            border_radius=10,
                            width=400,
                            height=400
                            
                        ),
                        
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.colors.BLACK12
        )