import requests
from requests_ntlm2 import HttpNtlmAuth


# Notes
# В итоге выяснилось, что и NTLM уязвим, и специалисты Microsoft подготовили NTLMv2, который до сих пор считается
# достаточно надежным, хотя сейчас предпочтительный протокол — Kerberos
#
# NTLMv2 похож на NTLM, но в хеше пароля NTLMv2 используется аутентификация сообщений HMAC-MD5, а последовательности
# запрос—ответ присваивается метка времени, чтобы предотвратить атаки, в ходе которых взломщик записывает учетные
# данные и впоследствии их использует.


def signup_post(request):
    """Получаем POST запрос с логином и паролем от клиента"""
    name = request.form.get('name')
    password = request.form.get('password')


def check_auth(url, username, password):
    """Принимает и проверяет логин и пароль"""
    try:
        auth = HttpNtlmAuth(f'domain\\{username}', password)
        response = requests.get(url, auth=auth)
        print('response text=', response.text)
        response.raise_for_status()
        return True
    except Exception as e:
        return False


print(check_auth('http://127.0.0.1:8000/', 'admin', 'Admin2023'))
