use main_db;

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
(0,'All Time',133.57,0,0,0,0,0,0,0,0,133.57)
