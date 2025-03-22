import flet as ft
from src.components.main_app import App
from src.components_view.data_page_view import DataPageView
from src.components_view.report_page_view import ReportPageView
from src.services.data_service import DataService
from time import time

def main(page: ft.Page):
    app = App(
        page,
        DataService()
    )
    app.init()
ft.app(target=main)