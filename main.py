import asyncio
import logging
 
from extract import run_extract
from models import Vacancy
from transform import run_transform
from load import run_load


PAGES = 100


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%H:%M:%S',
)
logger = logging.getLogger(__name__)
 
 
async def main() -> None:
    raw_vacancies = await run_extract(pages=PAGES)
    parsed_vacancies = [Vacancy.from_dict(v) for v in raw_vacancies]
    logger.info('Parsed %d vacancies', len(parsed_vacancies))
 
    df = run_transform(parsed_vacancies)
    logger.info('Transformed vacancies into DataFrame with %d rows', len(df))

    run_load(df)
    logger.info('ETL pipeline completed successfully')
 

if __name__ == '__main__':
    asyncio.run(main())