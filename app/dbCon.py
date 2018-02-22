#!../flask/bin/python
# -*- coding: utf-8 -*-

# from app import app
import datetime
import time
import MySQLdb as mysql

#from flask import request


# Open database connection
db = mysql.connect(user="root", passwd='', db="Library", charset="utf8")
# auto commit change
db.autocommit(True)
# show where typed text is inserted
# prepare a cursor object using cursor() method
c = db.cursor()

db2 = mysql.connect(user="root", passwd='', db="Library", charset="utf8")
db2.autocommit(True)
c2 = db2.cursor()


def search_BOOK(args):
	#ISBN = '0002005018'
	ISBN = args.get('ISBN')
	#title = 'Clara Callan: A Novel'
	title = args.get('title')
	#author = ''
	author = args.get('author')
	
	# search by ISBN and title
	if (None == author or '' == author) and (ISBN != '' and ISBN != None) and (title != '' and title != None):
			# and author == None:
			#substring search  BOOK.Title LIKE '%%%s%%' 
			titles = title.split(' ')
			gen_str = ''
			cnt = 0
			for title_str in titles:
				if 0 == cnt:
					gen_str = "BOOK.Title LIKE '%%%s%%'" % title_str
				else:
					gen_str += " and BOOK.Title LIKE '%%%s%%'" % title_str
				cnt += 1	
			gen_str += " and BOOK.ISBN = '%s'" % ISBN
			#gen_str = "BOOK.ISBN = '%s'" %ISBN
			#sql = "SELECT BOOK.ISBN, BOOK.Title, BOOK_AUTHORS.Author_id, BOOK_COPIES.Branch_id, BOOK_COPIES.No_of_copies from BOOK, BOOK_AUTHORS, BOOK_COPIES where BOOK.Book_id like '%".$Book_id."%' and BOOK.Title like'%".$Title."%' and BOOK_AUTHORS.Book_id=BOOK.Book_id and BOOK_COPIES.Book_id=BOOK.Book_id"
			#gen_str += " and BOOK.Title = '%s'" %title
			sql = "SELECT BOOK.ISBN, BOOK.Title, BOOK.Author_name FROM BOOK WHERE %s \
			 ORDER BY BOOK.ISBN;" % gen_str
			c.execute(sql)
			res = []
			for i in c.fetchall():
				#if have book loans record
				#if no book loans record
				sql = "SELECT B.Branch_id, L.Branch_name, B.No_of_copies, B.No_of_copies-COUNT(BL.ISBN) AS AVA_no \
				FROM BOOK_LOANS AS BL RIGHT JOIN (BOOK_COPIES AS B LEFT JOIN LIBRARY_BRANCH AS L ON L.Branch_id=B.Branch_id) \
				ON (B.Branch_id = BL.Branch_id and B.ISBN = BL.ISBN) \
				WHERE B.ISBN = '%s' GROUP BY B.Branch_id HAVING COUNT(BL.ISBN)>=0;" % i[0]
				c2.execute(sql)
				branch_info = [{'Branch_id':j[0], 'Branch_name':j[1],'No_of_copies':j[2],'No_of_available_copies':j[3]} for j in c2.fetchall()]
				res.append({'ISBN':i[0], 'title':i[1], 'author':i[2], 'branch':branch_info})
			return res
	
	# search by title and author
	if (ISBN == None or ISBN == '') and (title != '' and title != None) and (author != '' and author != None):
			#substring search  BOOK.Title LIKE '%%%s%%' 
		titles = args.get('title').split(' ')
		gen_str = ''
		cnt = 0
		for title_str in titles:
			if 0 == cnt:
				gen_str = "BOOK.Title LIKE '%%%s%%'" % title_str
			else:
				gen_str += " and BOOK.Title LIKE '%%%s%%'" % title_str
			cnt += 1	
		print gen_str
		authors = args.get('author').split(' ')
		gena_str = ''
		cnt = 0
		for author_str in authors:
			if 0 == cnt:
				gena_str = "BOOK.Author_name LIKE '%%%s%%'" % author_str
			else:
				gena_str += " and BOOK.Author_name LIKE '%%%s%%'" % author_str
			cnt += 1
		print gena_str
		sql = "SELECT BOOK.ISBN, BOOK.Title, BOOK.Author_name FROM BOOK WHERE %s " % gen_str
		sql += "and %s ORDER BY BOOK.ISBN;" % gena_str
		c.execute(sql)
		res = []
		for i in c.fetchall():
			#if have book loans record
			#if no book loans record
			sql = "SELECT B.Branch_id, L.Branch_name, B.No_of_copies, B.No_of_copies-COUNT(BL.ISBN) AS AVA_no \
			FROM BOOK_LOANS AS BL RIGHT JOIN (BOOK_COPIES AS B LEFT JOIN LIBRARY_BRANCH AS L ON L.Branch_id=B.Branch_id) \
			ON (B.Branch_id = BL.Branch_id and B.ISBN = BL.ISBN) \
			WHERE B.ISBN = '%s' GROUP BY B.Branch_id HAVING COUNT(BL.ISBN)>=0;" % i[0]
			c2.execute(sql)
			branch_info = [{'Branch_id':j[0], 'Branch_name':j[1],'No_of_copies':j[2],'No_of_available_copies':j[3]} for j in c2.fetchall()]
			res.append({'ISBN':i[0], 'title':i[1], 'author':i[2], 'branch':branch_info})
		return res
		
	#search by ISBN and author
	if (title == None or title == '') and (ISBN != '' and ISBN !=None) and (author != ''and author !=None):
			#substring search  BOOK.author LIKE '%%%s%%' 
		authors = args.get('author').split(' ')
		gena_str = ''
		cnt = 0
		for author_str in authors:
			if 0 == cnt:
				gena_str = "BOOK.Author_name LIKE '%%%s%%'" % author_str
			else:
				gena_str += " and BOOK.Author_name LIKE '%%%s%%'" % author_str
			cnt += 1
		gena_str += " and BOOK.ISBN = '%s'" % ISBN
		print gena_str
		sql = "SELECT BOOK.ISBN, BOOK.Title, BOOK.Author_name FROM BOOK WHERE \
		 %s ORDER BY BOOK.ISBN;" % gena_str
		c.execute(sql)
		res = []
		for i in c.fetchall():
			#if have book loans record
			#if no book loans record
			sql = "SELECT B.Branch_id, L.Branch_name, B.No_of_copies, B.No_of_copies-COUNT(BL.ISBN) AS AVA_no \
			FROM BOOK_LOANS AS BL RIGHT JOIN (BOOK_COPIES AS B LEFT JOIN LIBRARY_BRANCH AS L ON L.Branch_id=B.Branch_id) \
			ON (B.Branch_id = BL.Branch_id and B.ISBN = BL.ISBN) \
			WHERE B.ISBN = '%s' GROUP BY B.Branch_id HAVING COUNT(BL.ISBN)>=0;" % i[0]
			c2.execute(sql)
			branch_info = [{'Branch_id':j[0], 'Branch_name':j[1],'No_of_copies':j[2],'No_of_available_copies':j[3]} for j in c2.fetchall()]
			res.append({'ISBN':i[0], 'title':i[1], 'author':i[2], 'branch':branch_info})
		return res
		
	# search by ISBN, title, author
	if (ISBN != ''and ISBN != None) and (title != '' and title != None) and (author != '' and author != None):
			#substring search  BOOK.Title LIKE '%%%s%%' 
		titles = args.get('title').split(' ')
		gen_str = ''
		cnt = 0
		for title_str in titles:
			if 0 == cnt:
				gen_str = "BOOK.Title LIKE '%%%s%%'" % title_str
			else:
				gen_str += " and BOOK.Title LIKE '%%%s%%'" % title_str
			cnt += 1	
		print gen_str
		authors = args.get('author').split(' ')
		gena_str = ''
		cnt = 0
		for author_str in authors:
			if 0 == cnt:
				gena_str = "BOOK.Author_name LIKE '%%%s%%'" % author_str
			else:
				gena_str += " and BOOK.Author_name LIKE '%%%s%%'" % author_str
			cnt += 1
		gena_str += " and BOOK.ISBN = '%s'" % ISBN
		print gena_str
		sql = "SELECT BOOK.ISBN, BOOK.Title, BOOK.Author_name FROM BOOK WHERE %s " % gen_str
		sql += "and %s ORDER BY BOOK.ISBN;" % gena_str
		c.execute(sql)
		res = []
		for i in c.fetchall():
			#if have book loans record
			#if no book loans record
			sql = "SELECT B.Branch_id, L.Branch_name, B.No_of_copies, B.No_of_copies-COUNT(BL.ISBN) AS AVA_no \
			FROM BOOK_LOANS AS BL RIGHT JOIN (BOOK_COPIES AS B LEFT JOIN LIBRARY_BRANCH AS L ON L.Branch_id=B.Branch_id) \
			ON (B.Branch_id = BL.Branch_id and B.ISBN = BL.ISBN) \
			WHERE B.ISBN = '%s' GROUP BY B.Branch_id HAVING COUNT(BL.ISBN)>=0;" % i[0]
			c2.execute(sql)
			branch_info = [{'Branch_id':j[0], 'Branch_name':j[1],'No_of_copies':j[2],'No_of_available_copies':j[3]} for j in c2.fetchall()]
			res.append({'ISBN':i[0], 'title':i[1], 'author':i[2], 'branch':branch_info})
		return res
			
	# search by ISBN
	#if ('' != ISBN) and (title == None) and (author == None):
	if (ISBN != '' and ISBN != None and title == '' and author == ''):

	# if ISBN or title and author:
		sql = "SELECT BOOK.ISBN, BOOK.Title, BOOK.Author_name FROM BOOK WHERE BOOK.ISBN \
		= '%s' ORDER BY BOOK.ISBN;" % ISBN#args.get('ISBN')
		# execute SQL query using execute() method.h
		c.execute(sql)
		# result
		res = []
		# fetches all the rows in a result set
		for i in c.fetchall():
			#if have book loans record
			#if no book loans record
			sql = "SELECT B.Branch_id, L.Branch_name, B.No_of_copies, B.No_of_copies-COUNT(BL.ISBN) AS AVA_no \
			FROM BOOK_LOANS AS BL RIGHT JOIN (BOOK_COPIES AS B LEFT JOIN LIBRARY_BRANCH AS L ON L.Branch_id=B.Branch_id) \
			ON (B.Branch_id = BL.Branch_id and B.ISBN = BL.ISBN) \
			WHERE B.ISBN = '%s' GROUP BY B.Branch_id HAVING COUNT(BL.ISBN)>=0;" % i[0]
			c2.execute(sql)
			branch_info = [{'Branch_id':j[0], 'Branch_name':j[1],'No_of_copies':j[2],'No_of_available_copies':j[3]} for j in c2.fetchall()]
			res.append({'ISBN':i[0], 'title':i[1], 'author':i[2], 'branch':branch_info})
		return res

	# search by title
	if (title != '' and title != None and ISBN == '' and author == ''):
			#substring search  BOOK.Title LIKE '%%%s%%' 
		titles = args.get('title').split(' ')
		gen_str = ''
		cnt = 0
		for title_str in titles:
			if 0 == cnt:
				gen_str = "BOOK.Title LIKE '%%%s%%'" % title_str
			else:
				gen_str += " and BOOK.Title LIKE '%%%s%%'" % title_str
			cnt += 1	
		sql = "SELECT BOOK.ISBN, BOOK.Title, BOOK.Author_name FROM BOOK WHERE %s \
		 ORDER BY BOOK.ISBN;" % gen_str
		c.execute(sql)
		res = []
		for i in c.fetchall():
			#if have book loans record
			#if no book loans record
			sql = "SELECT B.Branch_id, L.Branch_name, B.No_of_copies, B.No_of_copies-COUNT(BL.ISBN) AS AVA_no \
			FROM BOOK_LOANS AS BL RIGHT JOIN (BOOK_COPIES AS B LEFT JOIN LIBRARY_BRANCH AS L ON L.Branch_id=B.Branch_id) \
			ON (B.Branch_id = BL.Branch_id and B.ISBN = BL.ISBN) \
			WHERE B.ISBN = '%s' GROUP BY B.Branch_id HAVING COUNT(BL.ISBN)>=0;" % i[0]
			c2.execute(sql)
			branch_info = [{'Branch_id':j[0], 'Branch_name':j[1],'No_of_copies':j[2],'No_of_available_copies':j[3]} for j in c2.fetchall()]
			res.append({'ISBN':i[0], 'title':i[1], 'author':i[2], 'branch':branch_info})
		return res

	# search by authors
	if (author != '' and author != None and title == '' and ISBN == ''):
		authors = args.get('author').split(' ')
		gen_str = ''
		cnt = 0
		for author_str in authors:
			if 0 == cnt:
				gen_str = "BOOK.Author_name LIKE '%%%s%%'" % author_str
			else:
				gen_str += " and BOOK.Author_name LIKE '%%%s%%'" % author_str
			cnt += 1
		sql = "SELECT BOOK.ISBN, BOOK.Title, BOOK.Author_name FROM BOOK WHERE %s ORDER BY BOOK.ISBN;" % gen_str
		c.execute(sql)
		res = []
		for i in c.fetchall():
			#if have book loans record
			#if no book loans record
			sql = "SELECT B.Branch_id, L.Branch_name, B.No_of_copies, B.No_of_copies-IFNULL(COUNT(BL.ISBN),0) AS AVA_no \
			FROM BOOK_LOANS AS BL RIGHT JOIN (BOOK_COPIES AS B LEFT JOIN LIBRARY_BRANCH AS L ON L.Branch_id=B.Branch_id) \
			ON (B.Branch_id = BL.Branch_id and B.ISBN = BL.ISBN) \
			WHERE B.ISBN = '%s' GROUP BY B.Branch_id HAVING COUNT(BL.ISBN)>=0;" % i[0]
			c2.execute(sql)
			branch_info = [{'Branch_id':j[0], 'Branch_name':j[1],'No_of_copies':j[2],'No_of_available_copies':j[3]} for j in c2.fetchall()]
			res.append({'ISBN':i[0], 'title':i[1], 'author':i[2], 'branch':branch_info})
		return res
	else:
		# print '\r\nno args\r\n'
		return []
		
		
