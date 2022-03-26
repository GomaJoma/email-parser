import requests
import json
from bs4 import BeautifulSoup


def extract_email(row):
    for el in row.split('>'):
        if '@' in el:
            for ell in el.split('<'):
                if '@' in ell:
                    for elll in ell.split(' '):
                        if '@' in elll:
                            if 'href="' in elll:
                                if ':' in elll:
                                    email = elll.split(':')[-1][:-1]
                                else:
                                    email = elll.split('=')[-1].strip('"')
                            else:
                                email = elll
                            return email


def main():
    with open('err.log', 'w') as err:
        output = {}
        for i in range(1, 99):
            num = str(i) if i > 9 else '0' + str(i)
            url = 'https://' + num + '.domain'  # Change this string as your wish

            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.42 (Edition Yx 05)'}
            response = None
            try:
                response = requests.get(url, headers=headers)
            except:
                error = 'Не удалось подключиться к сайту: ' + url + '\n'
                err.write(error)
                print('Не удалось подключиться к сайту:', url)
            if response:
                if response.status_code == 200:
                    emails = {}
                    soup = BeautifulSoup(response.text, 'lxml')
                    body = str(soup.find('body'))
                    body_rows = body.split('\n')
                    for line in body_rows:
                        if '@' in line:
                            mail_index = line.find('@')
                            if line[mail_index-1] == '/':
                                continue
                            email = extract_email(line)
                            if '\xa0' in email:
                                email = email[1:]
                            if email not in emails:
                                emails[email] = {
                                    'num': num,
                                    'url': url,
                                }
                    output[num] = emails
                    print(emails)
                else:
                    print(response.status_code)
        with open('emails.json', 'w') as file:
            file.write(json.dumps(output, ensure_ascii=False))


if __name__ == '__main__':
    main()
