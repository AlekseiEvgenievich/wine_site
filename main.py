from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime
import numpy as np
import pandas

def year_form(n):
    if 10 <= n % 100 <= 20:
        return 'лет'
    elif n % 10 == 1:
        return 'год'
    elif 2 <= n % 10 <= 4:
        return 'года'
    else:
        return 'лет'

data_today = datetime.datetime.now()
year_today = datetime.datetime.now().year
starting_year = 1920
difference = year_today - starting_year
years_correct = year_form(difference)

#excel_data_df = pandas.read_excel('wine.xlsx')
#caps = excel_data_df.to_dict('records')
excel_data_df = pandas.read_excel('wine3.xlsx')
excel_data_df.replace({np.nan: None}, inplace=True)
organized = excel_data_df.groupby('Категория').apply(lambda x: x.drop('Категория', axis=1).to_dict(orient='records')).to_dict()

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    number=difference,
    years=years_correct,
    organized_data=organized,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

#server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
print(1)
server.serve_forever()
