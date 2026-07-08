from enum import Enum

class Quote(Enum):
    WET     = 0 # БВИ
    BUDGET  = 1 # Весь общий конкурс (БВИ в том числе)
    UNUSUAL = 2 # Особая квота
    SPECIAL = 3 # Отдельная квота
    TARGET  = 4 # Целевая квот