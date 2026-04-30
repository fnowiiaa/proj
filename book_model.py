import json
import os

class Book:
    """Модель книги"""
    def __init__(self, title, author, genre, pages):
        self.title = title.strip()
        self.author = author.strip()
        self.genre = genre.strip()
        self.pages = pages

    @staticmethod
    def validate_title(title):
        return bool(title and title.strip())

    @staticmethod
    def validate_author(author):
        return bool(author and author.strip())

    @staticmethod
    def validate_genre(genre):
        return bool(genre and genre.strip())

    @staticmethod
    def validate_pages(pages):
        try:
            p = int(pages)
            return p > 0
        except (ValueError, TypeError):
            return False

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "pages": self.pages
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["genre"], data["pages"])


class BookManager:
    """Управление списком книг, сохранение/загрузка JSON"""
    def __init__(self, filename="books.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        """Загружает книги из JSON-файла. Если файл повреждён, начинает с пустого списка."""
        if not os.path.exists(self.filename):
            self.books = []
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book.from_dict(book) for book in data]
        except (json.JSONDecodeError, KeyError, TypeError):
            # При повреждении файла начинаем с пустого списка
            self.books = []

    def save_books(self):
        """Сохраняет текущий список книг в JSON."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, title, author, genre, pages):
        """Добавляет книгу после валидации. Возвращает (успех, сообщение_об_ошибке)."""
        if not Book.validate_title(title):
            return False, "Название книги не может быть пустым"
        if not Book.validate_author(author):
            return False, "Автор не может быть пустым"
        if not Book.validate_genre(genre):
            return False, "Жанр не может быть пустым"
        if not Book.validate_pages(pages):
            return False, "Количество страниц должно быть положительным целым числом"

        new_book = Book(title, author, genre, int(pages))
        self.books.append(new_book)
        self.save_books()
        return True, "Книга успешно добавлена"

    def delete_book(self, index):
        """Удаляет книгу по индексу в текущем (неотфильтрованном) списке."""
        if 0 <= index < len(self.books):
            removed = self.books.pop(index)
            self.save_books()
            return removed
        raise IndexError("Неверный индекс")

    def filter_books(self, genre_filter=None, pages_filter=None):
        """
        Возвращает список книг, соответствующих фильтрам.
        genre_filter: строка (если задана, фильтруем по равенству с учётом регистра)
        pages_filter: может быть ">200" или None.
        """
        result = self.books
        if genre_filter and genre_filter != "Все жанры":
            result = [b for b in result if b.genre == genre_filter]
        if pages_filter == ">200":
            result = [b for b in result if b.pages > 200]
        return result