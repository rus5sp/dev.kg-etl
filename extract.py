import asyncio
import logging

import aiohttp


logger = logging.getLogger(__name__)


BASE_URL = 'https://devkg.com/api'
USER_AGENT = 'dev.kg-etl/1.0 (rustudien@gmail.com)'
CONCURRENCY_LIMIT = 5


async def get(session: aiohttp.ClientSession, sem: asyncio.Semaphore, path: str, params: dict) -> dict:
    """Send a single GET request to the API"""
    url = BASE_URL + path
    headers = {'User-Agent': USER_AGENT}

    async with sem:
        logger.debug('GET %s params=%s', url, params)
        async with session.get(url, headers=headers, params=params) as response:
            response.raise_for_status()
            data = await response.json()

    return data


async def fetch_slugs(session: aiohttp.ClientSession, sem: asyncio.Semaphore, page: int) -> list[str]:
    """Return job slugs from a single listing page."""
    logger.info('Fetching slugs — page %d', page)
    data = await get(session, sem, '/pages/jobs', params={'page': page})
    return [job['slug'] for job in data['result']['list']]


async def fetch_vacancy(session: aiohttp.ClientSession, sem: asyncio.Semaphore, slug: str) -> dict:
    """Return raw vacancy dict for a given slug."""
    logger.info('Fetching vacancy — slug=%s', slug)
    data = await get(session, sem, '/pages/job', params={'slug': slug})
    return data['result']['job']


async def run_extract(pages: int) -> list[dict]:
    """
    Extract raw vacancy dicts from dev.kg for the given number of listing pages.

    Steps:
      1. Fetch all slugs from pages in parallel.
      2. Fetch full vacancy data for each slug in parallel.

    Returns a flat list of raw vacancy dicts.
    """
    sem = asyncio.Semaphore(CONCURRENCY_LIMIT)

    async with aiohttp.ClientSession() as session:
        slug_tasks = [fetch_slugs(session, sem, page) for page in range(1, pages + 1)]
        pages_of_slugs = await asyncio.gather(*slug_tasks)
        slugs = [slug for page in pages_of_slugs for slug in page]
        logger.info('Collected %d slugs across %d pages', len(slugs), pages)

        vacancy_tasks = [fetch_vacancy(session, sem, slug) for slug in slugs]
        vacancies = await asyncio.gather(*vacancy_tasks)
        logger.info('Fetched %d vacancies', len(vacancies))

    return vacancies