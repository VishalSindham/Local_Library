from flask import request
import requests
from random import randint

def is_alphabets(s : str):
    """
        This function  first splits the given argument and
        check if all the elements are alphabets or not 
    """
    return ''.join(s.split()).isalpha()

def remove_spaces(s : str):
    """
        This function removes all unnessary spaces from passed argument
    """
    return ' '.join(s.split())

def make_API_call():
    """
        This function makes a call to the API endpoint to fetch 
        books.
    """

    BASE_URL     = 'https://frappe.io/api/method/frappe-library?'

    title        = remove_spaces(request.form['title'])
    authors      = remove_spaces(request.form['author'])
    publisher    = remove_spaces(request.form['publisher'])
    isbn         = request.form['isbn'] 

    end = ''

    if title or authors or isbn or publisher:
        end = f'title={title}&authors={authors}&isbn={isbn}publisher={publisher}'
        response = requests.get(BASE_URL + end).json()['message']
    
    else:
        response = requests.get(BASE_URL + f'page={randint(1,100)}').json()['message']

    return response
    

