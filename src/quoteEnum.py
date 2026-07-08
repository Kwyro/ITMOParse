from enum import Enum

class Quote(Enum):
    WET     = 0 # БВИ
    BUDGET  = 1 # Общий конкурс
    UNUSUAL = 2 # Особая квота
    SPECIAL = 3 # Отдельная квота
    TARGET  = 4 # Целевая квот