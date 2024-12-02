
CREATE TABLE Game (
    appid INT PRIMARY KEY,
    name VARCHAR(255),
    release_date DATE,
    genres VARCHAR(255),
    platforms VARCHAR(255),
    category VARCHAR(255),
    developer VARCHAR(255),
    owner_count INT,
    `2d_or_3d` VARCHAR(50)
);

CREATE TABLE SteamReview (
    app_id INT PRIMARY KEY,
    app_name VARCHAR(255),
    review_score DECIMAL(5, 2),
    review_votes INT,
    review_text TEXT
);

CREATE TABLE UserTable (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE GroupTable (
    group_id INT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(255) NOT NULL
);

CREATE TABLE GroupWithUser (
    group_id INT,
    user_id INT,
    PRIMARY KEY (group_id, user_id),
    FOREIGN KEY (group_id) REFERENCES GroupTable(group_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES UserTable(user_id) ON DELETE CASCADE
);

CREATE TABLE PostTable (
    post_id INT PRIMARY KEY AUTO_INCREMENT,
    group_id INT,
    appid INT,
    review_text_private TEXT,
    timestamp DATETIME,
    FOREIGN KEY (group_id) REFERENCES GroupTable(group_id) ON DELETE CASCADE,
    FOREIGN KEY (appid) REFERENCES Game(appid) ON DELETE CASCADE
);

CREATE TABLE GroupChatTable (
    chat_id INT PRIMARY KEY AUTO_INCREMENT,
    group_id INT,
    post_id INT,
    message TEXT,
    timestamp DATETIME,
    FOREIGN KEY (group_id) REFERENCES GroupTable(group_id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES PostTable(post_id) ON DELETE CASCADE
);
