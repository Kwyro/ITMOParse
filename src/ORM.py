from typing import Dict

class Student:
    def __init__(self, id: int, disciplines_scores: Dict[str, int | None] | None, priority: int, ia_scores: int, total_scores: int, agreement: bool) -> None:
        self.id = id                                                      # ССПВО ID
        self.disciplines_scores = self.__check_scores(disciplines_scores) # Баллы за каждый предмет
        self.priority = priority                                          # Приоритет направления
        self.ia_scores = ia_scores                                        # Сумма баллов за ИД
        self.total_scores = total_scores                                  # Сумма баллов (ВИ + ИД)
        self.agreement = agreement                                        # Есть ли согласие

    def __check_scores(self, disciplines_scores: Dict[str, int | None] | None) -> Dict[str, int]:
        if disciplines_scores is None:
            return {"Математика": 0, "Русский язык": 0, "Информатика": 0}
        if isinstance(disciplines_scores, list):
            return {"Математика": 0, "Русский язык": 0, "Информатика": 0}
        for subject, score in disciplines_scores.items():
            if score is None:
                disciplines_scores[subject] = 0
        return disciplines_scores