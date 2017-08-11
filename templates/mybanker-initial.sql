CREATE TABLE users (name varchar(50) NOT NULL, username varchar(25) NOT NULL, isadmin enum('yes','no') NOT NULL, password varchar(100) NOT NULL, email varchar(50) DEFAULT NULL, created date NOT NULL, PRIMARY KEY (name))
INSERT INTO users VALUES ('MyBanker Admin', 'admin', 'yes','5607df723a0b7e4b36f2d61091e883c7c856196796fdc1ff13800920a24e3f9d','admin@localhost',CURDATE())
CREATE TABLE categories (name VARCHAR(25) NOT NULL, type ENUM('EX','IN'), PRIMARY KEY (name))
INSERT INTO categories VALUES ('WASTE','EX'),('CAR','EX'),('CAR FUEL','EX'),('CLOTHES','EX'),('HOME RENT','EX'),('HOME COUNCILTAX','EX'),('HOME UTIL WATER','EX'),('HOME UTIL GAS','EX'),('HOME UTIL ELECTRICITY','EX'),('HOME INTERNET','EX'),('HOME MISC','EX'),('PHONE','EX'),('JEWELLERIES','EX'),('ELECTRONICS','EX'),('KITCHENWARES','EX'),('HOUSEHOLDS','EX'),('HEALTHCARE','EX'),('GIFTS OUT','EX'),('TOYS','EX'),('FOOD','EX'),('ENTERTAINMENT','EX'),('TRAVEL','EX'),('EDUCATION','EX'),('SALARY','IN'),('BANK INTEREST','IN'),('REFUNDS','IN'),('GIFTS IN','IN'),('SALE','IN')
CREATE TABLE accounts (name varchar(50) NOT NULL, owner varchar(25) NOT NULL, balance decimal(10,2) NOT NULL, description varchar(100) NOT NULL, created date NOT NULL, lastoperated date NOT NULL, excludetotal enum('yes','no') NOT NULL, currency char(3) NOT NULL, type enum('A','L'), PRIMARY KEY (name, owner))
CREATE TABLE transactions (opdate date NOT NULL, description varchar(100) NOT NULL, category varchar(50) NOT NULL, credit decimal(7,2) DEFAULT NULL, debit decimal(7,2) DEFAULT NULL, account varchar(50) NOT NULL, owner varchar(25) NOT NULL)
CREATE TABLE months (name int NOT NULL, PRIMARY KEY(name))
INSERT INTO months VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)
CREATE TABLE messages (id INT UNSIGNED NOT NULL AUTO_INCREMENT, indate date NOT NULL, owner varchar(25) NOT NULL, subject text NOT NULL, message text NOT NULL, fromuser varchar(25) NOT NULL, status enum('N','R') NOT NULL, PRIMARY KEY(id))
CREATE TABLE investmentaccounts (accid int NOT NULL, owner varchar(25) NOT NULL, name varchar(100) NOT NULL, plan varchar(100) NOT NULL, company varchar(50) NOT NULL, email varchar(50) NOT NULL, phone varchar(11) NOT NULL, address varchar(100) NOT NULL, linkedbank varchar(50) NOT NULL, sipstart date NOT NULL, sipend date NOT NULL, invested decimal(10,2) NOT NULL, balanceunits decimal(10,2) NOT NULL, status enum('Active','Closed') NOT NULL, lastoperated date NOT NULL, url varchar(200), urluser varchar(20), urlpass varchar(20), notes varchar(200), PRIMARY KEY (accid))
CREATE TABLE investmenttransactions (accid int NOT NULL, opdate date NOT NULL, sipamount decimal(10,2) NOT NULL, purchasedunits decimal(10,2) NOT NULL, PRIMARY KEY(accid))
