import flet as ft
from themes import dracula
from database import Database


class Book(ft.Container):
    def __init__(
        self,
        title,
        on_click,
        image=None,
    ):
        super().__init__()
        self.title = title
        self.image_ = image
        self.height = 100
        self.border_radius = 20
        self.bgcolor = dracula.current
        self.on_click = on_click
        self.content = ft.Row(
            [
                ft.Container(
                    ft.Image(
                        src_base64=self.image_ or "",
                        height=80,
                        width=80,
                    ),
                    height=80,
                    width=80,
                    bgcolor=dracula.pink,
                    margin=10,
                    border_radius=10,
                ),
                ft.Text(
                    title,
                    color=dracula.foreground,
                    size=16,
                ),
            ],
        )


class FiltersWidget(ft.Container):
    def __init__(self, on_change):
        super().__init__(bgcolor=dracula.comment)
        self.dd_on_change = on_change
        self.height = 50
        self.size = self.__create_dropdown(
            "Длинна",
            [
                "Любая",
                "Короткая",
                "Средняя",
                "Длинная",
                "Очень длинная",
            ],
        )
        self.genre = self.__create_dropdown(
            "Жанр",
            [
                "Любой",
                "Детектив",
                "Приключения",
                "Ужасы",
                "Фантастика",
                "Юмор",
            ],
        )
        self.end = self.__create_dropdown(
            "Концовка",
            [
                "Любая",
                "Хорошая",
                "Плохая",
            ],
        )
        self.content = ft.Row(
            [
                self.size,
                self.genre,
                self.end,
            ],
        )

    def on_change(self, *_):
        self.dd_on_change(self.size.value, self.genre.value, self.end.value)

    def __create_dropdown(self, title: str, options: list):
        return ft.Dropdown(
            label=title,
            value=options[0],
            options=[
                ft.dropdown.Option(
                    option,
                    text_style=ft.TextStyle(size=12),
                )
                for option in options
            ],
            content_padding=5,
            padding=5,
            expand=True,
            dense=True,
            select_icon_size=1,
            on_change=self.on_change,
        )


class BookInfoWidget(ft.Container):
    def __init__(self, page, book_id: int, db: Database):
        super().__init__()
        self.page = page
        self.bgcolor = dracula.background
        self.expand = True
        self.padding = 20
        book = db.get_book_info(book_id)
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Image(
                            src_base64=book["image"] or "", expand=True
                        ),
                        ft.Column(
                            [
                                ft.Text(book["title"], size=20),
                                ft.Text(book["author"]),
                                ft.Markdown(
                                    "[Яндекс книги]()",
                                    on_tap_link=lambda _: self.page.launch_url(
                                        book["yabook_link"]
                                    ),
                                ),
                                ft.Markdown(
                                    "[Litres]()",
                                    on_tap_link=lambda _: self.page.launch_url(
                                        book["litres_link"]
                                    ),
                                ),
                            ],
                            expand=True,
                        ),
                    ],
                ),
                ft.Row(
                    [
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text(book["description"], expand=True),
                                ]
                            ),
                            margin=ft.margin.only(top=20),
                            bgcolor=dracula.current,
                            border_radius=30,
                            expand=True,
                            padding=20,
                        )
                    ],
                    expand=True,
                ),
            ]
        )


class BooksListWidget(ft.Container):
    def __init__(self, db: Database, page: ft.Page):
        super().__init__()
        self.bgcolor = dracula.background
        self.width = 600
        self.expand = True
        self.db = db
        self.books = ft.Column([], expand=True, scroll=True)
        self.content = self.books

    def add_book(self, book: Book):
        self.books.controls.append(book)

    def set_books_by_ids(self, ids):
        self.books.controls = []
        for id_ in ids:
            book = self.db.get_book_info(id_)
            self.add_book(
                # Book(
                #     title=book["title"],
                #     on_click=lambda *_: self.page.go(f"/book/{id_}"),
                #     image=book["image"],
                # )
                Book(
                    title=book["title"],
                    on_click=lambda *_, id_=id_: self.page.go(f"/book/{id_}"),
                    image=book["image"],
                )
            )
        self.update()

    def on_filters_change(self, size: str, genre: str, end: str):
        size = size.lower() if size.lower() != "любая" else None
        genre = genre.lower() if genre.lower() != "любой" else None
        end = end.lower() if end.lower() != "любая" else None
        book_ids = self.db.get_book_list(size, genre, end)

        self.set_books_by_ids(book_ids)
