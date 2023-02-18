CREATE TABLE IF NOT EXISTS temperature_by_time (
    temperature REAL NOT NULL, 
    time TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS teapot_state (
    state TEXT NOT NULL,
    time TEXT NOT NULL
);