import os
import re

import requests
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from apache.case.models import LogEntry


class Command(BaseCommand):
    help = 'the custom command allows to download the log file and insert data into the database'
    LOG_REGEX = re.compile(
        os.getenv('LOG_REGEX', r'(?P<ip>.+) (?P<user_id>.+) (?P<user_name>.+) \[(?P<date>.+)\] "(?P<method>.+) '
                               r'(?P<request_path>.+) HTTP\/(?P<http_version>.+)" (?P<status_code>\d+) '
                               r'(?P<response_size>.*) "(?P<referrer>.*)" "(?P<user_agent>.*)" "-"'))

    def add_arguments(self, parser):
        parser.add_argument('log_url', type=str, action='store', help='url to the log file')

    def handle(self, **options):
        with requests.get(options['log_url'], stream=True) as r:
            if not r.ok:
                raise CommandError(f'URL status code: {r.status_code}')

            with tqdm(total=int(r.headers['Content-Length'])) as pbar:
                not_ended_line = None  # Переменная необходима, чтобы перенести незаконченную строку на следующий цикл
                log_entry_list = list()

                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        for line in chunk.decode('utf-8').splitlines():
                            try:
                                if not_ended_line:
                                    line = not_ended_line + line

                                data = self.LOG_REGEX.match(line).groupdict()

                                log_entry_list.append(LogEntry(ip=data['ip'],
                                                               user_id=data['user_id'],
                                                               user_name=data['user_name'],
                                                               date=data['date'],
                                                               method=data['method'],
                                                               request_path=data['request_path'],
                                                               http_version=data['http_version'],
                                                               status_code=data['status_code'],
                                                               response_size=data['response_size'] if data[
                                                                   'response_size'].isdigit() else 0,
                                                               referrer=data['referrer'],
                                                               user_agent=data['user_agent']
                                                               ))

                                not_ended_line = None  # Должна быть всегда None, если регулярка успешно совпала

                                if len(log_entry_list) == 1_000_000:
                                    LogEntry.objects.bulk_create(log_entry_list)
                                    log_entry_list.clear()

                            except AttributeError:  # В случае несовпадения регулярки, строку переносим на другой цикл
                                if not not_ended_line:
                                    not_ended_line = line
                            except Exception:
                                pass

                        pbar.update(len(chunk))

                if log_entry_list:
                    LogEntry.objects.bulk_create(log_entry_list)

            self.stdout.write(self.style.SUCCESS('Custom command logparser completed'))