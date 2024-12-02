CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE IF NOT EXISTS `groups` (
    group_id INT NOT NULL,
    group_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (group_id)
);

CREATE TABLE IF NOT EXISTS group_with_user (
    group_id INT NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (group_id, user_id),
    FOREIGN KEY (group_id) REFERENCES `groups`(group_id),
    FOREIGN KEY (user_id) REFERENCES users(username)
);


CREATE TABLE IF NOT EXISTS group_chat (
    chat_id INT NOT NULL AUTO_INCREMENT,
    group_id INT NOT NULL,
    post_id INT NOT NULL,
    message_ TEXT,
    time_stamp DATETIME NOT NULL,
    PRIMARY KEY (chat_id),
    FOREIGN KEY (group_id) REFERENCES `groups`(group_id),
    FOREIGN KEY (post_id) REFERENCES post_table(post_id)
);

CREATE TABLE IF NOT EXISTS post_table (
    post_id INT NOT NULL AUTO_INCREMENT,
    group_id INT NOT NULL,
    appid INT NOT NULL,
    review_text_private TEXT NOT NULL,
    time_stamp DATETIME NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (group_id) REFERENCES `groups`(group_id)
);
