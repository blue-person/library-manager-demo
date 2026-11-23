# Import libraries
import tkinter as tk
from collections.abc import Callable, Sequence
from tkinter import messagebox

# Import packages
import database

# Constants
FIELD_NAMES = ("Title", "Author", "Year", "ISBN")
BUTTON_WIDTH = 12

# Shared state
selected_book_id: int
field_vars: list[tk.StringVar] = []


# Dialogs
def show_info(text: str) -> None:
	messagebox.showinfo("Information", text)


def ask_confirmation(text: str) -> bool:
	return messagebox.askquestion("Confirmation", text) == "yes"


# Form and list helpers
def get_fields() -> tuple[str, ...]:
	return tuple(var.get() for var in field_vars)


def fill_fields(values: Sequence[str | int]) -> None:
	for var, value in zip(field_vars, values, strict=True):
		var.set(str(value))


def fill_list(books: list[database.Book]) -> None:
	book_list.delete(0, tk.END)
	for book in books:
		book_list.insert(tk.END, book)  # pyright: ignore[reportArgumentType]


def show_all_books() -> None:
	fill_list(database.get_all_books())


def clear_window() -> None:
	fill_fields(("",) * len(FIELD_NAMES))
	show_all_books()


def run_action(
	action: Callable[[], None], success_message: str, error_message: str
) -> None:
	try:
		action()
		clear_window()
		show_info(success_message)
	except:
		show_info(error_message)


# Event handlers
def on_book_selected(event: tk.Event) -> None:
	global selected_book_id
	try:
		selected_book_id, *values = book_list.get(book_list.curselection()[0])
		fill_fields(values)
	except IndexError:
		pass


def search_books() -> None:
	fill_list(database.search_books(*get_fields()))


def add_book() -> None:
	title = field_vars[0].get()
	run_action(
		lambda: database.add_book(*get_fields()),
		f"{title} was added successfully",
		f"An error occurred while adding {title} to the database",
	)


def update_book() -> None:
	title = field_vars[0].get()
	run_action(
		lambda: database.update_book(selected_book_id, *get_fields()),
		f"{title} was updated successfully",
		f"An error occurred while updating {title} in the database",
	)


def delete_book() -> None:
	title = field_vars[0].get()
	if ask_confirmation(
		f"{title} will be deleted from the database. Do you want to continue?"
	):
		run_action(
			lambda: database.delete_book(selected_book_id),
			f"{title} was deleted successfully",
			f"An error occurred while deleting {title} from the database",
		)


def close_program() -> None:
	if ask_confirmation("Are you sure you want to exit?"):
		root.destroy()


# Main window
root = tk.Tk()
root.title("Book Manager")
root.resizable(False, False)

# Form fields in a two-column grid
for index, name in enumerate(FIELD_NAMES):
	row, column = divmod(index, 2)
	var = tk.StringVar()
	field_vars.append(var)
	tk.Label(root, text=name).grid(row=row, column=column * 2)
	tk.Entry(root, textvariable=var).grid(row=row, column=column * 2 + 1)

# Book list with scrollbar
book_list = tk.Listbox(root, height=8, width=25)
book_list.grid(row=2, column=0, rowspan=6, columnspan=2)
book_list.bind("<<ListboxSelect>>", on_book_selected)

scrollbar = tk.Scrollbar(root, command=book_list.yview)
scrollbar.grid(row=2, column=2, rowspan=6)
book_list.configure(yscrollcommand=scrollbar.set)

# Buttons
BUTTONS = (
	("View all", show_all_books),
	("Search", search_books),
	("Add", add_book),
	("Update", update_book),
	("Delete", delete_book),
	("Close", close_program),
)
for row, (text, command) in enumerate(BUTTONS, start=2):
	tk.Button(root, text=text, width=BUTTON_WIDTH, command=command).grid(
		row=row, column=3
	)


# Start application
def run() -> None:
	database.initialize_database()
	root.mainloop()
