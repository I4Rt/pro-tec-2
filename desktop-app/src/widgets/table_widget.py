import flet as ft
from datetime import datetime
from src.dto.base_dto import *
class TableWidget:
    WIDTH    = 1000
    HEIGHT   = 500
    
    FC_WIDTH = 500 - 60
    SC_WIDTH = 300 - 30
    TC_WIDTH = 200 
    
    def __init__(self):
        self.__data = {}
        self.__columns=[
            ft.Text("название", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.START, width=self.FC_WIDTH),
            ft.Text("последнее изменение", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, width=self.SC_WIDTH),
            ft.Text("действия", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, width=self.TC_WIDTH),
        ]
        self.__table_columns = ft.Container(
            ft.Row(
                self.__columns,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True
            ),
            width=self.WIDTH,
            bgcolor=ft.Colors.WHITE10,
            border_radius=10,
            padding=20
        )
        
        self.__table_view = ft.Container(
            content=ft.Text('Пока ничего нет', expand=True, text_align=ft.MainAxisAlignment.CENTER),
            padding=20
        )
        
    def __get_new_table_view(self, columns, rows):
        return ft.DataTable(
            width=self.WIDTH,
            columns=columns,
            rows=rows,
            bgcolor=ft.colors.WHITE10,
            border_radius=10,
            show_bottom_border=True,
            # expand=True
        )
    
    def add_col_row(
        self,
        report:PureReportDTO,
        open_function,
        del_function
    ):
        self.__data[report.id_] = (report.name, report.edit_time)
        self._update_table(open_function, del_function)
        
    def _update_table(self, open_function, del_function):
        items = list(self.__data.items())
        rows = []
        first_row = [
            ft.DataColumn(
                ft.Text(
                    str(items[0][1][0]),
                    width=self.FC_WIDTH
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    str(items[0][1][1]),
                    width=self.SC_WIDTH
                ),
            ),
            ft.DataColumn(
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="open",
                            icon=ft.icons.OPEN_IN_FULL,
                            on_click=open_function
                        ), 
                        ft.ElevatedButton(
                            text="del",
                            icon=ft.icons.DELETE,
                            bgcolor=ft.colors.WHITE24,
                            on_click=del_function
                        ), 
                    ],
                    width=self.TC_WIDTH
                ),
            )
        ]
        for pair in items[1:]:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                str(pair[1][0]),
                                width=self.FC_WIDTH
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(pair[1][1]),
                                width=self.SC_WIDTH
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        text="open",
                                        icon=ft.icons.OPEN_IN_FULL,
                                        on_click=open_function
                                    ), 
                                    ft.ElevatedButton(
                                        text="del",
                                        icon=ft.icons.DELETE,
                                        bgcolor=ft.colors.WHITE24,
                                        on_click=del_function
                                    ), 
                                ],
                                width=self.TC_WIDTH
                            ),
                        ),
                    ],
                )
            )
            
        self.__table_view = self.__get_new_table_view(
            first_row,
            rows
        )
    
    def get_view(self):
        return ft.Column(
            controls=[
                self.__table_columns,
                ft.Column(
                        spacing=10,
                        height=self.HEIGHT,
                        width=self.WIDTH,
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            self.__table_view
                            ],
                        expand=False
                    )
                ] 
            )