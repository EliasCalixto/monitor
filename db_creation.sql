CREATE DATABASE main_db;
USE main_db;

CREATE TABLE data_raw (
    id INT PRIMARY KEY,
    DateInfo VARCHAR(50),
    Income float,
    Setup float,
    Home float,
    Savings float,
    Studies float,
    Enjoy float,
    Others float,
    Fixed float,
    Cashout float,
    Cash float
);

INSERT INTO data_raw (id,DateInfo,Income,Setup,Home,Savings,Studies,Enjoy,Others,Fixed,Cashout,Cash)
VALUES
(0,'test',1,2,3,4,5,6,7,8,9,10)
