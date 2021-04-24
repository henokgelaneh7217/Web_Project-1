# Project 1: Books
This project is adopted form Harvard's most popular class **CS50** Programming with Python and JavaScript [[1]](#1).

# Objectives

1. Become more comfortable with Python.
2. Gain experience with Flask.
3. Learn to use SQL to interact with databases.

# Submitted By
*Name: Henok Gelaneh
*ID: ATR/7217/10
*Section: IT

# Overview

In this project, you’ll build a book review website. Users will be able to register for your website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. You’ll also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via your website’s API.

# Features

Alright, it’s time to actually build your web application! Here are the requirements:

1. **Registration**
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/signuo.png)
2. **Login**
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/login.png)
3. **Profile Page**
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/profile.png)
4. **Book Reader**
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/homepage.png)
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/homepagebookreader.png)
5. **Import**

The following code in our iports.py file lets us import any csv file to our connected database.
```Python
import csv
import os 
with open('books.csv','r') as f:
    
    timeset= datetime.datetime.now()
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        i += 1 
        cur.execute(" INSERT INTO public.books (isbn, title, author, year ) VALUES (%s,%s,%s,%s)",row)
```
6. **Search**
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/searchpage.png)
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/results1.png)
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/results2.png)
7. **Book Page**
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/bookpage.png)
8. **Review Submission**
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/personrev.png)
9. **Goodreads Review Data**
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/apidata.png)
10. **API Access**
![](https://github.com/henokgelaneh7217/Rescources/blob/main/imgs/jsondata.png)

