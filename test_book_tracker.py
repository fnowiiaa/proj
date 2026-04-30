import unittest
import os
import json
from book_model import Book, BookManager

class TestBookModel(unittest.TestCase):
    def test_validation(self):
        self.assertTrue(Book.validate_title("Война и мир"))
        self.assertFalse(Book.validate_title(""))
        self.assertTrue(Book.validate_pages("300"))
        self.assertFalse(Book.validate_pages("abc"))
        self.assertFalse(Book.validate_pages("-5"))

    def test_book_creation(self):
        b = Book("1984", "Оруэлл", "Антиутопия", 328)
        self.assertEqual(b.title, "1984")
        self.assertEqual(b.pages, 328)

class TestBookManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_books.json"
        self.manager = BookManager(filename=self.test_file)
        self.manager.books = []
        self.manager.save_books()

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_valid_book(self):
        success, msg = self.manager.add_book("Моби Дик", "Мелвилл", "Приключения", "600")
        self.assertTrue(success)
        self.assertEqual(len(self.manager.books), 1)

    def test_add_invalid_book(self):
        success, msg = self.manager.add_book("", "Автор", "Роман", "100")
        self.assertFalse(success)
        self.assertEqual(len(self.manager.books), 0)

    def test_filter_by_genre(self):
        self.manager.add_book("Книга1", "Автор1", "Фантастика", "300")
        self.manager.add_book("Книга2", "Автор2", "Детектив", "250")
        filtered = self.manager.filter_books(genre_filter="Фантастика")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "Книга1")

    def test_filter_by_pages(self):
        self.manager.add_book("Малая", "А", "Поэзия", "150")
        self.manager.add_book("Большая", "Б", "Роман", "350")
        filtered = self.manager.filter_books(pages_filter=">200")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "Большая")

    def test_save_and_load(self):
        self.manager.add_book("Сохранённая", "Писатель", "Жанр", "123")
        new_manager = BookManager(filename=self.test_file)
        self.assertEqual(len(new_manager.books), 1)
        self.assertEqual(new_manager.books[0].title, "Сохранённая")

    def test_corrupted_json(self):
        with open(self.test_file, "w") as f:
            f.write("{невалидный json}")
        manager = BookManager(filename=self.test_file)
        self.assertEqual(manager.books, [])  # Должен быть пустой список

if __name__ == "__main__":
    unittest.main()