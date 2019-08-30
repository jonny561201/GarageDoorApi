ALTER TABLE garage_door_users
    ADD COLUMN user_id UUID NOT NULL;

ALTER TABLE garage_door_users
    ADD COLUMN role_id UUID NOT NULL;

ALTER TABLE garage_door_users
    ADD CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES user_information(ID);

ALTER TABLE garage_door_users
    ADD CONSTRAINT roles_fk FOREIGN KEY (role_id) REFERENCES user_roles(ID)