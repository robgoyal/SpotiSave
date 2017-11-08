import requests
import configparser
import xlsxwriter

def get_auth_token():

    # Retrieve authentication token
    config = configparser.ConfigParser()
    config.read('config.ini')
    AUTH_TOKEN = config['KEY']['AUTH_TOKEN']

    return AUTH_TOKEN

def create_csv():
    workbook = xlsxwriter.Workbook('spotifysongs.xlsx')
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Track ID', bold)
    worksheet.write('B1', 'Track Name', bold)
    worksheet.write('C1', 'Album Name', bold)
    worksheet.write('D1', 'Date Added', bold)

    worksheet.close()


def main():

    auth_token = get_auth_token()

    header = {'Authorization': 'Bearer {}'.format(auth_token)}
    url = "https://api.spotify.com/v1/me/tracks"

    r = requests.get(url, headers = header)
    print(r.text)

if __name__=="__main__":
    main()