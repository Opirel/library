from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from icecream import ic
import os

# app start
app = Flask(__name__)

# database configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'  # Use SQLite database named 'library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create the book table
class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BookName = db.Column(db.String(100), nullable=False)
    Author = db.Column(db.String(100))
    YearPublished= db.Column(db.Integer)
    Type = db.Column(db.Integer)

# create the customer table
class Customer(db.Model):
    CustomerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerName = db.Column(db.String(40), nullable=False)
    City= db.Column(db.String(25), nullable=False)
    Age= db.Column(db.Integer, nullable=False)

class Loan(db.Model):
    CustomerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BookID = db.Column(db.String(40), nullable=False)
    LoadDate= db.Column(db.Integer, nullable=False)
    ReturnDate= db.Column(db.Integer, nullable=False)


# Ensure this is run after defining the Book class
with app.app_context():
    db.create_all()  # Create tables if they don't exist

# add new book
@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.get_json()
    try:
        new_book = Book(
            BookName=data['BookName'],
            Author=data['Author'],
            YearPublished=data['YearPublished'],
            Type=data['Type']
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book added successfully"}), 201
    except Exception as e:
        ic(e)
        abort(400, description="Error while adding the book")

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [{"BookID": book.BookID, "BookName": book.BookName, "Author": book.Author, "YearPublished": book.YearPublished, "Type": book.Type} for book in books]
    return jsonify(book_list)





if __name__ == '__main__':
    app.run(debug=True)

