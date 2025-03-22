import flet as ft
from src.widgets.table_widget import TableWidget

class DataPageView:
    def __init__(self):
        
        self.table = TableWidget()
        
        self.button = ft.ElevatedButton(
            text="добавить отчет",
            icon=ft.icons.ADD
        )

    def get_view(self):
        
        return ft.Row(
                    [
                        ft.Column(   
                            [
                                self.table.get_view(),
                                self.button,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            
        
            
            