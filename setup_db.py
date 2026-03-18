import sqlite3
import os

DB_PATH = "nirvana.db"

def setup_db():
    # Delete existing DB if present
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[*] Removed existing {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- Songs table (searched by users) ---
    cursor.execute("""
        CREATE TABLE songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            album TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    """)

    # --- Admin table (contains the flag password) ---
    cursor.execute("""
        CREATE TABLE admin (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Seed songs
    songs = [
        ("Smells Like Teen Spirit", "Nevermind", 1991),
        ("Come as You Are",         "Nevermind", 1991),
        ("Lithium",                 "Nevermind", 1991),
        ("Polly",                   "Nevermind", 1991),
        ("In Bloom",                "Nevermind", 1991),
        ("Heart-Shaped Box",        "In Utero",  1993),
        ("All Apologies",           "In Utero",  1993),
        ("Rape Me",                 "In Utero",  1993),
        ("Frances Farmer",          "In Utero",  1993),
        ("About a Girl",            "Bleach",    1989),
        ("School",                  "Bleach",    1989),
        ("Blew",                    "Bleach",    1989),
        ("Drain You",               "Nevermind", 1991),
        ("Territorial Pissings",    "Nevermind", 1991),
        ("Something in the Way",    "Nevermind", 1991),
        ("Where Did You Sleep",     "MTV Unplugged", 1994),
        ("The Man Who Sold the World", "MTV Unplugged", 1994),
        ("Lake of Fire",            "MTV Unplugged", 1994),
        ("Pennyroyal Tea",          "In Utero",  1993),
        ("Dumb",                    "In Utero",  1993),
    ]
    cursor.executemany("INSERT INTO songs (title, album, year) VALUES (?, ?, ?)", songs)

    # Seed admin — password is the flag (exactly 20 chars)
    cursor.execute(
        "INSERT INTO admin (id, username, password) VALUES (1, 'admin', ?)",
        ("L0n6L!v3kUr7K08aN3",)
    )

    conn.commit()
    conn.close()

    print(f"[+] Database '{DB_PATH}' created successfully")
    print(f"[+] {len(songs)} songs inserted")
    print(f"[+] Admin credentials seeded")
    print(f"\n[*] To start the challenge, run:  python app.py")

if __name__ == "__main__":
    setup_db()
