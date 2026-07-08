from typing import List, Dict
from requests import Response
import requests

from ORM import Student
from quoteEnum import Quote
from main import parseStudents

def getStudentList(quote: Quote) -> List[Student]:
    ...

def getQuote(URL: str, quote: Quote) -> Dict:
    """Функция для получения данных студентов из API сайта"""
    responce: Response = requests.get(url=URL)
    result = responce.json()
    
    pageProps = result['pageProps']
    programList = pageProps["programList"] # Все студенты во всех квотах

    match quote:
        case Quote.BUDGET:  return programList["general_competition"] # Общий конкурс
        case Quote.SPECIAL: return programList["by_special_quota"]    # Отдельная квота
        case Quote.TARGET:  return programList["by_target_quota"]     # Целевое обучение
        case Quote.WET:     return programList["without_entry_tests"] # БВИ
        case Quote.UNUSUAL: return programList["by_unusual_quota"]    # Особая квота