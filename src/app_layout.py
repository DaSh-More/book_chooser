import flet as ft
from widgets import BooksListWidget, FiltersWidget, BookInfoWidget, Book
from themes import dracula
from database import Database


class AppLayout(ft.Column):
    def __init__(self, app, page: ft.Page, db: Database, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = db
        self.app = app
        self.page = page
        self.width = 600
        self.expand = True
        self.spacing = 0

        self.controls = []

        books_list_widget = BooksListWidget(self.db, self.page)
        filters_widget = FiltersWidget(books_list_widget.on_filters_change)
        
        self.books_view = [filters_widget, books_list_widget]
        self.preveiw_view = [ft.Text("hello", bgcolor=dracula.pink)]

        # self.set_books_view()

    def set_view(self, view):
        self._active_view = view
        self.controls = self._active_view
        self.update()

    def set_preview_view(self):
        self.set_view(self.preveiw_view)

    def set_books_view(self):
        self.set_view(self.books_view)

    def set_book_info_view(self, book_id):
        self.set_view([BookInfoWidget(self.page, book_id, self.db)])
