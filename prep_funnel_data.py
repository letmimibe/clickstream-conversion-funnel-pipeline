import pandas as pd
import sqlite3
import os

RAW_FILE = 'event-history.csv'
DB_NAME = 'funnel_warehouse.db'
TABLE_NAME = 'events'

def process_clickstream_in_chunks(file_path, db_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' tidak ditemukan.")
        return

    print(f"Memproses {file_path} secara chunking ke {db_path}...")
    
    # Hapus DB lama jika ada untuk reset clean
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    chunk_size = 200000  # Memproses 200.000 baris per batch
    total_processed = 0

    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # 1. Hapus baris tanpa user_session atau user_id
        df_clean = chunk.dropna(subset=['user_id', 'user_session']).copy()
        
        # 2. Filter hanya event relevan untuk conversion funnel
        df_clean = df_clean[df_clean['event_type'].isin(['view', 'cart', 'purchase'])]
        
        # 3. Format timestamp ke standar datetime ISO
        df_clean['event_time'] = pd.to_datetime(df_clean['event_time'], errors='coerce')
        df_clean = df_clean.dropna(subset=['event_time'])
        df_clean['event_time'] = df_clean['event_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # 4. Ingest ke SQLite Table
        df_clean.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
        
        total_processed += len(df_clean)
        print(f"Berhasil memproses {total_processed:,} baris...")

    # Buat Index untuk mempercepat query SQL Funnel
    print("Membuat index database untuk optimasi query SQL...")
    cursor = conn.cursor()
    cursor.execute(f"CREATE INDEX idx_user_session ON {TABLE_NAME} (user_session, event_type);")
    cursor.execute(f"CREATE INDEX idx_event_time ON {TABLE_NAME} (event_time);")
    conn.commit()
    conn.close()

    print(f" Selesai! Database '{db_path}' siap digunakan dengan total {total_processed:,} events.")

if __name__ == "__main__":
    process_clickstream_in_chunks(RAW_FILE, DB_NAME)