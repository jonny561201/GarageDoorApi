CREATE TABLE garage_door_users (
    ID serial PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

INSERT INTO garage_door_users (user_name, password) values
('Jonny561201', 'password'),
('l33t', 'password1'),
('dingDongFoo', 'obviouslyPassword1');