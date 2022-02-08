INSERT INTO users (username, password, is_admin)
VALUES ('admin', 'pbkdf2:sha256:260000$bjQfFlgJn9cxeStI$ccc213ba5e0e37a9d50315064c6c9db26e6014533a399e4bbb460e9b681bba54', true);

INSERT INTO users (username, password, is_admin)
VALUES ('user', 'pbkdf2:sha256:260000$bjQfFlgJn9cxeStI$ccc213ba5e0e37a9d50315064c6c9db26e6014533a399e4bbb460e9b681bba54', false);
