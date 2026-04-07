"""
Add trial_start and trial_period_end columns to subscriptions table if missing.
"""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "coffeechat.db")


def add_columns():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for col in ("trial_start", "trial_period_end"):
        try:
            cur.execute(f"ALTER TABLE subscriptions ADD COLUMN {col} DATETIME")
            print(f"Added column: {col}")
        except Exception as e:
            # Likely column already exists; log and continue
            print(f"Skip {col}: {e}")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    add_columns()

