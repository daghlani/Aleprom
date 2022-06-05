#!/usr/bin/python
import requests
from requests.auth import HTTPBasicAuth
import sys

user = 'my_user1'
password = 'my_password'
url = 'http://localhost:5000/sendMessage'
severity = sys.argv[1]
text = sys.argv[2]


def requests_query(url, user, password, text, severity, timeout=35):
    """

    :param timeout: timeout of query.
    :param url: Target url that you want to send request to her.
    :param user: auth user.
    :param password: password of user.
    """
    headers = {
        'Content-Type': 'application/json',
    }
    data = dict(
        severity=severity,
        text=text
    )
    try:
        response = requests.post(url, headers=headers, json=data, auth=(user, password),
                                 timeout=int(timeout))
        if response.status_code == 200:
            result = response.status_code
            return result
        else:
            print('status code of request is %s so result is -1.' % response.status_code)
            return -1
    except requests.exceptions.Timeout as Timeout:
        print('request is in error: %s' % Timeout)
        return -1
    except requests.exceptions.HTTPError as HTTPError:
        print('request is in error: %s' % HTTPError)
        return -1
    except requests.exceptions.TooManyRedirects as TooManyRedirects:
        print('request is in error: %s' % TooManyRedirects)
        return -1
    except requests.exceptions.ConnectionError as ConnectionError:
        print('request is in error: %s' % ConnectionError)
        return -1
    except requests.exceptions.RequestException as RequestException:
        print('request is in error: %s' % RequestException)
        return -1


if __name__ == "__main__":
    requests_query(url=url, user=user, password=password, text=text, severity=severity)
