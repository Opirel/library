from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from icecream import ic
from flask_restful import Api, Resource, reqparse
import os

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# app start
app = Flask(__name__)
CORS(app)
api = Api(app)

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
    LoanDate= db.Column(db.Integer, nullable=False)
    ReturnDate= db.Column(db.Integer, nullable=False)


# Ensure this is run after defining the Book class
with app.app_context():
    db.create_all()  # Create tables if they don't exist


# Book Resource
class BookResource(Resource):
    def get(self):
        books = Book.query.all()
        book_list = [{"BookID": book.BookID, "BookName": book.BookName, "Author": book.Author, "YearPublished": book.YearPublished, "Type": book.Type} for book in books]
        return book_list

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('BookName', required=True, help="BookName cannot be blank!")
        parser.add_argument('Author')
        parser.add_argument('YearPublished', type=int)
        parser.add_argument('Type', type=int)
        args = parser.parse_args()

        try:
            new_book = Book(
                BookName=args['BookName'],
                Author=args['Author'],
                YearPublished=args['YearPublished'],
                Type=args['Type']
            )
            db.session.add(new_book)
            db.session.commit()
            return {"message": "Book added successfully"}, 201
        except Exception as e:
            ic(e)
            abort(400, description="Error while adding the book")

class CustomerResource(Resource):
    def get(self):
        customers = Customer.query.all()
        customer_list = [{"CustomerID": customer.CustomerID, "CustomerName": customer.CustomerName, "City": customer.City, "Age": customer.Age} for customer in customers]
        return customer_list

    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('CustomerName', required=True, help="CustomerName cannot be blank!")
        parser.add_argument('City', required=True)
        parser.add_argument('Age', type=int, required=True)
        args = parser.parse_args()

   
        new_customer = Customer(
            CustomerName=args['CustomerName'],
            City=args['City'],
            Age=args['Age']
        )
        db.session.add(new_customer)
        db.session.commit()
        

# Route to get all books
@app.route('/get_books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [{"BookID": book.BookID, "BookName": book.BookName, 
                "Author": book.Author, "YearPublished": book.YearPublished,
                "Type": book.Type} for book in books]
    return jsonify(book_list)


@app.route('/customers', methods=['POST','GET'])
def add_customer():
    data = request.get_json()
    try:
        new_customer = Customer(
            CustomerName=data['CustomerName'],
            City=data['City'],
            Age=data['Age']
        )
        db.session.add(new_customer)
        db.session.commit()
        ic("the customer ${new_customer.CustomerName} was adedd")
        return jsonify({"message": "Customer added successfully"}), 201
    except Exception as e:
        ic(e)
        abort(400, description="Error while adding the Customer")

if __name__ == '__main__':
    app.run(debug=True)

