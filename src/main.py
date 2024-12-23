import flet as ft
from app_layout import AppLayout
from flet import TemplateRoute
from widgets import Book
from database import Database


class BookChooser:
    def __init__(self, page: ft.Page):
        super().__init__()
        db_path = r"D:\DISTR\Загрузки\iMe Desktop\Library.db"
        self.page = page
        self.db = Database(db_path)
        self.layout = AppLayout(self, page, self.db)
        self.page.add(self.layout)

        self.page.on_route_change = self.route_change
        self.page.update()

        self.page.go("/books/")

    def route_change(self, e):
        troute = TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/preview")
        elif troute.match("/preview"):
            self.layout.set_preview_view()
        elif troute.match("/books"):
            self.layout.set_books_view()
        elif troute.match("/book/:id"):
            self.layout.set_book_info_view(int(troute.id))
        self.page.update()
    


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    app = BookChooser(page)


ft.app(main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0")