def check_out_BOOK(args):
	ISBN = args.get('ISBN')
	branch_id = args.get('branch_id')
	card_no = args.get('card_no')

	# error: no args
	if (None == ISBN or None == branch_id or None == card_no):
		retStr = ""
		return retStr,[]

	if ('' != ISBN and '' != branch_id and '' != card_no):
		# valid args: ISBN & branch_id
		sql = "SELECT COUNT(*) FROM BOOK_COPIES WHERE ISBN = '%s' and Branch_id = %d;" % (ISBN, int(branch_id))
		c.execute(sql)
		resTemp = c.fetchone()
		if 0 == int(resTemp[0]):
			retStr = "Error: no data for such ISBN or branch id"
			return retStr,[]

		# valid args: card_no
		#card_no.decode(‘utf-8’)
		#card_no.decode('utf-8').encode('gb2312')
		sql = "SELECT COUNT(*) FROM BORROWER WHERE Card_no = '%s';" % card_no
		c.execute(sql)
		resTemp = c.fetchone()
		if 0 == int(resTemp[0]):
			retStr = "Error: no data for such card no"
			return retStr,[]

		# valid whether borrower have right to borrow more than 3 books
		sql = "SELECT COUNT(*) FROM BOOK_LOANS WHERE Card_no = '%s' and Date_in is NULL;" % card_no
		c.execute(sql)
		resTemp = c.fetchone()
		if int(resTemp[0]) >= 3:
			retStr = "Error: cannot borrow more than 3 books"
			return retStr,[]

		# get number of book copies
		sql = "SELECT No_of_copies FROM BOOK_COPIES WHERE ISBN = '%s' and Branch_id = %d;" % (ISBN, int(branch_id))
		c.execute(sql)
		resTemp = c.fetchone()
		Num_book_copies = int(resTemp[0])

		# valid whether there are book to borrow
		sql = "SELECT COUNT(*) FROM BOOK_LOANS WHERE ISBN = '%s' and Branch_id = %d and Date_in is NULL;" % (ISBN, int(branch_id))
		c.execute(sql)
		resTemp = c.fetchone()
		# print "%d,%d \r\n" % (Num_book_copies,int(resTemp[0]))
		# print sql
		if Num_book_copies <= int(resTemp[0]):
			retStr = "Error: no book you can borrow, have been borrowed by other people"
			return retStr,[]

		# get new Loan_id
		sql = "SELECT COUNT(*) FROM BOOK_LOANS;"
		c.execute(sql)
		resTemp = c.fetchone()
		new_Loan_id = int(resTemp[0]) + 1

		# borrow book
		sql = "INSERT INTO `BOOK_LOANS` (`Loan_id`,`ISBN`,`Branch_id`,`Card_no`,`Date_out`,`Due_date`,`Date_in`) VALUES (%d, '%s', %d, '%s', CURDATE(), DATE_ADD(CURDATE(),INTERVAL 14 DAY), NULL);" % (int(new_Loan_id), ISBN, int(branch_id), card_no)
		c.execute(sql)

		res = []
		# print res
		retStr = "Loan ok!"
		return retStr,res

	else:
		print '\r\nwrong args\r\n'
		retStr = "Error: wrong input(input box should not leave blank)"
		return retStr,[]


