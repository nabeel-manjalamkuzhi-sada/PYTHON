# Advanced Inventory Management System

# Function to view the inventory
def view_inventory():
    print("Function: View Inventory\n")
    if not inventory:
        print("Inventory is empty.\n")
    else:
        for product, details in inventory.items():
            quantity, price = details
            print(f"Product: {product}")
            print(f"Quantity: {quantity}")
            print(f"Price: ₹{price:.2f}\n")
            input()  # Pause for each product
    print()


# Function to add or update a product
def add_product():
    try:
        product = input("Enter product name: ")
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: "))

        if quantity < 0 or price < 0:
            print("Error: Quantity and price must be non-negative.")
        else:
            if product in inventory:
                inventory[product][0] += quantity  # Update quantity
                inventory[product][1] = price      # Update price
                print("Product updated successfully.")
            else:
                inventory[product] = [quantity, price]
                print("Product added successfully.")
    except ValueError:
        print("Error: Please enter valid numeric values.")
    input()


# Function to remove a product
def remove_product():
    product = input("Enter the name of the product to remove: ")
    if product in inventory:
        del inventory[product]
        print("Product removed successfully.")
    else:
        print("Product not found in inventory.")
    input()


# Function to update an existing product
def update_product():
    product = input("Enter the product name to update: ")
    if product in inventory:
        try:
            quantity = int(input("Enter new quantity: "))
            price = float(input("Enter new price: "))
            if quantity < 0 or price < 0:
                print("Error: Quantity and price must be non-negative.")
            else:
                inventory[product] = [quantity, price]
                print("Product updated successfully.")
        except ValueError:
            print("Error: Please enter valid numeric values.")
    else:
        print("Product not found in inventory.")
    input()


# Function to calculate total inventory value
def calculate_total_value():
    print("Function: Calculate Total Inventory Value\n")
    total = 0
    for product, (quantity, price) in inventory.items():
        total += quantity * price
    print(f"Total Inventory Value: ₹{total:.2f}")
    input()


# Main menu loop
inventory = {
    "Laptop": [10, 1200.00],
    "Mouse": [50, 25.50]
}

flag = 0
while flag == 0:
    try:
        print("\n==== Advanced Inventory Management System ====")
        print("1. View Inventory")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Update Product")
        print("5. Calculate Total Value")
        print("6. Exit")
        print("=============================================\n")

        choice = int(input("Enter option number: "))
        print()

        if choice == 1:
            view_inventory()
        elif choice == 2:
            add_product()
        elif choice == 3:
            remove_product()
        elif choice == 4:
            update_product()
        elif choice == 5:
            calculate_total_value()
        elif choice == 6:
            flag = 1
        else:
            print("Invalid choice. Please select a valid option.")
    except ValueError:
        print("Error: Please enter a number.")

print("Program has ended.")
