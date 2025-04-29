

CREATE TABLE IF NOT EXISTS bridge_anime_genre (
    anime_sk_id INT,
    genre_id INT,
    PRIMARY KEY (anime_sk_id, genre_id),
    FOREIGN KEY (anime_sk_id) REFERENCES fact_anime(anime_sk_id),
    FOREIGN KEY (genre_id) REFERENCES dim_genre(genre_id)
);
