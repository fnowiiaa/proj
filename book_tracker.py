import tkinter as tk
from tkinter import ttk, messagebox
from book_model import BookManager

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Трекер прочитанных книг")
        self.root.geometry("800x500")
        self.root.resizable(True, True)

        self.manager = BookManager()

        # Переменные для фильтров
        self.genre_filter_var = tk.StringVar(value="Все жанры")
        self.pages_filter_var = tk.BooleanVar(value=False)

        # Создание интерфейса
        self.create_input_frame()
        self.create_filter_frame()
        self.create_tree_frame()
        self.create_button_frame()

        # Заполнение таблицы при старте
        self.refresh_table()

    def create_input_frame(self):
        """Фрейм с полями ввода новой книги"""
        input_frame = ttk.LabelFrame(self.root, text="Добавление новой книги", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Название
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        # Автор
        ttk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.author_entry = ttk.Entry(input_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        # Жанр
        ttk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.genre_entry = ttk.Entry(input_frame, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=2)

        # Страницы
        ttk.Label(input_frame, text="Кол-во страниц:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.pages_entry = ttk.Entry(input_frame, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=2)

        # Кнопка добавления
        self.add_btn = ttk.Button(input_frame, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def create_filter_frame(self):
        """Фрейм для фильтрации"""
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        # Фильтр по жанру
        ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.genre_combo = ttk.Combobox(filter_frame, textvariable=self.genre_filter_var, width=27)
        self.genre_combo.grid(row=0, column=1, padx=5, sticky=tk.W)
        self.update_genre_list()  # заполним доступными жанрами

        # Фильтр по страницам
        self.pages_filter_cb = ttk.Checkbutton(filter_frame, text="Больше 200 страниц",
                                                variable=self.pages_filter_var,
                                                command=self.refresh_table)
        self.pages_filter_cb.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        # Кнопка применить фильтр (хотя можно и автоматически, но добавим для наглядности)
        ttk.Button(filter_frame, text="Применить фильтр", command=self.refresh_table).grid(row=2, column=0, columnspan=2, pady=5)

    def create_tree_frame(self):
        """Таблица для отображения списка книг"""
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("title", "author", "genre", "pages"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страницы")
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("genre", width=100)
        self.tree.column("pages", width=80)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_button_frame(self):
        """Кнопка удаления"""
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        self.delete_btn = ttk.Button(btn_frame, text="Удалить выбранную книгу", command=self.delete_book)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

    def update_genre_list(self):
        """Обновляет выпадающий список жанров на основе всех книг"""
        genres = sorted(set(book.genre for book in self.manager.books))
        genres.insert(0, "Все жанры")
        self.genre_combo['values'] = genres
        if self.genre_filter_var.get() not in genres:
            self.genre_filter_var.set("Все жанры")

    def refresh_table(self):
        """Обновляет таблицу, применяя текущие фильтры"""
        # Получаем выбранный фильтр жанра
        genre_filter = self.genre_filter_var.get()
        if genre_filter == "Все жанры":
            genre_filter = None
        # Фильтр по страницам
        pages_filter = ">200" if self.pages_filter_var.get() else None

        filtered_books = self.manager.filter_books(genre_filter, pages_filter)

        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Заполняем отфильтрованными данными
        for book in filtered_books:
            self.tree.insert("", tk.END, values=(book.title, book.author, book.genre, book.pages))

        # Обновляем список жанров для комбобокса
        self.update_genre_list()

    def add_book(self):
        """Обработчик добавления книги"""
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        pages = self.pages_entry.get()

        success, message = self.manager.add_book(title, author, genre, pages)
        if success:
            messagebox.showinfo("Успех", message)
            # Очищаем поля ввода
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.pages_entry.delete(0, tk.END)
            self.refresh_table()
        else:
            messagebox.showerror("Ошибка валидации", message)

    def delete_book(self):
        """Удаляет выбранную книгу из полного списка (не только отфильтрованного)"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для удаления")
            return

        # Определяем, какая книга выбрана (по названию и автору, так как индексы могут не совпадать из-за фильтрации)
        # Удаляем из основного списка менеджера по совпадению полей
        selected_values = self.tree.item(selected[0])['values']
        # Ищем книгу в основном списке (не отфильтрованном) с такими же полями
        for i, book in enumerate(self.manager.books):
            if (book.title == selected_values[0] and book.author == selected_values[1] and
                book.genre == selected_values[2] and book.pages == selected_values[3]):
                self.manager.delete_book(i)
                messagebox.showinfo("Удалено", f"Книга '{book.title}' удалена")
                self.refresh_table()
                return
        messagebox.showerror("Ошибка", "Не удалось найти книгу для удаления")


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()