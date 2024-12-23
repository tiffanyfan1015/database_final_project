
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

CREATE TABLE Users (
    username VARCHAR(255) NOT NULL PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE `Groups` (
    group_name VARCHAR(255) NOT NULL PRIMARY KEY,
    group_info VARCHAR(255)
);

CREATE TABLE GroupWithUser (
    group_name VARCHAR(255),
    username VARCHAR(255),
    PRIMARY KEY (group_name, username),
    FOREIGN KEY (group_name) REFERENCES `Groups`(group_name) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE PostTable (
    post_id INT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(255),
    appid INT,
    review_text_private TEXT,
    timestamp DATETIME,
    FOREIGN KEY (group_name) REFERENCES GroupTable(group_name) ON DELETE CASCADE,
    FOREIGN KEY (appid) REFERENCES Game(appid) ON DELETE CASCADE
);

CREATE TABLE GroupChatTable (
    chat_id INT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(255),
    post_id INT,
    message TEXT,
    timestamp DATETIME,
    FOREIGN KEY (group_name) REFERENCES GroupTable(group_name) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES PostTable(post_id) ON DELETE CASCADE
);
