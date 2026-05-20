import logging
import sqlite3
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)


def load_to_sqlite(df: pd.DataFrame, db_path: str = 'vacancies.db') -> None:
    """Load DataFrame to SQLite database."""
    with sqlite3.connect(db_path) as conn:
        df.to_sql(f'vacancies_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}', conn, if_exists='replace', index=False)
    logger.info('Loaded %d vacancies to %s', len(df), db_path)


def run_load(df: pd.DataFrame) -> None:
    """Run the load step of the ETL pipeline."""
    load_to_sqlite(df)