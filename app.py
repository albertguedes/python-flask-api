from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db_name = 'library.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Melhor definir como False em produção

db.init_app(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f'<User {self.username} by {self.email}>'

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

@app.route("/")
def index():
    return jsonify({"success": True, "message": "server on"}), 200

@app.route("/books")
def list_books():
    books = Book.query.all()
    return jsonify({
        "success": True, 
        "message": "books found", 
        "data": [
            {
                "id": b.id, 
                "title": b.title, 
                "author": b.author
            } for b in books
        ],
        "total": len(books)
    }), 200

@app.route("/book/create", methods=["POST"])
def create_book():
    title = request.json.get("title")
    author = request.json.get("author")
    if not title or not author:
        return jsonify({"success": False, "message": "missing title or author"}), 400
    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()
    return jsonify({
        "success": True, 
        "message": "book created"
    }), 201

@app.route("/book/<int:book_id>")
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"success": False, "message": "book not found"}), 404
    return jsonify({
        "success": True, 
        "message": "book found", 
        "id": book.id, 
        "title": book.title, 
        "author": book.author
    }), 200

@app.route("/book/<int:book_id>", methods=["PUT"])
def edit_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"success": False, "message": "book not found"}), 404
    title = request.json.get("title")
    author = request.json.get("author")
    if title:
        book.title = title
    if author:
        book.author = author
    db.session.commit()
    return jsonify({"success": True, "message": "book edited"}), 200

@app.route("/book/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"success": False, "message": "book not found"}), 404
    
    db.session.delete(book)  # Correção aqui
    db.session.commit()  # Commit da sessão após a exclusão
    return jsonify({"success": True, "message": "book deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)

