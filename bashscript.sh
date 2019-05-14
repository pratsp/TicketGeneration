#!/user/bin/bash
python3 ticket_gen.py 1000 act.json;
python3 jsontodb.py act.json activity.db;
sqlite3 activity.db ".read sqlscript.sql"