



CREATE TABLE IF NOT EXISTS dim_genre (
    genre_sk_id INT AUTOINCREMENT PRIMARY KEY,
    genre_id INT NOT NULL,
    genre_name VARCHAR(50) NOT NULL
);