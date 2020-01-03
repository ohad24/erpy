INSERT INTO params (p_name, p_val) VALUES ('PASS_SALT', :salt);
--INSERT INTO params (p_name, p_val) VALUES ('PASS_SALT', 'Bpstmjz3E92gVHj5ZPOL0w');

INSERT INTO ref_user_class (user_class_name, permission_level) VALUES ('root', 99); --1
INSERT INTO ref_user_class (user_class_name, permission_level) VALUES ('מנהל', 50); --2
INSERT INTO ref_user_class (user_class_name, permission_level) VALUES ('תפעול', 40); --3
INSERT INTO ref_user_class (user_class_name, permission_level) VALUES ('משתמש', 10); --4

INSERT INTO teams (team_name, description) VALUES ('IT', NULL); --1
INSERT INTO teams (team_name, description) VALUES ('מכירות', NULL); --2

INSERT INTO ref_hd_ticket_status (ticket_status_name) VALUES ('פתוח'); --1
INSERT INTO ref_hd_ticket_status (ticket_status_name) VALUES ('בהמתנה'); --2
INSERT INTO ref_hd_ticket_status (ticket_status_name) VALUES ('סגור'); --3


INSERT INTO ref_hd_ticket_close_reason (ticket_close_reason_name) VALUES ('טופל'); --1
INSERT INTO ref_hd_ticket_close_reason (ticket_close_reason_name) VALUES ('לא טופל'); --2
INSERT INTO ref_hd_ticket_close_reason (ticket_close_reason_name) VALUES ('מבוטל'); --3
INSERT INTO ref_hd_ticket_close_reason (ticket_close_reason_name) VALUES ('נשלל'); --4


INSERT INTO ref_hd_ticket_note_type (ticket_note_type_name) VALUES ('פתיחה'); --1
INSERT INTO ref_hd_ticket_note_type (ticket_note_type_name) VALUES ('תיעוד'); --2
INSERT INTO ref_hd_ticket_note_type (ticket_note_type_name) VALUES ('סגירה'); --3
INSERT INTO ref_hd_ticket_note_type (ticket_note_type_name) VALUES ('לוג'); --4


INSERT INTO users (user_name, user_class_id, first_name, last_name, passkey, email, phone)
VALUES ('erpy', 1, 'erpy', 'erpy', f_hash_pass(:postgres_password), '1@1.com', '1111'); --1

--TODO: remove after dev stage

-- INSERT INTO users (user_name, user_class_id, first_name, last_name, passkey, email, phone)
-- VALUES ('erpy', 1, 'erpy', 'erpy', f_hash_pass(1234), '1@1.com', '1111'); --1

INSERT INTO users (user_name, user_class_id, first_name, last_name, passkey, email, phone)
VALUES ('ohad24', 2, 'אוהד', 'מזרחי', f_hash_pass(1234), '1@1.com', '1111'); --2

INSERT INTO users (user_name, user_class_id, first_name, last_name, passkey, email, phone)
VALUES ('aaa', 4, 'חיים', 'מזרחי', f_hash_pass(1234), '1@1.com', '1111'); --3

INSERT INTO teams_assignment (team_id, user_id) VALUES (1, 2);