from pony import orm

__sizes = {
    0: "small",
    1: "medium",
    2: "large",
    3: "extra large",
}
__genres = {
    0: "детектив",
    1: "приключения",
    2: "ужасы",
    3: "фантастика",
    4: "юмор",
}

__ends = {
    0: "good",
    1: "bed",
}


db_path = r"D:\DISTR\Загрузки\iMe Desktop\Library.db"


# msg = base64.b64decode(img.split(",")[-1])
# buf = io.BytesIO(msg)
# img = Image.open(buf)
# Image.open(buf).show()


class Books:
    name = orm.Required(str)
    image_base64 = orm.Required(str)
    author = orm.Required(str)
    yabook_link = orm.Required(str)
    litres_link = orm.Required(str)
    size = orm.Required(str)
    genre = orm.Required(str)
    ending = orm.Required(str)


class Database:
    def __init__(self, db_path):
        self.db = orm.Database()
        self.Books = type(
            "Books",
            (self.db.Entity,),
            {
                "name": orm.Required(str),
                "image_base64": orm.Required(str),
                "author": orm.Required(str),
                "yabook_link": orm.Required(str),
                "litres_link": orm.Required(str),
                "size": orm.Required(str),
                "genre": orm.Required(str),
                "ending": orm.Required(str),
            },
        )

        self.db.bind(provider="sqlite", filename=db_path)
        self.db.generate_mapping()

    def get_book_info(self, book_id: int):
        with orm.db_session:
            book = self.Books[book_id]
            return {
                "title": book.name,
                "author": book.author,
                # base64 image
                "image": book.image_base64.split(",")[-1],
                "description": "Описание",
                "yabook_link": book.yabook_link,
                "litres_link": book.litres_link,
            }

    def get_book_list(
        self,
        size=None,
        genre=None,
        end=None,
    ) -> list[int]:
        """
        Возвращает список книг по указанным фильтрам

        Args:
            size (int, optional): see __sizes
            genre (int, optional): see __genres
            end (int, optional): see __ends

        Returns:
            list[int]: book_id 's
        """
        with orm.db_session:
            return orm.select(
                b.id
                for b in self.Books
                if (
                    (b.ending == end or (end == None))
                    and (b.genre == genre or (genre == None))
                    and (b.size == size or (size == None))
                )
            ).fetch()


# db_path = r"D:\DISTR\Загрузки\iMe Desktop\Library.db"
# db = Database(db_path)
# print(db.get_book_list(end='плохая'))
