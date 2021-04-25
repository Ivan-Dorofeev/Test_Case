import os
import re

import requests
from django.contrib.admin.models import LogEntry

from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Эта команда скачивает содержимое файла по ссылке и записывает в базу данных'

    def add_arguments(self, parser):
        """Добавляем аргумент парсера - ссылку на страничку"""
        parser.add_argument('log_url', type=str, action='store', help='url to the log file')

    def handle(self, **options):
        """Парсим ссылку, пишем дынные в БД"""
        with requests.get(options['log_url'], stream=True) as r:
            if not r.ok:
                raise CommandError(f'URL status code: {r.status_code}')
            with tqdm(total=int(r.headers['Content-Length'])) as pbar:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        for line in chunk.decode('utf-8').splitlines():
                            if line:
                                print('LINES = ', line)
                                data = str(line).split(' ')
                                print('DATA = ', data)
                                le = LogEntry(ip=data[0], date=data[3][0], http_method=data[4],
                                              url_request=data[5],
                                              code_response=data[7], size_response=data[8])
                                le.save()
                pbar.update(len(chunk))
        self.stdout.write(self.style.SUCCESS('Команда "logparser" выполнена!'))
