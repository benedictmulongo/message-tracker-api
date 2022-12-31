PRAGMA foreign_keys;
PRAGMA foreign_keys = ON;

-- delete from message;
-- delete from user;


delete from message;
delete from user;
delete from  user_messages;


insert into user (fullname, username, email, phone_number)
values
       ('ben mulongo', 'benmulongo', 'mulongo@ben.com', '0765864341'),
       ('nancy', 'nancylove', 'nancy@test.cd', '0765864342');

insert into message (text) values ('I love you my friend');

insert into user_messages
    (sender_id, recipient_id, message_id, is_fetched, send_date)
    VALUES (1,2,1, false, datetime());

delete from message where id=1;
delete from user_messages where message_id=1;