def check_in_BOOK(args):
	check_in_mode = args.get('check_in_mode')
	search_method = args.get('search')
	ISBN = args.get('ISBN')
	card_no = args.get('card_no')
	borrower = args.get('borrower')

	# no args
	if '' == check_in_mode or None == check_in_mode:
		retStr = ""
		return retStr,[]

	# search book_loan
	if 'search' == check_in_mode:
		# search by card no
		if ('' == ISBN or None == ISBN) and (card_no != '' and card_no != None):
			if(borrower != '' and borrower != None):
				names = borrower.split(' ')
				for name in names:
					sql = "SELECT Loan_id, BL.ISBN, Branch_id, BL.Card_no, Date_out, Due_date, B.Fname, B.Lname FROM BOOK_LOANS AS BL, \
					BORROWER AS B WHERE BL.card_no = '%s' and (B.Fname LIKE '%s' OR B.Lname LIKE '%s') and B.card_no = BL.card_no \
					and Date_in is NULL;" % (card_no,name,name)
					c.execute(sql)
					res = []
					for i in c.fetchall():
						res.append({'loan_id':i[0], 'ISBN':i[1], 'branch_id':i[2], 'card_no':i[3], 'date_out':i[4], 'due_date':i[5], \
						'Fname':i[6], 'Lname':i[7]})

					# print res
					retStr = "results(empty if no check out history):"
					return retStr,res
			if(borrower == '' or borrower == None):
				names = borrower.split(' ')
				for name in names:
					sql = "SELECT Loan_id, BL.ISBN, Branch_id, BL.Card_no, Date_out, Due_date, B.Fname, B.Lname FROM BOOK_LOANS AS BL, \
					BORROWER AS B WHERE BL.card_no = '%s' and B.card_no = BL.card_no \
					and Date_in is NULL;" % (card_no )
					c.execute(sql)
					res = []
					for i in c.fetchall():
						res.append({'loan_id':i[0], 'ISBN':i[1], 'branch_id':i[2], 'card_no':i[3], 'date_out':i[4], 'due_date':i[5], \
						'Fname':i[6], 'Lname':i[7]})

					# print res
					retStr = "results(empty if no check out history):"
					return retStr,res
		# search by book ISBN
		if ('' != ISBN and None != ISBN) and (card_no == '' or card_no == None):
			if(borrower != '' and borrower != None):
				names = borrower.split(' ')
				for name in names:
					sql = "SELECT Loan_id, BL.ISBN, Branch_id, BL.Card_no, Date_out, Due_date, B.Fname, B.Lname FROM BOOK_LOANS AS BL, \
					BORROWER AS B WHERE BL.ISBN = '%s' and (B.Fname LIKE '%s' OR B.Lname LIKE '%s') and B.card_no = BL.card_no \
					and Date_in is NULL;" % (ISBN,name,name)
					c.execute(sql)
					res = []
					for i in c.fetchall():
						res.append({'loan_id':i[0], 'ISBN':i[1], 'branch_id':i[2], 'card_no':i[3], 'date_out':i[4], 'due_date':i[5], \
						'Fname':i[6], 'Lname':i[7]})

					# print res
					retStr = "results(empty if no check out history):"
					return retStr,res
			if(borrower == '' or borrower == None):
				names = borrower.split(' ')
				for name in names:
					sql = "SELECT Loan_id, BL.ISBN, Branch_id, BL.Card_no, Date_out, Due_date, B.Fname, B.Lname FROM BOOK_LOANS AS BL, \
					BORROWER AS B WHERE BL.ISBN = '%s' and B.card_no = BL.card_no \
					and Date_in is NULL;" % (ISBN )
					c.execute(sql)
					res = []
					for i in c.fetchall():
						res.append({'loan_id':i[0], 'ISBN':i[1], 'branch_id':i[2], 'card_no':i[3], 'date_out':i[4], 'due_date':i[5], \
						'Fname':i[6], 'Lname':i[7]})

					# print res
					retStr = "results(empty if no check out history):"
					return retStr,res
		
		# search by book ISBN and card_no
		if ('' != ISBN and None != ISBN) and (card_no != '' and card_no != None):
			if(borrower != '' and borrower != None):
				names = borrower.split(' ')
				for name in names:
					sql = "SELECT Loan_id, BL.ISBN, Branch_id, BL.Card_no, Date_out, Due_date, B.Fname, B.Lname FROM BOOK_LOANS AS BL, \
					BORROWER AS B WHERE BL.ISBN = '%s' and BL.card_no = '%s' and (B.Fname LIKE '%s' OR B.Lname LIKE '%s') and \
					B.card_no = BL.card_no and Date_in is NULL;" % (ISBN,card_no,name,name)
					c.execute(sql)
					res = []
					for i in c.fetchall():
						res.append({'loan_id':i[0], 'ISBN':i[1], 'branch_id':i[2], 'card_no':i[3], 'date_out':i[4], 'due_date':i[5], \
						'Fname':i[6], 'Lname':i[7]})

					# print res
					retStr = "results(empty if no check out history):"
					return retStr,res
			if(borrower == '' or borrower == None):
				names = borrower.split(' ')
				for name in names:
					sql = "SELECT Loan_id, BL.ISBN, Branch_id, BL.Card_no, Date_out, Due_date, B.Fname, B.Lname FROM BOOK_LOANS AS BL, \
					BORROWER AS B WHERE BL.ISBN = '%s' and BL.card_no = '%s' and B.card_no = BL.card_no \
					and Date_in is NULL;" % (ISBN,card_no)
					c.execute(sql)
					res = []
					for i in c.fetchall():
						res.append({'loan_id':i[0], 'ISBN':i[1], 'branch_id':i[2], 'card_no':i[3], 'date_out':i[4], 'due_date':i[5], \
						'Fname':i[6], 'Lname':i[7]})

					# print res
					retStr = "results(empty if no check out history):"
					return retStr,res

	# check in book_loan
	if 'check_in' == check_in_mode:

		if '' == args.get('loan_id') or None == args.get('loan_id'):
			retStr = "Error: please select one!"
			return retStr,[]

		# whether had loan this book
		sql = "SELECT count(*) FROM BOOK_LOANS WHERE Loan_id = %d and Date_in is NULL;" % int(args.get('loan_id'))
		c.execute(sql)
		resTemp = c.fetchone()
		if 0 == int(resTemp[0]):
			retStr = "Error: no book to check in"
			return retStr,[]

		sql = "UPDATE BOOK_LOANS SET Date_in = CURDATE() WHERE Loan_id = %d and Date_in is NULL;" % int(args.get('loan_id'))
		c.execute(sql)
		sql = "UPDATE FINE SET paid_attr = 1 WHERE Loan_id = %d and Est_amt != 0;" % int(args.get('loan_id'))
		c.execute(sql)

		retStr = "check in ok!"
		return retStr,[]

	else:
		# print '\r\nno args\r\n'
		retStr = "Error: wrong input(input box should not leave blank)"
		return retStr,[]


