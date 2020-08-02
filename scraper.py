import requests
import lxml.html as html
import os
import datetime
import json

HOME_URL_WEB_DEVELOPER = 'https://www.ironhack.com/es/desarrollo-web'
HOME_URL_ANALITICS = 'https://www.ironhack.com/es/data-analytics'
HOME_URL_UX_UI = 'https://www.ironhack.com/es/diseno-ux-ui'

XPATH_TITLE = '//*[@id="gatsby-focus-wrapper"]/header/section[2]/section/h1/text()'
XPATH_SUBTITLE = '//*[@id = "gatsby-focus-wrapper"]/header/section[2]/section/p/text()'

XPATH_TITLE_DESCRIPTION = '//*[@id = "gatsby-focus-wrapper"]/section[1]/h2/text()'
XPATH_MAIN_DESCRIPTION_TITLE = '//*[@id = "gatsby-focus-wrapper"]/section[1]/section[3]/article/h3/text()'
XPATH_MAIN_DESCRIPTION_TEXTS = '//*[@id = "gatsby-focus-wrapper"]/section[1]/section[3]/article/p/text()'


def parse_home(url, type):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            title = parsed.xpath(XPATH_TITLE)[0]
            subtitle = parsed.xpath(XPATH_SUBTITLE)[0]
            title_description = parsed.xpath(XPATH_TITLE_DESCRIPTION)[0]
            main_description_title = parsed.xpath(
                XPATH_MAIN_DESCRIPTION_TITLE)[0]
            main_description_texts = parsed.xpath(XPATH_MAIN_DESCRIPTION_TEXTS)
            # print(f'main_description_texts: {main_description_texts}')

            ironhackObject = {
                'title': title,
                'subtitle': subtitle,
                'description': {
                    'title': title_description,
                    'main_description_title': main_description_title,
                    'main_description_texts': main_description_texts
                }
            }

            # today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir('ironhack'):
                os.mkdir('ironhack')

            # with open(f'{today}/ironhack.txt', 'w', encoding='utf-8') as f:
            #     f.write(title)
            #     f.write('\n\n')
            #     f.write(subtitle)

            with open(f'ironhack/{type}.json', 'w', encoding='utf-8') as f:
                json.dump(ironhackObject, f)
        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def run():
    parse_home(HOME_URL_WEB_DEVELOPER, 'web_developer')
    parse_home(HOME_URL_ANALITICS, 'data_analytics')
    parse_home(HOME_URL_UX_UI, 'ux_ui')


if __name__ == '__main__':
    run()
