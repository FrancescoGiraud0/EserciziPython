CREATE TABLE IF NOT EXISTS 'messages'(
    'id' INTEGER UNIQUE PRIMARY KEY UNIQUE NOT NULL,
    'msg_timestamp' DATETIME NOT NULL,
    'id_mitt' INT NOT NULL,
    'message' VARCHAR(250) NOT NULL,
    'len' INT NOT NULL,
    'type' VARCHAR(10) NOT NULL DEFAULT 'text',
    CONSTRAINT ForeignMitt FOREIGN KEY ('id_mitt') REFERENCES 'contacts'('id')
        ON DELETE SET NULL
        ON UPDATE CASCADE
);