def borrower_mgr(args):
	SSN = args.get('SSN')
	f_name = args.get('fname')
	l_name = args.get('lname')
	address = args.get('address')
	phone = args.get('phone')

	if ((None == SSN or '' == SSN) and (None == f_name or '' == f_name) and (None == l_name \
	or '' == l_name) and (None == address or '' == address) and (None == phone or '' == phone)):
		retStr = ""
		return retStr,[]

	#if this borrower exists
	if ('' != SSN and None != SSN and '' != f_name and None != f_name and '' != l_name and None != l_name and '' != address and None != address \
	and '' != phone and None != phone):
		sql = 'SELECT COUNT(*) FROM BORROWER WHERE SSN = "%s";' % SSN
		c.execute(sql)
		resTemp = c.fetchone()
		if int(resTemp[0]) >= 1:
			retStr = "Error: borrower exists"
			return retStr,[]
		#insert new borrower
		sql = "SELECT COUNT(*) FROM BORROWER"
		c.execute(sql)
		resTemp = c.fetchone()
		new_card_no = 'ID'
		no = str(int(resTemp[0]) + 1)
		new_card_no += "'%s'" % str(no)
		card_no = "ID00" + no
		sql = 'INSERT INTO BORROWER (Card_no, SSN, Fname, Lname, Address, Phone) VALUES ("%s", "%s", "%s", "%s", "%s", "%s");' % (card_no, SSN, f_name, l_name, address, phone)
		c.execute(sql)
		retStr = "Success! Your card no:'%s'" % card_no
		return retStr,[]
	else:
		retStr = "Error: wrong input(SSN, name, address and phone should not be blank)"
		return retStr,[]


