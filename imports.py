import csv 
import psycopg2
import datetime
import os 

con = psycopg2.connect("dbname='dbd64qsfoslgk9' user='tajkczbpbvimtl' host='ec2-34-250-16-127.eu-west-1.compute.amazonaws.com' password='45cc6a4159ff2a7e4b5af48cc85220202e243d1e8a62431c2d63aa6d6efe733a'")
cur = con.cursor()

cur.execute(
    """ CREATE TABLE books ( 
    id SERIAL NOT NULL, 
    isbn varchar(100) NOT NULL, 
    title varchar (100) NOT NULL, 
    author varchar(100) NOT NULL, 
    year integer NOT NULL, 
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (isbn) )  """)

print('books created!')

cur.execute(
    """ CREATE TABLE users (
    name varchar(100) NOT NULL, 
    email varchar(100) NOT NULL, 
    password varchar(100) NOT NULL, 
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (email));  """)

print('users created!')

cur.execute(
    """ CREATE TABLE reviews (
    email varchar(100) NOT NULL, 
    rating integer NOT NULL, 
    comment varchar(1200) NOT NULL, 
    isbn varchar(100) NOT NULL, 
    date DATE NOT NULL DEFAULT CURRENT_DATE) ;  """)

print('reviews created!')

i = 1 
timeset = None
with open('books.csv','r') as f:
    
    timeset= datetime.datetime.now()
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        i += 1 
        cur.execute(" INSERT INTO public.books (isbn, title, author, year ) VALUES (%s,%s,%s,%s)",row)
        print ( f"{i} books added successfully at {timeset}")

con.commit() 
timeDiff = endtime
print ( f"Action Completed In: {timeDiff} ")
cur.close()
con.close()