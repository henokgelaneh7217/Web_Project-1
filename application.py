import psycopg2
from flask import Flask
import requests
import json
from flask import jsonify, flash, redirect, url_for, render_template, request 
from flask import session
from datetime import timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=1)
app.secret_key = 'key1234key5678'

con = psycopg2.connect("dbname='dbd64qsfoslgk9' user='tajkczbpbvimtl' host='ec2-34-250-16-127.eu-west-1.compute.amazonaws.com' password='45cc6a4159ff2a7e4b5af48cc85220202e243d1e8a62431c2d63aa6d6efe733a'")
cur = con.cursor()
 
@app.route('/')
def signin():
    if 'name' in session:
        flash('Already Signed in')
        return redirect(url_for('home'))
    else:
        return render_template('signin.html')

@app.route('/signup')
def signup():
    if 'name' in session:
        flash('Already Signed in')
        return redirect(url_for('home'))
    else:
        return render_template('register.html')

@app.route('/signout')
def signout():
    if 'name' in session:
        session.pop('name', None)
        session.pop('email', None)
        session.pop('password', None)

        flash('Sign Out Sucessful.', 'info')
        return redirect(url_for('signin'))
    else:
        flash('Already Singed out.')
        return  redirect(url_for('signin'))

@app.route('/profile')
def profile():
    if 'email' in session:    
        email = session['email']   
        query = "SELECT * FROM public.users WHERE email=%s"
        cur.execute(query, (email,))
        user_email = cur.fetchall()
        profile = {
            'name': user_email[0][0], 
            'email': session['email'],
            'password': user_email[0][2],
            'date': user_email[0][3]
        }
        return render_template('profile.html', profile=profile)

    else: 
        flash('Sign In first')
        return redirect(url_for('signin'))
        
@app.route('/register' , methods = ['POST','GET'])
def register():
   if request.method == 'POST':
      name = request.form['Name']
      email = request.form['Email']
      password = request.form['Password']
      query = "SELECT * FROM public.users WHERE email=%s"
      cur.execute(query, (email,))
      check = cur.fetchone()
      if check:
         flash('You are already Registered. Please Log In.')
         return redirect(url_for('signin'))
      else :
         cur.execute("INSERT INTO public.users (name, email, password) VALUES (%s,%s,%s)", (name,email,password))
         con.commit()
         session['name'] = name
         session['email'] = email
         session['password'] = password

         flash('Registraion Successful')
         return redirect(url_for('home'))
   else:
      if 'name' in session:
         flash('You are already Registered. Please Log In.')
         return redirect(url_for('home'))
      else:
         return render_template('signin.html')

@app.route('/signin_validation', methods=["POST", "GET"])
def signin_validation():
    if request.method == 'POST':
        email = request.form['Emailin']
        password = request.form['Passwordin']
        query = "SELECT * FROM public.users WHERE email=%s"
        cur.execute(query, (email,))
        check = cur.fetchone()
        if check: 
            list = []
            for i in check:
               list.append(i)

            val_name = list[0]
            val_email = list[1]
            val_pass = list[2]
            val_date = list[3]
            if val_email == email and val_pass == password:
                session.permanent = True
                session['name'] = val_name
                session['password'] = val_pass
                session['email'] = val_email
                session['date'] = val_date
                flash('Welcome '+list[0])
                return redirect(url_for('home'))
            else:
                flash('Email or Password Incorrect.')
                return redirect(url_for('signin'))
        else:
            flash('Please Register first.')
            return redirect(url_for('signin'))
    else:
        flash('Signin failed')
        return redirect(url_for('signin'))


