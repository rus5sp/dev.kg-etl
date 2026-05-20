import logging

import pandas as pd

from models import Vacancy


logger = logging.getLogger(__name__)


def convert_to_dataframe(vacancies: list[Vacancy]) -> pd.DataFrame:
    """Convert a list of Vacancy objects to a pandas DataFrame."""
    return pd.DataFrame(vacancies)


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate vacancies based on 'id', keeping the first occurrence."""
    if df['id'].duplicated().any():
        logger.warning('Found %d duplicate vacancies based on id', df['id'].duplicated().sum())
    return df.drop_duplicates(subset=['id'], keep='first')


def remove_nan_values(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with NaN values in critical columns."""
    critical = ['position', 'organization', 'date']
    if df[critical].isna().values.any():
        missing = df[critical].isna().any(axis=1).sum()
        logger.warning('Found %d vacancies with missing critical fields', missing)
    return df.dropna(subset=critical)


def sort_by_date(df: pd.DataFrame) -> pd.DataFrame:
    """Sort vacancies by date in descending order."""
    return df.sort_values('date', ascending=False).reset_index(drop=True)


def run_transform(vacancies: list[dict]) -> pd.DataFrame:
    """Run the transform step of the ETL pipeline."""
    df = convert_to_dataframe(vacancies)
    df = remove_duplicates(df)
    df = remove_nan_values(df)
    df = sort_by_date(df)
    return df