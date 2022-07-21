from flask import  render_template , request, redirect
from flask.helpers import url_for
from app import app , db
from models.models import *
from useful_functions.useful_functions import *


## routes  defined here 


@app.route('/')
def home():
    available_books = Books.query.all()
    return render_template('home.html', books = available_books)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/members', methods = ["POST", "GET"])
def members():
    """
        Using this route we will create a member and add to the members table with balance  , 
        we will fetch the user data from the form and vaildate the data if everthing is correct
        then create a member and record it in DB. After a member is added it will 
        reload the same page show all the members .
        If member is not being added it will show all the present members 
    
    """
    if request.method == "POST" :

        user_name         = request.form['user_name']  # getting user name from the form 
        member_balance    = request.form['balance']  # getting user balance from the form

        if not is_alphabets(user_name):
            """
                This function help to check if filled data is valid or not for user name 
            """
            message = "Please enter a proper name which only contains alphabets"
            return render_template('general_error.html', message = message, page = 'members')
        
        if not member_balance.isnumeric():
            """
                This fuction will help vaild if the balance input is numeric or not 
            """
            message = 'Please enter numbers only'
            return render_template('general_error.html', message = message, page = "members")
        

        try :
            member = Members( member_name = user_name, member_balance = float(member_balance))
            db.session.add(member)
            db.session.commit()
        except :
            """
            Incase any error happens on the db side this will be raised and handle it 
            """
            return render_template('general_error.html', message="It's not you, but us Internal Server error")
    members = Members.query.all()
    return render_template('members.html', members = members)



@app.route('/transactions')
def transactions():
    """
        Route to keep track of transactions 
    """
    transactions = Transactions.query.order_by(Transactions.time.desc()).all()
    return render_template('transactions.html', transactions = transactions)



@app.route('/rent_out/<int:book_id>', methods = ["POST", "GET"])
def rent_out(book_id):

    """
        This route will perform the opertion to renting books 

    """
    all_members = Members.query.filter(
                            Members.member_borrowed == False
                            ).all() # this will fetch all the members who did not borrow any book
    
    if request.method == "POST":

        member_id = request.form['id'] # fetching the member id  from the form

        if not member_id.isnumeric():
                # Checking if id passed is numeric or not 
            return render_template('general_error.html', message = 'Enter a vaild id')
        
        member = Members.query.get(int(member_id)) # fetching the member object 

        # this will check if passed member_id is related to a  member or not 
        if member == None :
            return render_template('general_error.html', message = 'Not A vaild Member....')
        
        if member.member_balance < -500 :
            # checking is member is having enough balance to borrow a book

            message = f'{member.member_name} balance   is not enough to borrow , that is {member.member_balance} \
                That is less than -500  '
            return render_template('general_error.html', message = message)
        
        try :
            
            member.member_borrowed  = True # Set as this member as borrowed a book
            member.member_balance  -= 100

            book = Books.query.get(book_id)
            if book == None :
                return render_template('general_error.html', message = 'Book ID is not valid')
            
            book.quantity  -= 1 # decrease the book quantity 
            book.borrower = member.member_id  # book borrower is set to id of the member 

            transaction = Transactions(
                                book_name           = book.book_name,
                                member_name         = member.member_name,
                                borrowed_or_not     = False
                                )
            db.session.add(transaction)
            db.session.commit()

            return redirect(url_for('home'))
        except :

            return render_template(
                'general_error.html', 
                message = 'Unexcepted error while processing your rent out request'
                )
    return render_template(
                        'rent_out.html',
                        id = book_id,
                        members = all_members
                         )


@app.route('/addBooks', methods = ["POST", "GET"])
def addBooks():
    """
        This route will fetch from a API call using form data if passed 
    """
    if request.method == "POST":

        response  = make_API_call()

        # parse the data 
        for data in response:

            book_id = int(data["bookID"])


            # check if the same data exists in the DB or not 
            
            check_id = Books.query.get(book_id)


            if check_id == None :
                book = Books(
                            book_id    = book_id,
                            book_name  = data['title'],
                            author     = data['authors'],
                            publisher  = data['publisher'],
                            isbn       = data['isbn']
                            )
                db.session.add(book)
                db.session.commit()
            elif check_id :
                print(check_id)
                check_id
                quantity  = request.form["quantity"]
                book = Books.query.get(book_id)
                print(book)
                book.quantity = book.quantity + int(quantity)                
                db.session.commit()
                print('here reached ')

        return redirect(url_for('home'))
    else : 

        return render_template('add_books.html')

@app.route('/addCustomBooks', methods = ["POST" , "GET"])
def add_custom_books():
    if request.method == "POST":
        book_id       = request.form["book_id"]
        book_name     = request.form["book_name"]
        author        = request.form["authors"]
        quantity      = request.form['quantity']
        publisher     = request.form["publisher"]
        isbn          = request.form["isbn"] or 404

        # checking if book_id already exists and is valid or not 
        if not book_id.isnumeric():
            return render_template( 'general_error.html',message = 'Please enter a vaild Book ID')
        
        book_id = int(book_id)
        if Books.query.get(book_id) != None :
            message = 'This book is already present or other book with same id present'
            return render_template('general_error.html',{'message':message})
        
        try:
            print('here in')
            book = Books (
                            book_id      = book_id,
                            book_name    = book_name,
                            author       = author,
                            quantity     = quantity,
                            publisher    = publisher,
                            isbn         = isbn
                            )
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('home'))
            
        except :
            return render_template('general_error.html', message='Something went wrong try again')
    else :
        return render_template('general_error.html', message = 'Not able to update the books')




@app.route('/return_book')
def return_book():
    """
        This route will help return borrowed books
    """
    books  = Books.query.filter(
                            Books.borrower != -1 
                        ).all()
    return render_template('return_book.html', books = books)


@app.route('/summary/<int:id>')
def summary(id):
    """
    This routes will show who borrowed the book when it was returned
    """
    book            = Books.query.get(id) # get the book
    book.quantity   += 1    # reset the quantity of the book 
    member          = Members.query.get(book.borrower)  # get the borrower 
    
    transactions = Transactions(
                                book_name        = book.book_name,
                                member_name      = member.member_name,
                                borrowed_or_not  = True
                                )
    db.session.add(transactions)
    book.borrower = -1


    member.member_borrowed = False # set the member status to not borrowed 
    db.session.commit()
    return render_template('summary.html', member = member)

@app.route('/delete_member/<int:id>')
def delete(id):
    """
        This route deletes the member information
    """

    try :
        delete_member = Members.query.get(id)
        db.session.delete(delete_member)
        db.session.commit()
        return redirect('/')
    except :
        return render_template('general_error.html', message = 'Unknown error')

@app.route('/update/<int:id>', methods = ["POST", "GET"])
def update(id):
    """
        This route will update the members balance
    """
    if request.method == "POST":
        try : 
            user  = Members.query.get(id)
            if request.form["amount"].isnumeric():
                user.member_balance += float(request.form["amount"])
                db.session.commit()
                return redirect(url_for('members'))
        except :
            return render_template('general_error.html',message = "Enter numbers only " )
    else :
        return render_template('update.html', id = id )
