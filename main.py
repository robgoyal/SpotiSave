# Name: main.py
# Author: Robin Goyal
# Last-Modified: November 8, 2017
# Purpose: Retrieve basic information regarding currently saved tracks
#          on my profile for future use

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

    # Initialize workbook and worksheet
    workbook = xlsxwriter.Workbook('spotifysongs.xlsx')
    worksheet = workbook.add_worksheet()

    # Create formatter
    bold = workbook.add_format({'bold': True})

    # Declare headings for worksheet
    worksheet.write('A1', 'Track ID', bold)
    worksheet.write('B1', 'Track Name', bold)
    worksheet.write('C1', 'Album Name', bold)
    worksheet.write('D1', 'Date Added', bold)

    return worksheet, workbook


def close_csv(workbook):
    '''
    workbook: workbook file created for song data
    '''

    workbook.close()

def main():

    # Retrieve authentication token
    auth_token = get_auth_token()

    # Get worksheet and workbook pointer
    worksheet, workbook = create_csv()

    # Setup data regarding initial request
    header = {'Authorization': 'Bearer {}'.format(auth_token)}
    payload = {'limit': 50}
    url = "https://api.spotify.com/v1/me/tracks"

    # Initialize row to 1 to account for header row
    row = 1

    while True:

        # Perform initial request
        r = requests.get(url, headers = header, params = payload)

        # Check if status code returned 200
        if r.status_code == 200:
            r = r.json()

            # Append track information to sheet
            for item in r['items']:
                worksheet.write(row, 0, item['track']['id'])
                worksheet.write(row, 1, item['track']['name'])
                worksheet.write(row, 3, item['added_at'])

                row += 1

            # Check if there are no songs remaining
            if r['next'] == None:
                break

            # Retrieve url for next request
            else:
                url = r['next']

        # Print error message for debugging
        else:
            print(r.text)

    # Close csv file
    close_csv(workbook)

if __name__=="__main__":
    main()