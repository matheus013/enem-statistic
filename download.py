# taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
import requests


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


ids = [
    # ('1BH1Pg5GipRkfM8MFiA0HQxTMB45jlpAs', 2009),
    # ('1n8byZOnGMsSezTKk0EFKdRKy9GkrbA2Q', 2010),
    # ('1UtpeturU0KAt5YdrePQY76GTveWok-zq', 2011),
    # ('1KWbYhnuTc6AwMy2-bwKWCWLujnjAENlY', 2012),
    # ('17ab_5WYBaFO0ZV66PqJexOUmVQq09IPZ', 2013),
    # ('1MMnEOGtrc6cPbBOmBbgXu8eK3lMZWtoS', 2014),
    # ('1HWtn6F-66ShlP2SNookUPYWvGqI8kqm5', 2015),
    # ('1ebQMsNGbJ5oRB-NG59n2c2FFaiapJ9Rf', 2016),
    # ('1VlKNnVuv3LESU66kv8Tc9yJ_DkKYDi_K', 2017),
    # ('1Rj1LNONfCcGRoaFB6IlYaUkMQv0kVWLq', 2018),
    # ('1580YGFZv0OB9zcWtxggZxhUmVDXwODZi', 2019),
    # ('1VNZ0dnSvR5p3771FQZrPoevuASHnwBTJ', 'names')
    ('1-1z2FLQCweWJH1Hl-4tyQkDRdCnTkNmm', '100k')
]

for i in ids:
    print("download from {}".format(i[1]))
    download_file_from_google_drive(i[0], str(i[1]) + '.csv')