def fine(args):
	fine_mode = args.get('fine_mode')
	# no args
	if ('' == fine_mode or None == fine_mode) :
		retStr = ""
		return retStr,[]

	# search fine
	if 'search' == fine_mode:
		card_no = args.get('card_no')

		if (None == card_no or ''== card_no):
			retStr = ""
			return retStr,[]

		#if this card_no exists
		if ('' != card_no and None != card_no):
			sql = 'SELECT BOOK_LOANS.Card_no, SUM(FINE.Est_amt) FROM FINE INNER JOIN \
			BOOK_LOANS ON FINE.Est_amt != 0 and BOOK_LOANS.Card_no = "%s" and \
			FINE.Loan_id = BOOK_LOANS.Loan_id GROUP BY BOOK_LOANS.Card_no;' % card_no
			c.execute(sql)
			res = []
			for i in c.fetchall():
				sql = 'SELECT B.LOAN_ID, B.CARD_NO, B.DATE_OUT, B.DUE_DATE, B.DATE_IN, F.Paid_attr FROM BOOK_LOANS AS B, FINE AS F \
				WHERE  F.LOAN_ID = B.LOAN_ID AND F.EST_AMT !=0 AND B.CARD_NO = "%s";' % i[0]
				c2.execute(sql)
				loan_info = [{'loan_id':j[0],'card_no':j[1],'date_out':j[2],'due_date':j[3],'date_in':j[4],'a_pay': j[5]} for j in c2.fetchall()]
				res.append({'card_no':i[0],'fine':i[1],'loan':loan_info})
			retStr = ""
			return retStr,res
			# sql2 = "SELECT (Card_no, Loan_id, Fine_amt) FROM BOOK_LOANS, FINE WHERE BOOK_LOANS.Loan_id = FINE.Loan_id and Paid_attr = 1 and Card_no = %d and Loan_id = %d and Fine_amt = %f GROUP BY Card_no;" % (Card_no, Loan_id, Fine_amt)
			# c.execute(sql2)
			# resStr2 = c.fetchall()
			# return retStr2,[]

	# pay
	if 'pay' == fine_mode:
		loan_id = args.get('loan_id')

		if (None == loan_id or ''== loan_id):
			retStr = "you need to pay"
			return retStr,[]

		#if this loan_id exists
		sql = 'SELECT B.DATE_IN FROM FINE AS F, BOOK_LOANS AS B WHERE F.LOAN_ID = B.LOAN_ID AND F.loan_id = %d;' % int(loan_id)
		c.execute(sql)
		resTemp = c.fetchall()
		date_in = str(resTemp[0])
		print date_in
		if (date_in =="None" or date_in == None or date_in =="(None,)"):
			retStr = "Not check in yet!"
			return retStr,[]
		else:
			sql = "UPDATE FINE SET Est_amt = 0, Paid_attr = 0 WHERE Loan_id = %d and Paid_attr = 1;" % (int(loan_id))
			c.execute(sql)
			retStr = "Fine is paid!"
			return retStr,[]
	else:
 		retStr = "Error: wrong input(Card_no should not be blank)"
 		return retStr,[]

