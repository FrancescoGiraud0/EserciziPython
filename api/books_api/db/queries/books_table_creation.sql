CREATE TABLE IF NOT EXISTS "Books" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "title" VARCHAR(50) NOT NULL,
    "author" VARCHAR(50) NOT NULL,
    "year_published" INTEGER NOT NULL,
    CONSTRAINT "checkYear" CHECK( "year_published" <= date("%Y", "now") )
);