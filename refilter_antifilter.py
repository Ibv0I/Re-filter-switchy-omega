import requests
from datetime import datetime
import re

# URLs для скачивания списков
url_ooni = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ooni_domains.lst"  # URL ooni списка
url_community = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/community.lst"  # URL community списка
url_antifilter = "https://community.antifilter.download/list/domains.txt"  # URL списка antifilter

# Имя итогового файла
output_file = "Re-filter+antifilter.txt"

def download_list(url):
    """Скачивает список доменов по URL."""
    try:
        print(f"Скачивание списка: {url}")
        response = requests.get(url)
        response.raise_for_status()
        print("Список успешно скачан.")
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании списка: {e}")
        return []

def extract_domains(lines):
    """Извлекает домены из простого списка доменов."""
    return {line.strip() for line in lines if line.strip()}  # Убираем пробелы и пустые строки

def clean_antifilter(lines):
    """Очищает список antifilter от формата Switchy Omega, оставляя только домены."""
    domains = set()
    domain_pattern = re.compile(r"^\*://\*\.(.+)/\*$")  # Регулярка для извлечения доменов
    for line in lines:
        line = line.strip()
        match = domain_pattern.match(line)
        if match:
            domains.add(match.group(1))  # Добавляем только домен
        else:
            print(f"Пропущена некорректная строка: {line}")
    return domains

def convert_to_switchy(domains):
    """Преобразует домены в формат Switchy Omega."""
    switchy_lines = ["#BEGIN\n\n[Wildcard]\n"]
    for domain in sorted(domains):  # Сортируем для порядка
        switchy_lines.append(f"*://*.{domain}/*\n")
    switchy_lines.append("#END\n")
    return switchy_lines

def save_to_file(filename, lines):
    """Сохраняет строки в файл."""
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(lines)
    print(f"Итоговый список сохранён в {filename}")

def process_and_refilter(url1, url2, url3, output_file):
    """Скачивает, обрабатывает списки и сохраняет результат."""
    # Скачиваем списки
    ooni_list = download_list(url1)
    community_list = download_list(url2)
    antifilter_list = download_list(url3)

    # Извлекаем домены из первого и второго списка
    ooni_domains = extract_domains(ooni_list)
    community_domains = extract_domains(community_list)

    # Очищаем третий список от формата Switchy Omega, оставляя только домены
    antifilter_domains = clean_antifilter(antifilter_list)

    # Создаем общий список доменов
    all_domains = ooni_domains.union(community_domains).union(antifilter_domains)
    print(f"Объединено {len(all_domains)} уникальных доменов.")

    # Преобразуем в формат Switchy Omega для итогового списка
    switchy_lines = convert_to_switchy(all_domains)

    # Добавляем дату и время составления списка
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    switchy_lines.append(f"\n# Generated on: {current_time}\n")

    # Сохраняем итоговый список
    save_to_file(output_file, switchy_lines)

if __name__ == "__main__":
    process_and_refilter(url_ooni, url_community, url_antifilter, output_file)
