from tracemalloc import start
from app import db
from datetime import datetime
import random

# Table to create Book records 
class Books(db.Model):
    """
        This table is used to keep book records , following information 
        is stored :
        Book ID using book_id column
        Book Name using book_name column
        Book Author using author column
        Book Publisher using publisher column 
        Book Stock available using quantity column
        Borrower to keep track of which books are borrowed
        ISBN column to keep track of book ISBN numbers
    """
    book_id   = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(150))
    author    = db.Column(db.String(75))
    publisher = db.Column(db.String(75))
    quantity  = db.Column(db.Integer, default = 1)
    borrower  = db.Column(db.Integer, default = -1)
    isbn      = db.Column(db.String(15))

## Table to create Members Record
class Members(db.Model):
    """
        This table is used to create members records using following 
        columns respectively 
        member_id to keep track of Member ID
        member_name to keep store Members Name 
        member_balance to keep track Members Balance
        member_borrowed to keep track if the member has borrowed any book 
    """
    member_id        = db.Column(db.Integer, primary_key = True)
    member_name      = db.Column(db.String(150))
    member_balance   = db.Column(db.Float, default = 2000)
    member_borrowed  = db.Column(db.Boolean, default = False)


##  Table to keep track  of transactions 

class Transactions(db.Model):
    """
        This table keeps track of transactions using following 
        columns 
        _id is used for transaction id
        book_name to keep track book borrowed in that transaction
        member_name to keep track who borrowed in that particular transaction
        borrowed_and_not to keep track of transactions 
        time to keep a time stamp of transactions

    """
    _id                         = db.Column(db.Integer, primary_key = True)
    book_name                   = db.Column(db.String(150))
    member_name                 = db.Column(db.String(150))
    borrowed_or_not             = db.Column(db.Boolean, default = False)
    time                        = db.Column(db.DateTime, default = datetime.utcnow)      
