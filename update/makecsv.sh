DB=indexes.db
if [ -f "$DB" ]; then
    echo "DB file exists, removing it."
    rm "$DB"
fi
python3 python/create_sqlite.py
python3 python/insert_sqlite.py
python3 python/generate_csv.py
python3 python/generate_summary.py
