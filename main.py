from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time


def search_wikipedia(query):
    browser.get(
        'https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0')
    assert "Википедия" in browser.title

    search_box = browser.find_element(By.ID, "searchInput")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Ждем загрузки страницы


def list_paragraphs():
    paragraphs = browser.find_elements(By.CSS_SELECTOR, "p")
    for i, paragraph in enumerate(paragraphs):
        print(f"\nПараграф {i + 1}:\n{paragraph.text}")
        user_input = input("Продолжить чтение параграфов? (y/n): ")
        if user_input.lower() != 'y':
            break


def list_links():
    links = browser.find_elements(By.CSS_SELECTOR, "a")
    related_links = [link for link in links if link.get_attribute('href') and "/wiki/" in link.get_attribute('href')]
    for i, link in enumerate(related_links[:10]):  # Показать первые 10 ссылок
        print(f"{i + 1}. {link.text} - {link.get_attribute('href')}")
    return related_links


def choose_link_and_navigate(links):
    while True:
        try:
            choice = int(input(f"Введите номер статьи (1-{len(links)}) или 0 для отмены: "))
            if choice == 0:
                break
            elif 1 <= choice <= len(links):
                browser.get(links[choice - 1].get_attribute('href'))
                break
            else:
                print("Неверный выбор.")
        except ValueError:
            print("Введите номер статьи.")


def main():
    global browser
    browser = webdriver.Firefox()

    while True:
        query = input("Введите запрос для поиска на Википедии (или 'exit' для выхода): ")
        if query.lower() == 'exit':
            break

        search_wikipedia(query)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")

            action = input("Введите номер действия: ")

            if action == '1':
                list_paragraphs()
            elif action == '2':
                links = list_links()
                choose_link_and_navigate(links)
            elif action == '3':
                browser.quit()
                return
            else:
                print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()