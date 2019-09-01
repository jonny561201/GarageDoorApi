INSERT INTO user_information (first_name, last_name, email) VALUES
('Jon', 'Tester', 'fake1234@gmail.com');

INSERT INTO user_login (user_name, password, user_id, role_id) VALUES
('Jonny561201', 'password', (SELECT ID FROM user_information WHERE first_name = 'Jon'), (SELECT ID FROM user_roles WHERE role_name = 'garage_door')),
('l33t', 'password1', (SELECT ID FROM user_information WHERE first_name = 'Jon'), (SELECT ID FROM user_roles WHERE role_name = 'security')),
('dingDongFoo', 'obviouslyPassword1', (SELECT ID FROM user_information WHERE first_name = 'Jon'), (SELECT ID FROM user_roles WHERE role_name = 'sump_pump'));

INSERT INTO user_preferences (is_fahrenheit, user_id) VALUES (TRUE, (SELECT ID FROM user_information WHERE last_name = 'Tester'));