a = "003"
b = 'batik'
print(f"[{a}]")

from datetime import date

def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age
print(calculateAge(date(1999, 8, 7)), "years")

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
print(calculate_age(date(1999, 8, 7)))