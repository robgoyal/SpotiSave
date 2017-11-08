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

    return worksheet, workbook


def close_csv(workbook):

    workbook.close()

def main():

    auth_token = get_auth_token()

    worksheet, workbook = create_csv()

    header = {'Authorization': 'Bearer {}'.format(auth_token)}
    payload = {'limit': 50}
    url = "https://api.spotify.com/v1/me/tracks"


    row = 1

    while True:
        r = requests.get(url, headers = header, params = payload)
        # Check if status code returned 200
        if r.status_code == 200:
            r = r.json()

            for item in r['items']:
                worksheet.write(row, 0, item['track']['id'])
                worksheet.write(row, 1, item['track']['name'])
                worksheet.write(row, 3, item['added_at'])

                row += 1

            # Check if any songs are remaining
            if r['next'] == None:
                break
            else:
                url = r['next']
        else:
            print(r.text)

    close_csv(workbook)

if __name__=="__main__":
    main()