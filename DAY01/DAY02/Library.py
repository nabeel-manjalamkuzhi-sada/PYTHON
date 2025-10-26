# Library Book Management System

def view_books():
    print("Function: View all books in the library.\n")
    if not library:
        print("No books in the library.\n")
    else:
        for title, details in library.items():
            print(f"Title: {title}")
            print(f"Author: {details['author']}")
            print(f"Copies Available: {details['copies']}\n")
            input()  # Wait for Enter to continue
    print("\n")


def add_book():
    try:
        title = input("Enter the book title: ")
        author = input("Enter the author's name: ")
        copies = int(input("Enter the number of copies: "))

        if copies < 0:
            print("Error: Number of copies cannot be negative.")
        else:
            if title in library:
                library[title]['copies'] += copies
                print("Book already exists. Copies updated.")
            else:
                library[title] = {"author": author, "copies": copies}
                print("Book added successfully.")
        input()
    except ValueError:
        print("Error: Please enter a valid integer for copies.")
        input()


def borrow_book():
    print("Function: Borrow a book.\n")
    title = input("Enter the title of the book to borrow: ")

    if title in library:
        if library[title]['copies'] > 0:
            library[title]['copies'] -= 1
            print("Book borrowed successfully.")
        else:
            print("Sorry, the book is currently out of stock.")
    else:
        print("Book not found in the library.")
    input()


def return_book():
    print("Function: Return a book.\n")
    title = input("Enter the title of the book to return: ")

    if title in library:
        library[title]['copies'] += 1
        print("Book returned successfully.")
    else:
        print("This book is not recognized in the system.")
    input()


def remove_book():
    print("Function: Remove a book from the library.\n")
    title = input("Enter the title of the book to remove: ")

    if title in library:
        del library[title]
        print("Book removed successfully.")
    else:
        print("Book not found.")
    input()


# Initialize library dictionary
library = {}

# Menu
flag = 0
while flag == 0:
    try:
        print("\n==== Library Book Management System ====")
        print("1. View All Books")
        print("2. Add New Book")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Remove Book")
        print("6. Exit")
        print("=======================================\n")

        choice = int(input("Enter option number: "))
        print("\n")

        if choice == 1:
            view_books()
        elif choice == 2:
            add_book()
        elif choice == 3:
            borrow_book()
        elif choice == 4:
            return_book()
        elif choice == 5:
            remove_book()
        elif choice == 6:
            flag = 1
        else:
            print("Invalid choice. Please choose a valid option.\n")
    except ValueError:
        print("Error: Please enter a valid number.\n")

print("Program has ended.")
