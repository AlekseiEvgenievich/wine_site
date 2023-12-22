import argparse
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import numpy as np
import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def create_parser ():
    parser = argparse.ArgumentParser(description='Программа предназначена для запуска и рендеринга сайта с винами')
    parser.add_argument('--excelfile',default = 'wine3.xlsx', help = 'Загрузка Excel файла с наименованием вин')
    return parser


def get_year_form_in_russian(years):
    if 10 <= years % 100 <= 20:
        return 'лет'
    elif years % 10 == 1:
        return 'год'
    elif 2 <= years % 10 <= 4:
        return 'года'
    else:
        return 'лет'
        
        
def main():
    year_today = datetime.datetime.now().year
    starting_year = 1920
    difference = year_today - starting_year
    years_correct = get_year_form_in_russian(difference)

    parser = create_parser()
    args = parser.parse_args()

    excel_data_df = pandas.read_excel(args.excelfile)
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
        product_data=organized,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
    
  
if __name__ == '__main__':
    main()
