import re


def extract_numbers(substring) -> list:
    numeros = re.findall(r'\d+', substring)
    numeros = [int(n) for n in numeros]

    return numeros
