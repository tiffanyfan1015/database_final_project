CREATE TABLE Game (
    appid INT PRIMARY KEY,
    name VARCHAR(255),
    release_date DATE,
    english BOOL,
    developer VARCHAR(255),
    publisher VARCHAR(255),
    platforms VARCHAR(255),
    required_age INT,
    category VARCHAR(255),
);


LOAD DATA LOCAL INFILE '/path/to/your/steam.csv'
INTO TABLE Game
FIELDS TERMINATED BY ','
ENCLOSED BY '"'            
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE Comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    appid INT,
    username VARCHAR(255),
    comment TEXT,
    created_at TIMESTAMP
);

CREATE TABLE Description (
    appid INT PRIMARY KEY,
    detailed_description TEXT,
    about_the_game TEXT,
    short_description TEXT
);

LOAD DATA LOCAL INFILE '/path/to/your/description.csv'
INTO TABLE Description
FIELDS TERMINATED BY ','
ENCLOSED BY '"'            
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE Media (
    appid INT PRIMARY KEY,
    header_image TEXT
);

LOAD DATA LOCAL INFILE '/path/to/your/media.csv'
INTO TABLE Media
FIELDS TERMINATED BY ','
ENCLOSED BY '"'            
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE Requirements (
    appid INT PRIMARY KEY,
    pc_requirements TEXT,
    mac_requirements TEXT,
    linux_requirements TEXT,
    minimum TEXT,
    recommended TEXT
);

LOAD DATA LOCAL INFILE '/path/to/your/Requirements.csv'
INTO TABLE Requirements
FIELDS TERMINATED BY ','
ENCLOSED BY '"'            
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE Support (
    appid INT PRIMARY KEY,
    website TEXT,
    support_url TEXT,
    support_email TEXT
);

LOAD DATA LOCAL INFILE '/path/to/your/Support.csv'
INTO TABLE Support
FIELDS TERMINATED BY ','
ENCLOSED BY '"'            
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

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
    user_name VARCHAR(255),
    appid INT,
    tag INT, -- 0=ask, 1=recommend
    content TEXT,
    timestamp DATETIME,
    FOREIGN KEY (group_name) REFERENCES `Groups`(group_name) ON DELETE CASCADE,
    FOREIGN KEY (appid) REFERENCES Game(appid) ON DELETE CASCADE
);

CREATE TABLE GroupChatTable (
    chat_id INT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(255),
    user_name VARCHAR(255),
    post_id INT,
    message TEXT,
    timestamp DATETIME,
    FOREIGN KEY (group_name) REFERENCES `Groups`(group_name) ON DELETE CASCADE,
    -- FOREIGN KEY (user_name) REFERENCES Users (username) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES PostTable(post_id) ON DELETE CASCADE
);