import flet as ft
from src.components_view.main_page_view import MainPage

# Класс для логики приложения
class App:
    def __init__(
        self, 
        root: ft.Page,
        main_view: MainPage
    ):
        self.root = root
        self.root.title = "Мое приложение"
        self.root.theme_mode = ft.ThemeMode.DARK
        self.root.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.root.padding=ft.padding.symmetric(0, 10)

        # Создаем экземпляр верстки
        self.main_page = main_view

    def init(self):
        self.main_page.button.on_click = lambda e: self.show_snackbar(e, self.main_page.text_field.value)
        self.root.add(self.main_page.get_view())
        
    def show_snackbar(
        self, 
        e, 
        message
        ):
        
        theme_ = ft.Theme()
        theme_.visual_density = ft.VisualDensity.COMPACT
        alter_dialog = ft.AlertDialog(
            content= ft.Row(
                controls=[
                    ft.Text(
                        str(message),
                        color=ft.colors.WHITE,
                        text_align=ft.alignment.center,
                    ),
                ],
                alignment = ft.MainAxisAlignment.CENTER
            ),
            actions=[
                ft.TextButton("Ok", on_click = lambda e: self.root.close(alter_dialog)),
            ],
        )
        
        self.root.open(
            alter_dialog
        )
        
        self.root.update()
        
    