import requests
from requests import Response
from openpyxl import Workbook

from typing import List, Dict

from ORM import Student
from quoteEnum import Quote
from codes import programs
from service import getQuote, parseStudents

code: str = input("Введите номер программы: ")

programmNumber = programs[code]        # Номер направления (указывается в ссылке самого направления)
strangePart = "YtZroTHbw-TByDqFwY3fe"  # Какой-то странный фрагмент api-запроса, который непонятно откуда доставать

URL: str = f"https://abit.itmo.ru/_next/data/{strangePart}/ru/rating/bachelor/budget/{programmNumber}.json?degree=bachelor&financing=budget&id={programmNumber}"

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
    # Распределение студентам по квотам
    WET:     dict = getQuote(URL, Quote.WET)        # БВИ
    unusual: dict = getQuote(URL, Quote.UNUSUAL)    # Особая квота
    special: dict = getQuote(URL, Quote.SPECIAL)    # Отдельная квота
    target:  dict = getQuote(URL, Quote.TARGET)     # Целевое обучение
    general: dict = getQuote(URL, Quote.BUDGET)     # Общий конкурс
    
    # Массивы с студентами
    WET_Students:     list[Student] = parseStudents(WET, "БВИ")
    unusual_Students: list[Student] = parseStudents(unusual, "Особая квота")
    special_Students: list[Student] = parseStudents(special, "Отдельная квота")
    target_Students:  list[Student] = parseStudents(target, "Целевая квота")
    general_Students: list[Student] = parseStudents(general, "Общий конкурс")
    
    # Сохранение данных в файл .xlsx
    workbook = Workbook()
    save_to_excel(general_Students, "Общий конкурс", workbook, first=True)
    save_to_excel(target_Students, "Целевая квота", workbook)
    save_to_excel(unusual_Students, "Особая квота", workbook)
    save_to_excel(special_Students, "Отдельная квота", workbook)
    save_to_excel(WET_Students, "БВИ", workbook)

    workbook.save(f"ИТМО.{code}.xlsx") # Название таблицы

if __name__ == "__main__":
    main()