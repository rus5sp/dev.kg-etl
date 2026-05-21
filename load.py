import logging
import sqlite3
import os

import pandas as pd


logger = logging.getLogger(__name__)


TABLE_NAME = 'vacancies'


def init_db(df: pd.DataFrame, db_path: str) -> None:
    with sqlite3.connect(db_path) as conn:
        df.head(0).to_sql(TABLE_NAME, conn, index=False)
        conn.execute(
            f'CREATE UNIQUE INDEX IF NOT EXISTS idx_id ON {TABLE_NAME}(id)'
        )
    logger.info('Initialized database at %s', db_path)


def load_to_sqlite(df: pd.DataFrame, db_path: str = 'vacancies.db') -> None:
    if not os.path.exists(db_path):
        init_db(df, db_path)

    columns = ', '.join(df.columns)
    placeholders = ', '.join(['?'] * len(df.columns))

    with sqlite3.connect(db_path) as conn:
        cursor = conn.executemany(
            f'INSERT OR IGNORE INTO {TABLE_NAME} ({columns}) VALUES ({placeholders})',
            df.values
        )

    logger.info(
        'Processed %d vacancies: %d new, %d already existed',
        len(df), cursor.rowcount, len(df) - cursor.rowcount
    )