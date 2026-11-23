# Import libraries
import sqlite3

# Constants
DATABASE_PATH = "books.db"
CREATE_TABLE_COMMAND = (
	"CREATE TABLE IF NOT EXISTS books("
	"id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn TEXT)"
)

# Types
type Book = tuple[int, str, str, int, str]


# Run SQL commands
def execute_command(command: str, parameters: tuple[str | int, ...] = ()) -> list[Book]:
	connection = sqlite3.connect(DATABASE_PATH)
	try:
		results = connection.execute(command, parameters).fetchall()
		connection.commit()
		return results
	finally:
		connection.close()


# Create table if missing
def initialize_database() -> None:
	execute_command(CREATE_TABLE_COMMAND)


# Read books
def get_all_books() -> list[Book]:
	return execute_command("SELECT * FROM books")


def search_books(title: str, author: str, year: str, isbn: str) -> list[Book]:
	return execute_command(
		"SELECT * FROM books WHERE title = ? OR author = ? OR year = ? OR isbn = ?",
		(title, author, year, isbn),
	)


# Write books
def add_book(title: str, author: str, year: str, isbn: str) -> None:
	execute_command(
		"INSERT INTO books VALUES (NULL, ?, ?, ?, ?)",
		(title, author, year, isbn),
	)


def update_book(book_id: int, title: str, author: str, year: str, isbn: str) -> None:
	execute_command(
		"UPDATE books SET title = ?, author = ?, year = ?, isbn = ? WHERE id = ?",
		(title, author, year, isbn, book_id),
	)


def delete_book(book_id: int) -> None:
	execute_command("DELETE FROM books WHERE id = ?", (book_id,))
