import requests
from datetime import datetime

# URLs для скачивания списков
url_1 = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ooni_domains.lst"
url_2 = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/community.lst"
url_3 = "https://community.antifilter.download/list/domains.lst"
url_4 = "https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-raw.lst"

# Имя итогового файла
output_file = "gfwlist.txt"

def download_list(url):
    try:
        print(f"Скачивание списка: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        print("Список успешно скачан.")
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании списка: {e}")
        return []

def extract_domains(lines):
    return {
        line.strip()
        for line in lines
        if line.strip()
        and not line.startswith("#")
        and not line.startswith("!")
    }

def save_to_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        for line in data:
            file.write(line + "\n")
    print(f"Итоговый список сохранён в {filename}")

def process_and_refilter(output_file):
    urls = [url_1, url_2, url_3, url_4]
    all_domains = set()

    for url in urls:
        lines = download_list(url)
        all_domains.update(extract_domains(lines))

    print(f"Объединено {len(all_domains)} уникальных доменов.")

    # Формируем список доменов в формате ||domain
    formatted_domains = [f"||{domain}" for domain in sorted(all_domains) if not domain.startswith("||")]

    # Текущая дата и время создания
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Первая строка — нужный заголовок, далее дата, пустая строка, домены
    final_output = [
        "[AutoProxy 0.2.9]",
        f"! Generated on: {current_time}",
        ""
    ] + formatted_domains

    save_to_file(output_file, final_output)

if __name__ == "__main__":
    process_and_refilter(output_file)
