# Import Section
from flask import Flask
from flask import current_app as app
from flaskext.mysql import MySQL
from hashlib import sha256
import gc

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL()
mysql.init_app(app)

# Method to load and run all queries from a file
# Run queries one by one and return on first failure
def runQueriesFromFile(queryfile):

  conn = mysql.connect()
  cursor = conn.cursor()

  # Read all queries first
  with open (queryfile, "r") as myFile:
    loadQuery = myFile.readlines()

  # Run query one by one and return on first failure
  for query in loadQuery:
    if query:
      try:
        cursor.execute(query)
        conn.commit()
      except Exception as e:
        return str(e)
  conn.close()
  gc.collect() 
  return "Success"

# Method to validate login credentials entered
def checkLogin(username, password):
  conn = mysql.connect()
  cursor = conn.cursor()
  try:
    cursor.execute('SELECT password FROM users WHERE username = "%s"' % username)
    for row in cursor.fetchall():
      if sha256(password).hexdigest() == row[0]:
        return True
      else:
        return False
  except Exception as e:
    conn.close()
    gc.collect()
    return False
  conn.close()
  gc.collect()

# Get Name from Username
def getNameofUser(username):
  conn = mysql.connect()
  cursor = conn.cursor()
  try:
    cursor.execute('SELECT name FROM users WHERE username = "%s"' % username)
    return cursor.fetchone()[0]
  except Exception as e:
    conn.close()
    gc.collect()
    return False
  conn.close()
  gc.collect()

# Method to add new user
def addUser(name, username, password, email):
  conn = mysql.connect()
  cursor = conn.cursor()
  try:
    query = "INSERT INTO users VALUES('%s', '%s', '%s', '%s', '%s', CURDATE())" % (name, username, 'no', sha256(password).hexdigest(), email)
    cursor.execute(query)
    conn.commit()
  except Exception as e:
    conn.close()
    gc.collect()
    return str(e)
  conn.close()
  gc.collect()
  return "User %s added successfully" % name

# Method to update admin password
def updatePassword(username, currentpassword, newpassword):
  if currentpassword == newpassword:
    return "Funny! Idea here is to change password not set the same password again"
  conn = mysql.connect()
  cursor = conn.cursor()
  currentPW = sha256(currentpassword).hexdigest()
  newPW = sha256(newpassword).hexdigest()
  if checkLogin(username, currentpassword):
    try:
      query = "UPDATE users SET password='%s' WHERE username='%s' AND password='%s'" % (newPW, username, currentPW)
      cursor.execute(query)
      conn.commit()
    except Exception as e:
      conn.close()
      gc.collect()
      return str(e)
    conn.close()
    gc.collect()
    return "Password for %s updated successfully" % username
  else:
    return "Operation failed! Password didn't match"

# List all users and send as dictionary
def listMybankerUsers():
  conn = mysql.connect()
  cursor = conn.cursor()
  userdict = []
  try:
    cursor.execute('SELECT * FROM users')
    userdict = cursor.fetchall()
  except Exception as e:
    conn.close()
    gc.collect()
    return None
  conn.close()
  gc.collect()
  return userdict
    
# Get list of categories
def getCategories():
  conn = mysql.connect()
  cursor = conn.cursor()
  inc_categories = []
  exp_categories = []
  try:
    cursor.execute('SELECT name FROM categories WHERE type="IN"')
    for item in cursor.fetchall():
      inc_categories.append(item[0])
    cursor.execute('SELECT name FROM categories WHERE type="EX"')
    for item in cursor.fetchall():
      exp_categories.append(item[0])
  except:
    conn.close()
    gc.collect()
    return None
  conn.close()
  gc.collect()
  return inc_categories, exp_categories

# Add a new category
def addCategory(name, cat_type):
  conn = mysql.connect()
  cursor = conn.cursor()
  try:
    query = "INSERT INTO categories VALUES('%s', '%s')" % (name.upper(), cat_type)
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) is 0:
      conn.commit()
      returnstring = "New category %s added" % name
    else:
      returnstring = str(data[0])
  except Exception as e:
    conn.close()
    gc.collect()
    return str(e)
  conn.close()
  gc.collect()
  return returnstring

# Check how many accounts a user has got
def checkTotalAccounts(username):
  conn = mysql.connect()
  cursor = conn.cursor()
  try:
    query = "SELECT COUNT(*) FROM accounts WHERE owner = '%s'" % username
    cursor.execute(query)
    accountsTotal = cursor.fetchone()[0]
  except Exception as e:
    conn.close()
    gc.collect()
    return None
  conn.close()
  gc.collect()
  return accountsTotal

