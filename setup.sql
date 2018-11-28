CREATE USER 'enem2014user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'the.pass';
GRANT ALL PRIVILEGES ON enem_2014 . * TO 'enem2014user'@'localhost';