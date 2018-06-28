"""This file contains all unchangeable values."""

NOR_INCOME = 'INCOME'
NOR_EXPENSE = 'EXPENSE'
CONTRACT_INCOME = 'CINCOME'
CLASS_CHANGE_INCOME = 'CHANINCOME'
SALARY_EXPENSE = 'SEXPENSE'

FORM_CHOICES = (
    (NOR_INCOME, 'Орлого'),
    (NOR_EXPENSE, 'Зарлага'),
)

TXN_TYPES = (
    (SALARY_EXPENSE, 'Цалингын зарлага'),
    (CONTRACT_INCOME, 'Гэрээний орлого'),
    (CLASS_CHANGE_INCOME, 'Ангий солилтын орлого'),
    (NOR_INCOME, 'Орлого'),
    (NOR_EXPENSE, 'Зарлага'),
)

JANUARY = "JANUARY"
FEBRUARY = "FEBRUARY"
MARCH = "MARCH"
APRIL = "APRIL"
MAY = "MAY"
JUNE = "JUNE"
JULY = "JULY"
AUGUST = "AUGUST"
SEPTEMBER = "SEPTEMBER"
OCTOBER = "OCTOBER"
NOVEMBER = "NOVEMBER"
DECEMBER = "DECEMBER"

MONTHS = (
    (JANUARY, '1-р сар'),
    (FEBRUARY, '2-р сар'),
    (MARCH, '3-р сар'),
    (APRIL, '4-р сар'),
    (MAY, '5-р сар'),
    (JUNE, '6-р сар'),
    (JULY, '7-р сар'),
    (AUGUST, '8-р сар'),
    (SEPTEMBER, '9-р сар'),
    (OCTOBER, '10-р сар'),
    (NOVEMBER, '11-р сар'),
    (DECEMBER, '12-р сар'),
)

FIRST_SHIFT = 'FIRST'
SECOND_SHIFT = 'SECOND'

SHIFTS = (
    (FIRST_SHIFT, '1-р ээлж'),
    (SECOND_SHIFT, '2-р ээлж'),
)


BEGINNER = "BEGINNER"
BMID = "BMID"
MID = "MID"
AMID = "AMID"
ADVANCED = "ADVANCED"


LEVEL_CHOICES = (
    (BEGINNER, "Анхан"),
    (BMID, "Дундын өмнөх"),
    (MID, "Дунд"),
    (AMID, "Ахисан дунд"),
    (ADVANCED, "Гүнзгий"),
)

BY_BANK = "BY_BANK"
BY_CASH = "BY_CASH"

TXN_METHODS = (
    (BY_BANK, "Дансаар"),
    (BY_CASH, "Бэлнээр"),
)


FREE = "FREE"
NON_FREE = "NON_FREE"

CLASS_CHANGE_CHOICES = (
    (FREE, "Төлбөргүй"),
    (NON_FREE, "Төлбөртэй"),
)
