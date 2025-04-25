



CREATE TABLE IF NOT EXISTS fact_anime (
    anime_sk_id INT AUTOINCREMENT PRIMARY KEY,
    anime_id INT NOT NULL,
    studio_sk_id INT,
    title VARCHAR(99) NOT NULL,
    watch_duration INT NOT NULL,
    episodes INT NOT NULL,
    score FLOAT(2),
    trailer_link VARCHAR(255),
    aired_from DATE NOT NULL,
    aired_to DATE,
    is_current BOOLEAN,
    validated BOOLEAN,
    timestamp_loaded DATE NOT NULL,
    FOREIGN KEY (studio_sk_id) REFERENCES dim_studio(studio_sk_id)
);