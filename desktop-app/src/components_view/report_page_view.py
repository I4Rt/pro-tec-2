import flet as ft
from src.widgets.table_values_widget import TableValuesWidget
from time import time
from datetime import datetime

class ReportPageView:
    def __init__(self, id_, name, description, back_function):
        
        self.id_field = ft.Text(str(f'id: {id_}'), width=200)
        self.name_field = ft.TextField(
            value=name, 
            width=700, 
            bgcolor=ft.colors.WHITE24,
        )
        self.description_field=ft.TextField(
            value=description,
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
        
        self.values_table = TableValuesWidget()
        self.values_table.add_col_row(
            str(int(time()*100)),
            start_time=str(datetime.now()),
            end_time=str(datetime.now()),
            deep=int(time()*10000)%100,
            step='бурение',
            comment='comment ' * (int(time()) % 10),
            edit_function = lambda e: e,
            del_function  = lambda e: e
        )
        self.values_table.add_col_row(
            str(int(time()*100) + 1),
            start_time=str(datetime.now()),
            end_time=str(datetime.now()),
            deep=int(time()*10000)%100,
            step='ковыряние',
            comment='comment ' * (int(time()) % 10),
            edit_function = lambda e: e,
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
                        self.values_table.get_view()
                        
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )