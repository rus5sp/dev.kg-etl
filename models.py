from dataclasses import dataclass
from datetime import datetime, date

from bs4 import BeautifulSoup

 
@dataclass
class Vacancy:
    id: int
    date: date
    position: str
    organization: str
    type: str
    city: str | None
    salary: str | None
    price_from: int | None
    price_to: int | None
    currency: str | None
    description: str
 
    @classmethod
    def from_dict(cls, data: dict) -> 'Vacancy':
        """Construct a Vacancy from a raw API dict."""
        return cls(
            id=data['id'],
            date=_parse_date(data['created_at']),
            position=data['position'],
            organization=data['organization_name'],
            type=data['type'],
            city=data.get('city'),
            salary=data.get('salary'),
            price_from=data.get('price_from'),
            price_to=data.get('price_to'),
            currency=data.get('currency'),
            description=clean_html(data['text']),
        )
 
 
def parse_date(value: str) -> date:
    return datetime.fromisoformat(value.replace('Z', '+00:00')).date()


def clean_html(text: str) -> str:
    return BeautifulSoup(text, 'html.parser').get_text(separator=' ').strip()