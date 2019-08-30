CREATE TABLE garage_door_users (
    ID UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);