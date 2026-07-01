import os
import json
import sqlite3

ROOT_FOLDER = "output/knight"
DB_NAME = "puzzles.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Drop old tables if they exist
cur.execute("DROP TABLE IF EXISTS puzzle_themes")
cur.execute("DROP TABLE IF EXISTS puzzles")

# Create puzzles table
cur.execute("""
CREATE TABLE puzzles (
    puzzleId TEXT PRIMARY KEY,
    piece TEXT NOT NULL,
    fen TEXT NOT NULL,
    moves TEXT NOT NULL,
    rating INTEGER,
    rd INTEGER,
    popularity INTEGER,
    nbPlays INTEGER,
    gameUrl TEXT
)
""")

# Create puzzle_themes table
cur.execute("""
CREATE TABLE puzzle_themes (
    puzzleId TEXT NOT NULL,
    theme TEXT NOT NULL,
    PRIMARY KEY (puzzleId, theme),
    FOREIGN KEY (puzzleId) REFERENCES puzzles(puzzleId)
)
""")

puzzle_count = 0
theme_count = 0

for filename in sorted(os.listdir(ROOT_FOLDER)):

    if not filename.endswith(".json"):
        continue

    filepath = os.path.join(ROOT_FOLDER, filename)

    print("Reading", filename)

    with open(filepath, "r", encoding="utf-8") as f:
        puzzles = json.load(f)

    for p in puzzles:

        cur.execute("""
        INSERT OR REPLACE INTO puzzles
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["puzzleId"],
            "knight",
            p["fen"],
            p["moves"],
            p.get("rating"),
            p.get("rd"),
            p.get("popularity"),
            p.get("nbPlays"),
            p.get("gameUrl")
        ))

        puzzle_count += 1

        for theme in p.get("themes", []):

            cur.execute("""
            INSERT OR IGNORE INTO puzzle_themes
            VALUES (?, ?)
            """, (
                p["puzzleId"],
                theme
            ))

            theme_count += 1

# Create indexes
cur.execute("CREATE INDEX idx_piece ON puzzles(piece)")
cur.execute("CREATE INDEX idx_rating ON puzzles(rating)")
cur.execute("CREATE INDEX idx_theme ON puzzle_themes(theme)")

conn.commit()
conn.close()

print()
print("Finished!")
print(f"Puzzles imported : {puzzle_count:,}")
print(f"Theme links      : {theme_count:,}")
print(f"Database created : {DB_NAME}")
