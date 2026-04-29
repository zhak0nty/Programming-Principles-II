# TSIS4 Snake

## Run

```bash
cd TSIS4
../.venv/bin/python main.py
```

## PostgreSQL

- Uses `psycopg2` and `config.py`
- Default DB name: `snake_db` (override via `PGDATABASE`)
- Auto-creates tables: `players`, `game_sessions`

## Includes

- Main Menu / Settings / Leaderboard / Game Over screens
- Username entry on menu
- Save score, level and timestamp to PostgreSQL after game over
- Top 10 leaderboard from DB and personal best in gameplay
- Poison food (shortens snake, can end run)
- Power-ups: speed boost, slow motion, shield
- Obstacles from level 3 with safe spawning
- `settings.json` for snake color, grid, sound
