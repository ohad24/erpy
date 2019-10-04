INSERT INTO ref_user_class
             (user_class_name, permission_level)
             VALUES ('root', 99);

INSERT INTO users (user_name, user_class_id, first_name, last_name, passkey, email, phone)
                   VALUES ('erpy', 1, 'erpy', 'erpy', '1234', '1@1.com', '1111');

INSERT INTO ref_hd_ticket_status (ticket_status_text) VALUES ('פתוח'); --1
INSERT INTO ref_hd_ticket_status (ticket_status_text) VALUES ('בהמתנה'); --2
INSERT INTO ref_hd_ticket_status (ticket_status_text) VALUES ('טופל'); --3
INSERT INTO ref_hd_ticket_status (ticket_status_text) VALUES ('מבוטל'); --4


INSERT INTO ref_hd_ticket_note (ticket_note_text) VALUES ('פתיחה'); --1
INSERT INTO ref_hd_ticket_note (ticket_note_text) VALUES ('תיעוד'); --2
INSERT INTO ref_hd_ticket_note (ticket_note_text) VALUES ('סגירה'); --3
INSERT INTO ref_hd_ticket_note (ticket_note_text) VALUES ('לוג'); --4