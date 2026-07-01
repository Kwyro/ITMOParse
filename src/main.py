import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import pandas as pd

from typing import List, Dict

from ORM import Student

programmNumber = 2342 # Номер направления (указывается в ссылке самого направления)
URL = f"https://abit.itmo.ru/_next/data/2gVOXLiouyaB4bhDUzQw8/ru/rating/bachelor/budget/{programmNumber}.json?degree=bachelor&financing=budget&id={programmNumber}"

def parseStudents(quote: Dict, category: str) -> List[Student]:
    """Функция для парсинга данных студентов по категориям"""
    students = list()
    for student in quote:
        id = student["sspvo_id"]
        disciplines_scores = student["disciplines_scores"]
        priority = student["priority"]
        ia_scores = student["ia_scores"]
        total_scores = student["total_scores"]
        agreement = student["is_send_agreement"]
        
        student = Student(id, disciplines_scores, priority, ia_scores, total_scores, agreement)
        students.append(student)
    
    return students

def save_to_excel(students: List[Student], listName: str, workbook: Workbook, first: bool = False) -> None:
    if first:
        sheet = workbook.active
        sheet.title = listName
    else:
        workbook.create_sheet(listName)
        sheet = workbook[listName]

    sheet.append(["ID", "Общее количество баллов", "Сумма баллов за ЕГЭ", "Дополнительные баллы", "Приоритет", "Согласие"])

    for student in students:
        sheet.append([
            student.id,
            student.total_scores,
            sum(student.disciplines_scores.values()),
            student.ia_scores,
            student.priority,
            student.agreement
        ])

def main() -> None:
    responce = requests.get(url=URL)
    result = responce.json()
    
    pageProps = result['pageProps']
    programList = pageProps["programList"] # Все студенты во всех квотах

    # Распределение студентам по квотам
    WET = programList["without_entry_tests"]     # БВИ
    unusual = programList["by_unusual_quota"]    # Особая квота
    special = programList["by_special_quota"]    # Отдельная квота
    target = programList["by_target_quota"]      # Целевое обучение
    general = programList["general_competition"] # Общий конкурс
    
    # Массивы с студентами
    WET_Students = parseStudents(WET, "БВИ")
    unusual_Students = parseStudents(unusual, "Особая квота")
    special_Students = parseStudents(special, "Отдельная квота")
    target_Students = parseStudents(target, "Целевая квота")
    general_Students = parseStudents(general, "Общий конкурс")
    
    # Сохранение данных в файл itmo.xlsx
    workbook = Workbook()
    save_to_excel(general_Students, "Общий конкурс", workbook, first=True)
    save_to_excel(unusual_Students, "Особая квота", workbook)
    save_to_excel(special_Students, "Отдельная квота", workbook)
    save_to_excel(WET_Students, "БВИ", workbook)

    workbook.save("ИТМО.Программная инженерия.xlsx") # Название таблицы

if __name__ == "__main__":
    main()