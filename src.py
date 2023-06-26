# improvements: more robust error checking/type validation throughout
#               better handling of different editions of the same book
#               checkout_book() handling multiple transactions at a time
#               checkout_book() having additional search functionality

from pymongo.mongo_client import MongoClient
import certifi

# verify credentials and connection to db
connected = 0
while not connected:
    # prompt for db username and password
    user = input("Enter database username: ")
    password = input("Enter user's password: ")
    uri = "mongodb+srv://" + user + ":" + password + "@cluster0.5aktca6.mongodb.net/?retryWrites=true&w=majority"

    # create client and connect to the servers
    client = MongoClient(uri, tlsCAFile=certifi.where())

    # send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("You have successfully connected.")
        connected = 1
    except Exception as e:
        print(e)
        print("Unable to connect. Please verify proper credentials and try again.")

# set up variables for accessing db and collection
db = client["library"]
collection = db["books"]

# function to insert a book into the collection
def insert_book():
    title = input("Enter the book title: ")
    author = input("Enter the author's name: ")
    isbn = input("Enter the ISBN-13: ")
    publisher = input("Enter the publisher:")
    quantity = int(input("Enter the number copies to add:"))
    price = input("Enter the price: ")
    exists = collection.find_one({"isbn": isbn})
    if exists:
        collection.update_one({"isbn":isbn}, {"$inc": {"quantity": quantity}})
    else:
        book = {"title": title, "author": author, "isbn": isbn, "publisher": publisher, "price": price, "quantity": quantity}
        collection.insert_one(book)
    print("Book inserted successfully.")

# function to search for a book in the collection
def search_book():
    print("Search Options:")
    print("1. Search by Title")
    print("2. Search by Author")
    print("3. Search by ISBN-13")
    print("4. Return to main menu")

    choice = input("Select an option (1-4): ")
    if choice == "1":
        key = "title"
    elif choice == "2":
        key = "author"
    elif choice == "3":
        key = "isbn"
    elif choice == "4":
        return
    else:
        print("Invalid option. Please try again.")
        return

    value = input(f"Enter the {key}: ")
    query = {key: value}
    book = collection.find_one(query)

    if book:
        print("Book found.")
        print("Title:", book["title"])
        print("Author:", book["author"])
        print("Price:", book["price"])
        print("Quantity:", book["quantity"])
        print("Publisher:", book["publisher"])
        print("ISBN:", book["isbn"])
    else:
        print("Book not found.")

# function to check out a book from the collection
def checkout_book():
    title = input("Enter the book title: ")
    book = collection.find_one({"title": title})
    if book:
        if book["quantity"] > 0:
            print("Price is: ", book["price"])
            will_buy = input("Enter 1 to accept or any other value to reject:")
            if will_buy == "1":
                collection.update_one({"_id": book["_id"]}, {"$set": {"quantity": book["quantity"] - 1}})
            else:
                return
            print("Book checked out successfully.")
        else:
            print("Book is unavailable.")
    else:
        print("Book not found.")

# main loop
while True:
    print("1. Insert a book")
    print("2. Search for a book")
    print("3. Checkout a book")
    print("4. Quit")
    choice = input("Select an option (1-4): ")

    if choice == "1":
        insert_book()
    elif choice == "2":
        search_book()
    elif choice == "3":
        checkout_book()
    elif choice == "4":
        break
    else:
        print("Invalid option. Please try again.")
    print("*********************")