@app.route('/home')
def home():
    if 'email' in session:    
        email = session['email']  

        query = "SELECT * FROM public.users WHERE email=%s"
        cur.execute(query, (email,))
        profile = cur.fetchall()

        query2 = "SELECT * FROM public.reviews WHERE email=%s"
        cur.execute(query2, (email,))
        review = cur.fetchall() 

        userInfo = {
            'name': profile[0][0], 
            'email': session['email'],
            'password': profile[0][2],
            'date': profile[0][3]
        }
        reviewnum = len(review)
        return render_template('home.html', userInfo = userInfo, reviewedbooks = review , reviewCount= reviewnum )

    else: 
        flash('Sign In first')
        return redirect(url_for('signin'))

@app.route('/book', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        title = request.form['byTitle']
        title = title.title()

        author = request.form['byAuthor']
        year = request.form['byYear']
        isbn = request.form['byIsbn']
        list = []
        text = None
        baseUrl = request.base_url
        if title:
            query = "SELECT * FROM books WHERE title=%s"
            cur.execute(query, (title,))
            result = cur.fetchall()
            text = title

        elif author:
            query = "SELECT * FROM books WHERE author=%s"
            cur.execute(query, (author,))
            result = cur.fetchall()
            text = author

        elif year:
            query = "SELECT * FROM books WHERE year=%s"
            cur.execute(query, (year,))
            result = cur.fetchall()
            text = year

        else:
            query = "SELECT * FROM books WHERE isbn=%s"
            cur.execute(query, (isbn,))
            result = cur.fetchall()
            text = isbn

        if result: 
            for i in result : 
                list.append(i)
            itemsCount = len(list)
            return render_template('search.html', baseUrl = baseUrl,  items = list, msg = "Books Found", text = text , itemsCount = itemsCount)
            
        else:
            return render_template('search.html', msgNo = "Sorry! No books found" , text = text)
    return render_template ('search.html')


@app.route('/book/<string:isbn>', methods = ['GET', 'POST'])
def singleBook(isbn):
    isbn = isbn
    email = session['email']
    apiCall = None
    apidata = None
    baseUrl = request.base_url

    query = "SELECT * FROM books WHERE isbn=%s"
    cur.execute(query, (isbn,))
    dbdata = cur.fetchall()

    query2 = "SELECT * FROM reviews WHERE isbn=%s"
    cur.execute(query2, (isbn,))
    dbreviews = cur.fetchall()

    query3 = "SELECT * FROM public.reviews WHERE isbn=%s AND email=%s"
    cur.execute(query3, (isbn,email,))
    alreadyHasReview = cur.fetchall()

    apiCall = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "", "isbns": isbn })
    apidata = apiCall.json()

    if request.method == 'POST':
        if alreadyHasReview: 
            flash("There's another review on record")
        else : 
            rating = int(request.form['rating'])
            comment = request.form['comment']
            email = session['email']
            fisbn = request.form['isbn']
            cur.execute("INSERT into public.reviews (email, rating, comment, isbn) Values (%s,%s,%s,%s)", (email, rating,comment,fisbn))
            con.commit()
            flash('Review Submitted!')
    
    if apiCall:
        return render_template('singlebook.html', apidata = apidata, dbdata = dbdata, dbreviews = dbreviews, isbn = isbn, baseUrl = baseUrl)
    else:
        flash('Could not fetch data.')
        return render_template('singlebook.html', dbdata = dbdata, dbreviews = dbreviews, isbn = isbn, baseUrl = baseUrl)
@app.route("/book/<string:isbn>/api")
def apicall(isbn):
    query = "SELECT * FROM public.books WHERE isbn=%s"
    cur.execute(query, (isbn,))
    bookdata = cur.fetchone()
    if bookdata:
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "", "isbns": isbn})
        average_rating=res.json()['books'][0]['average_rating']
        work_ratings_count=res.json()['books'][0]['work_ratings_count']
        x = {
            "title": bookdata[2],
            "author": bookdata[3],
            "year": bookdata[4],
            "isbn": isbn,
            "review_count": work_ratings_count,
            "average_rating": average_rating
        }
        return  jsonify(x)
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug =True)