# Add a new account
def addAccountDB(accinfo):
  conn = mysql.connect()
  cursor = conn.cursor()
  # Hardcoded to GBP at the moment. Need to revisit
  currency = "GBP"
  try:
    query = "INSERT INTO accounts VALUES('%s','%s',%s,'%s',CURDATE(),CURDATE(),'%s','%s','%s')" % \
             (accinfo['name'], accinfo['owner'], accinfo['balance'], accinfo['notes'], accinfo['exclude'], currency, accinfo['type'])
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) is 0:
      conn.commit()
      returnString = "New account %s added" % accinfo['name']
    else:
      returnString = str(data[0])
  except Exception as e:
    conn.close()
    gc.collect()
    return str(e)
  conn.close()
  gc.collect()
  return returnString

# Get accounts for dashboard table
def getAccounts(username, account="all"):
  conn = mysql.connect()
  cursor = conn.cursor()
  appendquery = ""
  if account != "all":
    appendquery = "AND name = '%s'" % account
  try:
    query = "SELECT name, balance, lastoperated, created, type, description FROM accounts WHERE owner = '%s' %s" % (username, appendquery)
    cursor.execute(query)
    data = cursor.fetchall()
  except Exception as e:
    conn.close()
    gc.collect()
    return None
  conn.close()
  gc.collect()
  return data

# Get account transactions
def getTransactions(username, accountname):
  conn = mysql.connect()
  cursor = conn.cursor()
  try:
    query = "SELECT opdate, description, credit, debit, category \
             FROM transactions \
             WHERE owner = '%s' AND account = '%s' \
             ORDER BY opdate DESC LIMIT 20" \
            % (username, accountname)
    cursor.execute(query)
    data = cursor.fetchall()
  except Exception as e:
    conn.close()
    gc.collect()
    return None
  conn.close()
  gc.collect()
  return data

# Check category type
def getCategoryType(category):
  conn = mysql.connect()
  cursor = conn.cursor()
  try:
    query = "SELECT type FROM categories WHERE name = '%s'" % category
    cursor.execute(query)
    data = cursor.fetchone()
  except Exception as e:
    conn.close()
    gc.collect()
    return None
  conn.close()
  gc.collect()
  return data[0]

# Add transaction
def addTransactionsDB(date, notes, amount, category, account, owner):
  conn = mysql.connect()
  cursor = conn.cursor()
  credit, debit, updatetype = ["NULL", amount, "debit"]
  if getCategoryType(category) == "IN":
    credit, debit, updatetype = [amount, "NULL", "credit"]
  try:
    query = "INSERT INTO transactions VALUES('%s', '%s', '%s', %s, %s, '%s', '%s')" % \
             (date, notes, category, credit, debit, account, owner)
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) is 0:
      conn.commit()
      if updateAccounts(account, owner, amount, updatetype):
        returnString = "Transaction added successfully"
      else:
        returnString = "Failed to update accounts table. But transaction recorded"
    else:
      returnString = str(data[0])
  except Exception as e:
    conn.close()
    gc.collect()
    return str(e)
  conn.close()
  gc.collect()
  return returnString

# Get account Type
def checkAccountType(account, owner):
  conn = mysql.connect()
  cursor = conn.cursor()
  isassetAcc = True
  try:
    query = "SELECT type FROM accounts WHERE name = '%s' AND owner = '%s'" % \
             (account, owner)
    cursor.execute(query)
    data = cursor.fetchone()
  except Exception as e:
    conn.close()
    gc.collect()
    return None
  conn.close()
  gc.collect()
  if data[0] == "L":
    isassetAcc = False
  return isassetAcc

# Update Balance in Accounts table
def updateAccounts(name, owner, amount, updatetype):
  conn = mysql.connect()
  cursor = conn.cursor()
  sign,operator = ["+", "-"]
  isassetAcc = checkAccountType(name, owner)
  if not isassetAcc:
    sign = "-"
  if updatetype == "credit":
    operator = "+"
  try:
    query = "UPDATE accounts \
             SET balance = balance %s %s%s, lastoperated = CURDATE() \
             WHERE name = '%s' AND owner = '%s'" % \
             (operator, sign, amount, name, owner)
    cursor.execute(query)
    conn.commit()
  except Exception as e:
    conn.close()
    gc.collect()
    return False
  conn.close()
  gc.collect()
  return True
