--users--
INSERT INTO users ("username", "password", "is_admin")
VALUES
('admin', 'pbkdf2:sha256:260000$Ok1YsbzJIUiLUIqC$076180e2657090eef94f250cf17300afe9d007997132b496dfae5d1eac59e37a', 1);

INSERT INTO users ("username", "password", "is_admin")
VALUES
('user', 'pbkdf2:sha256:260000$h8Uw9VC3SrLzGsth$f499ef5a11afae9b1f55a64f6827e605585ede23bc93e71a3708e90cc75bdc57', 0);

INSERT INTO users ("username", "password", "is_admin")
VALUES
('userx', 'pbkdf2:sha256:260000$OhaDgBhnSdwT3sJD$6440c58a64e9af710a90e5d3339fd4cd883a9962b8e01d1ca61a7281a11ac211', 0);

--books--
INSERT INTO books ("title", "subject", "author", "count")
VALUES
('Clean Code', 'Computer', 'Robert C. Martin', 0);

INSERT INTO books ("title", "subject", "author", "count")
VALUES
('The Fault In Our Stars', 'Story', 'John Green', 2);

INSERT INTO books ("title", "subject", "author", "count")
VALUES
('1984', 'Story', 'George Orwell', 2);

INSERT INTO books ("title", "subject", "author", "count")
VALUES
('The C Programming Language', 'Computer', 'me', 2);

--borrows--
INSERT INTO borrows ("borrower", "book", "date_borrowed", "due_date", "date_returned")
VALUES
('user', 'The Fault In Our Stars', "25-04-2022", "02-05-2022", NULL);

INSERT INTO borrows ("borrower", "book", "date_borrowed", "due_date", "date_returned")
VALUES
('userx', '1984', "25-04-2022", "02-05-2022", NULL);

INSERT INTO borrows ("borrower", "book", "date_borrowed", "due_date", "date_returned")
VALUES
('user', 'Clean Code', "25-04-2022", "02-05-2022", "30-04-2022");

INSERT INTO borrows ("borrower", "book", "date_borrowed", "due_date", "date_returned")
VALUES
('user', 'Clean Code', "25-04-2022", "02-05-2022", "10-05-2022");

INSERT INTO borrows ("borrower", "book", "date_borrowed", "due_date", "date_returned")
VALUES
('userx', 'The C Programming Language', "25-04-2022", "02-05-2022", "01-05-2022");

INSERT INTO borrows ("borrower", "book", "date_borrowed", "due_date", "date_returned")
VALUES
('userx', 'The C Programming Language', "25-04-2022", "02-05-2022", "04-05-2022");
