# import flet as ft
from database import Database

db = Database(r"D:\DISTR\Загрузки\iMe Desktop\Library.db")

image123 = db.get_book_info(0)["image"]


# def main(page: ft.Page):
#     for i in range(20):
#         if i % 5 == 0:
#             c = ft.Row()
#             page.add(c)
#         image = db.get_book_info(i)["image"]
#         c.controls.append(ft.Image(src_base64=image, width=80, height=))
#     page.update()

# ft.app(main)
