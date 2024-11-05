import re


def extract_numbers(substring) -> list:
    numeros = re.findall(r'\d+', substring)
    numeros = [int(n) for n in numeros]

    return numeros


def display_progress_bar(completed, total, bar_length=50):
    progress = int(bar_length * completed / total)
    bar = '=' * progress + ' ' * (bar_length - progress)
    completed = min(completed, total)

    print(f'\r[{bar}] {completed}/{total} linhas processadas', end='')
