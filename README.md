# Nirvana CTF — "Something in the Way"

A blind boolean-based SQL injection challenge disguised as a Nirvana fan page.

---

## Challenge Info

- **Category**: Web Exploitation
- **Difficulty**: Medium
- **Flag**: `CTF{k0me_as_you_4re!!}`
- **Hint**: *"Colorblind — Nirvana"*

---

## Setup

### 1. Install dependencies

```bash
pip install flask
```

### 2. Create the database

```bash
python setup_db.py
```

This creates `nirvana.db` (SQLite) with:
- `songs` table — the searchable discography
- `admin` table — contains the flag password

### 3. Run the app

```bash
python app.py
```

Visit: `http://localhost:5000`

---

## File Structure

```
nirvana-ctf/
├── app.py          # Flask app (vulnerable backend)
├── setup_db.py     # DB creation + seeding script
├── nirvana.db      # Generated SQLite database (after setup)
├── README.md
└── templates/
    ├── index.html  # Fan page with search + oracle word
    ├── admin.html  # Login page
    └── flag.html   # Flag display (post-login)
```

---

## Vulnerability Details

**Injection point**: `GET /search?q=<input>`

The search query is interpolated directly into SQL:
```python
f"SELECT * FROM songs WHERE title LIKE '%{q}%'"
```

**Oracle**: The word `colour` (British) vs `color` (American) in the page blurb.
- Query returns rows → `colour` → **TRUE**
- Query returns nothing → `color` → **FALSE**

**Escape the LIKE clause**:
```
%' AND SUBSTRING(password,1,1)='a'-- -
```

---

## Intended Solve (Burp Suite)

1. Search anything, intercept in **Proxy**, send to **Repeater**
2. Confirm injection: `%' AND 1=1-- -` → `colour`, `%' AND 1=2-- -` → `color`
3. Send to **Intruder**, payload position on the character:
   ```
   q=%' AND SUBSTRING(password,§1§,1)='§a§'-- -
   ```
   *(Use Cluster Bomb — position 1 iterates 1–20, position 2 iterates charset)*
4. **Options → Grep Match** → add `colour`
5. Hits with checkmark = correct character
6. Assemble the 20-char password, log in at `/admin`

---

## Notes for CTF Organisers

- The `/admin` route is intentionally not linked anywhere on the page
- No `robots.txt`, no HTML comments, no other hints — SQLi is the only path
- Change the flag password in `setup_db.py` before deploying
- Run with `debug=False` in production (already set in app.py)
