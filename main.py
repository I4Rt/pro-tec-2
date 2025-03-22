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
        self.main_page = MainPage()

    def init(self):
        # Настраиваем кнопку
        self.main_page.button.on_click = lambda e: self.show_snackbar(e, self.main_page.text_field.value)
        # Добавляем верстку на страницу
        self.root.add(self.main_page.get_view())
        

    # Функция для отображения SnackBar с замыканием
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
        


# Запуск приложения
def main(page: ft.Page):
    app = App(
        page,
        MainPage()
    )
    app.init()
    

ft.app(target=main)