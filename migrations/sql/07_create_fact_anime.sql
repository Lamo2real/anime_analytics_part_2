



CREATE TABLE IF NOT EXISTS fact_anime (
    anime_sk_id INT AUTOINCREMENT PRIMARY KEY,
    anime_id INT NOT NULL,
    studio_id INT,
    title VARCHAR(99) NOT NULL,
    watch_duration INT NOT NULL,
    episodes INT NOT NULL,
    score DECIMAL(2,1) NOT NULL,
    aired_from DATE NOT NULL,
    aired_to DATE,
    is_current BOOLEAN,
    validated BOOLEAN,
    timestamp_loaded DATE NOT NULL,
    FOREIGN KEY (studio_id) REFERENCES dim_studio(studio_id)
);