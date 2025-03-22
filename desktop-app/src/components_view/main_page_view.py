import flet as ft

class MainPage:
    def __init__(self):
        self.text_field = ft.TextField(label="Введите текст")
        self.button = ft.ElevatedButton(
            text="Нажми меня",
            icon=ft.icons.CHECK
        )

    def get_view(self):
        """Возвращает готовый UI."""
        return ft.Column(
            [
                self.text_field,
                self.button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )