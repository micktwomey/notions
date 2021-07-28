import enum

import pydantic


class NumberFormat(enum.Enum):
    number = "number"
    number_with_commas = "number_with_commas"
    percent = "percent"
    dollar = "dollar"
    canadian_dollar = "canadian_dollar"
    euro = "euro"
    pound = "pound"
    yen = "yen"
    ruble = "ruble"
    rupee = "rupee"
    won = "won"
    yuan = "yuan"
    real = "real"
    lira = "lira"
    rupiah = "rupiah"
    franc = "franc"
    hong_kong_dollar = "hong_kong_dollar"
    new_zealand_dollar = "new_zealand_dollar"
    krona = "krona"
    norwegian_krone = "norwegian_krone"
    mexican_peso = "mexican_peso"
    rand = "rand"
    new_taiwan_dollar = "new_taiwan_dollar"
    danish_krone = "danish_krone"
    zloty = "zloty"
    baht = "baht"
    forint = "forint"
    koruna = "koruna"
    shekel = "shekel"
    chilean_peso = "chilean_peso"
    philippine_peso = "philippine_peso"
    dirham = "dirham"
    colombian_peso = "colombian_peso"
    riyal = "riyal"
    ringgit = "ringgit"
    leu = "leu"


class Number(pydantic.BaseModel):
    format: NumberFormat
