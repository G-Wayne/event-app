##SQL FILE TO CREATE TABLES AND VALUES FOR TESTING QUESTIONS 2 AND 3

create database eventdb;
use mydb;

create table user(
    uid varchar(5) not null,
    password varchar(32) not null,
    fname varchar(50),
    lname varchar(50),
    age int,
    primary key(uid)
);

create table event(
	eid varchar(5) not null,
	ename varchar(50) not null,
	descript varchar(100) not null,
    category varchar(100)
    title varchar(50)
    eventstatus varchar (50)
	primary key(eid)
);


INSERT INTO user VALUES 
('REG404',MD5('404'));


