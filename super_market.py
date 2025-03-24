import mysql.connector
import requests

# Database setup for MySQL
def create_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL host
            user="root",       # Replace with your MySQL username
            password="12345",  # Replace with your MySQL password
            database="store_db"  # Replace with your database name
        )
        cursor = conn.cursor()

        # Create items table
        cursor.execute('''CREATE TABLE IF NOT EXISTS items
                         (id INT AUTO_INCREMENT PRIMARY KEY,
                          name VARCHAR(255) NOT NULL,
                          price FLOAT NOT NULL,
                          quantity INT NOT NULL)''')

        # Create transactions table
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                         (id INT AUTO_INCREMENT PRIMARY KEY,
                          item_id INT NOT NULL,
                          quantity INT NOT NULL,
                          total_amount FLOAT NOT NULL,
                          gst_amount FLOAT NOT NULL,
                          FOREIGN KEY (item_id) REFERENCES items(id))''')

        conn.commit()
        conn.close()
        print("Database and tables created successfully!")
    except Exception as e:
        print(f"Error creating database or tables: {e}")

# API to fetch GST rate (mock API for demonstration)
def fetch_gst_rate():
    try:
        response = requests.get('https://api.example.com/gst-rate')  # Replace with actual API endpoint
        if response.status_code == 200:
            return response.json()['gst_rate']
        else:
            return 18  # Default GST rate if API fails
    except Exception as e:
        print(f"Error fetching GST rate: {e}")
        return 18  # Default GST rate if API fails

# Add item to the database
def add_item():
    try:
        item_name = input("Enter Item Name: ")
        item_price = float(input("Enter Item Price: "))
        item_quant = int(input("Enter Total Quantity: "))

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",  # Use the correct password
            database="store_db"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, price, quantity) VALUES (%s, %s, %s)",
                       (item_name, item_price, item_quant))
        conn.commit()
        conn.close()

        print("\nItem Added Successfully!\n")
    except ValueError:
        print("\nInvalid input! Please enter numeric values for price and quantity.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")

# Generate bill with GST
def generate_bill():
    try:
        user_item = input("Enter Selling Item: ")
        user_quant = int(input("Enter Quantity: "))

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",  # Use the correct password
            database="store_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE name=%s", (user_item,))
        item = cursor.fetchone()

        if item and user_quant <= item[3]:
            item_id, item_name, item_price, item_quant_db = item
            gst_rate = fetch_gst_rate()
            total_amount = item_price * user_quant
            gst_amount = (total_amount * gst_rate) / 100
            total_amount_with_gst = total_amount + gst_amount

            # Update item quantity in the database
            new_quant = item_quant_db - user_quant
            cursor.execute("UPDATE items SET quantity=%s WHERE id=%s", (new_quant, item_id))

            # Insert transaction into the database
            cursor.execute("INSERT INTO transactions (item_id, quantity, total_amount, gst_amount) VALUES (%s, %s, %s, %s)",
                           (item_id, user_quant, total_amount_with_gst, gst_amount))

            conn.commit()
            conn.close()

            print("\nBill Generated Successfully!")
            print(f"Item: {item_name}")
            print(f"Quantity: {user_quant}")
            print(f"Total Amount (before GST): {total_amount}")
            print(f"GST ({gst_rate}%): {gst_amount}")
            print(f"Total Amount (after GST): {total_amount_with_gst}\n")
        else:
            conn.close()
            print("\nItem not available or insufficient quantity!\n")
    except ValueError:
        print("\nInvalid input! Please enter a valid quantity.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")

# View all items in the store
def view_items():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",  # Use the correct password
            database="store_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        conn.close()

        if items:
            print("\nItems in Store:")
            for item in items:
                print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Quantity: {item[3]}")
            print()
        else:
            print("\nNo items available in the store.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")

# Update item details
def update_item():
    try:
        item_id = int(input("Enter Item ID to update: "))
        new_price = float(input("Enter New Price: "))
        new_quant = int(input("Enter New Quantity: "))

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",  # Use the correct password
            database="store_db"
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET price=%s, quantity=%s WHERE id=%s",
                       (new_price, new_quant, item_id))
        conn.commit()
        conn.close()

        print("\nItem Updated Successfully!\n")
    except ValueError:
        print("\nInvalid input! Please enter numeric values for price and quantity.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")

# Delete item from the store
def delete_item():
    try:
        item_id = int(input("Enter Item ID to delete: "))

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",  # Use the correct password
            database="store_db"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id=%s", (item_id,))
        conn.commit()
        conn.close()

        print("\nItem Deleted Successfully!\n")
    except ValueError:
        print("\nInvalid input! Please enter a valid item ID.\n")
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")

# View entire database (items and transactions)
def view_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",  # Use the correct password
            database="store_db"
        )
        cursor = conn.cursor()

        # View items table
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        print("\nItems in Store:")
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Quantity: {item[3]}")

        # View transactions table
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        print("\nTransactions:")
        for transaction in transactions:
            print(f"ID: {transaction[0]}, Item ID: {transaction[1]}, Quantity: {transaction[2]}, Total Amount: {transaction[3]}, GST Amount: {transaction[4]}")

        conn.close()
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")

# Main menu
def main():
    create_db()
    while True:
        print("1. Add Items")
        print("2. Generate Bill")
        print("3. View All Items")
        print("4. Update Item")
        print("5. Delete Item")
        print("6. View Database")
        print("7. Exit")
        try:
            choice = int(input("Enter Choice: "))
            print()

            if choice == 1:
                add_item()
            elif choice == 2:
                generate_bill()
            elif choice == 3:
                view_items()
            elif choice == 4:
                update_item()
            elif choice == 5:
                delete_item()
            elif choice == 6:
                view_database()  # Call the new function
            elif choice == 7:
                print("Good Bye!")
                break
            else:
                print("Invalid Input! Please choose a number between 1 and 7.\n")
        except ValueError:
            print("\nInvalid input! Please enter a number.\n")
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

if __name__ == "__main__":
    main()