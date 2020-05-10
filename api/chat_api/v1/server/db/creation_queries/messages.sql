CREATE TABLE IF NOT EXISTS 'messages'(
    'id' INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
    'msg_timestamp' DATETIME NOT NULL,
    'id_dest' INT NOT NULL,
    'id_mitt' INT NOT NULL,
    'message' VARCHAR(250) NOT NULL,
    'len' INT NOT NULL,
    'type' VARCHAR(10) NOT NULL DEFAULT 'text',
    'received' INT NOT NULL DEFAULT 0,
    CONSTRAINT ForeignDest FOREIGN KEY ('id_dest') REFERENCES 'users'('id')
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT ForeignMitt FOREIGN KEY ('id_mitt') REFERENCES 'users'('id')
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT ChkReceived CHECK (received IN (0, 1))
);