def update(args):
	# update
	sql = 'INSERT INTO FINE (LOAN_ID) \
	SELECT B.LOAN_ID FROM BOOK_LOANS AS B WHERE ((B.DATE_IN IS NULL AND (B.DUE_DATE < CURDATE())) \
	OR (B.DATE_IN IS NOT NULL AND (B.DUE_DATE < B.DATE_IN))) AND NOT EXISTS (SELECT LOAN_ID FROM FINE)'
	sql = 'UPDATE FINE AS A, BOOK_LOANS AS B \
	SET A.EST_AMT = TIMESTAMPDIFF(DAY,B.DUE_DATE,CURDATE())*0.25 \
	WHERE B.DATE_IN IS NULL AND (B.DUE_DATE < CURDATE()) AND B.LOAN_ID = A.LOAN_ID;'
	c.execute(sql)
	sql = 'UPDATE FINE AS A, BOOK_LOANS AS B \
	SET A.EST_AMT = TIMESTAMPDIFF(DAY,B.DUE_DATE,B.DATE_IN)*0.25 \
	WHERE B.DATE_IN IS NOT NULL AND (B.DUE_DATE < B.DATE_IN) AND Paid_attr = 1 AND B.LOAN_ID = A.LOAN_ID;'
	c.execute(sql)
	sql = 'SELECT LOAN_ID FROM FINE'
	c.execute(sql)
	res = []
	for i in c.fetchall():
		sql = 'SELECT F.LOAN_ID, B.CARD_NO, F.EST_AMT, F.PAID_ATTR FROM FINE AS F, BOOK_LOANS AS B \
		WHERE F.LOAN_ID = %d AND F.LOAN_ID = B.LOAN_ID' % (int(i[0]))
		c2.execute(sql)
		for j in c2.fetchall():
			res.append({'loan_id':j[0],'card_no':j[1],'fine_amt':j[2],'paid_attr':j[3]})
	retStr = ""
	return retStr,res

#search_BOOK(request.args)
# if __name__ == '__main__':
# 	print search_BOOK()