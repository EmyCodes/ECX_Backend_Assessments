#!/usr/bin/python3
"""A simple CRUD API using Flask and SQLAlchemy"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
# from typing import Type
from database_info import username, password, database_name

app = Flask(__name__)

# Database configuration
access_db = f'mysql+pymysql://{username}:{password}@localhost/{database_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = access_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(90), nullable=False)
    author = db.Column(db.Text, nullable=False)


# Create the database
@app.route('/books', methods=['GET', 'POST'])
def get_books():
    """Handles GET and POST requests"""
    if request.method == "GET":
        books = Book.query.all()
        books = [{"id": book.id, "title": book.title,
                  "author": book.author} for book in books]
        return jsonify(books)

    if request.method == "POST":
        book = Book(title=request.json["title"], author=request.json['author'])
        db.session.add(book)
        db.session.commit()
        return jsonify({"message": "Book successfully added!! "})


@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    if request.method == 'GET':
        return jsonify({'id': book.id, 'title': book.title,
                        'author': book.author})
    elif request.method == "PUT":
        data = request.get_json()
        book.title = data["title"]
        book.author = data["author"]
        db.session.commit()
        return jsonify({"message": "Book successfully updated!"})
    elif request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': "Book successfully deleted! "})


if __name__ == '__main__':
    app.run(debug=True)
