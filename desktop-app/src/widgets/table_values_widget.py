import flet as ft
from datetime import datetime
from loguru import logger

class TableValuesWidget:
    WIDTH    = 1000
    HEIGHT   = 500
    
    START_TIME_COLUMN_WIDTH = 120
    END_TIME_COLUMN_WIDTH   = 120
    DEEPTH_COLUMN_WIDTH     = 100 
    STEP_COLUMN_WIDTH       = 100
    COMMENT_COLUMN_WIDTH    = 300
    ACTIONS_COLUMN_WIDTH    = 150
    
    def __init__(
        self
    ):
        self.__data = {}
        self.__columns=[
            ft.Text("начало", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, width=self.START_TIME_COLUMN_WIDTH),
            ft.Text("окончание", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, width=self.END_TIME_COLUMN_WIDTH),
            ft.Text("забой", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, width=self.DEEPTH_COLUMN_WIDTH),
            ft.Text("этап", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, width=self.STEP_COLUMN_WIDTH),
            ft.Text("комментарий", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, width=self.COMMENT_COLUMN_WIDTH),
            ft.Text("действия", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, width=self.COMMENT_COLUMN_WIDTH),
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
            column_spacing = 10,
            # expand=True
        )
    
    def add_col_row(
        self,
        id_,
        start_time,
        end_time,
        deep,
        step,
        comment,
        edit_function,
        del_function
    ):
        self.__data[id_] = (
            start_time,
            end_time,
            deep,
            step,
            comment
        )
        # logger.info(self.__data)
        self._update_table(edit_function, del_function)
        
    def _update_table(self, edit_function, del_function):
        items = list(self.__data.items())
        rows = []
        first_row = [
            ft.DataColumn(
                ft.Text(
                    str(items[0][1][0]),
                    width=self.START_TIME_COLUMN_WIDTH
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    str(items[0][1][1]),
                    width=self.END_TIME_COLUMN_WIDTH
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    str(items[0][1][2]),
                    width=self.DEEPTH_COLUMN_WIDTH,
                    text_align=ft.TextAlign.CENTER
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    str(items[0][1][3]),
                    width=self.STEP_COLUMN_WIDTH
                ),
            ),
            ft.DataColumn(
                ft.Text(
                    str(items[0][1][4]),
                    width=self.COMMENT_COLUMN_WIDTH
                ),
            ),
            ft.DataColumn(
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="edit",
                            icon=ft.icons.OPEN_IN_FULL,
                            on_click=edit_function
                        ), 
                        ft.ElevatedButton(
                            text="del",
                            icon=ft.icons.DELETE,
                            bgcolor=ft.colors.WHITE24,
                            on_click=del_function
                        ), 
                    ],
                    width=self.ACTIONS_COLUMN_WIDTH
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
                                width=self.START_TIME_COLUMN_WIDTH
                            ),
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(pair[1][1]),
                                width=self.END_TIME_COLUMN_WIDTH
                            ),
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(pair[1][2]),
                                width=self.DEEPTH_COLUMN_WIDTH,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(pair[1][3]),
                                width=self.STEP_COLUMN_WIDTH
                            ),
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(pair[1][4]),
                                width=self.COMMENT_COLUMN_WIDTH
                            ),
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        text="edit",
                                        icon=ft.icons.OPEN_IN_FULL,
                                        on_click=edit_function
                                    ), 
                                    ft.ElevatedButton(
                                        text="del",
                                        icon=ft.icons.DELETE,
                                        bgcolor=ft.colors.WHITE24,
                                        on_click=del_function
                                    ), 
                                ],
                                width=self.ACTIONS_COLUMN_WIDTH
                            ),
                        )
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