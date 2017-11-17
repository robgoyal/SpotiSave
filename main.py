# Name: main.py
# Author: Robin Goyal
# Last-Modified: November 16, 2017
# Purpose: Retrieve basic information regarding currently saved tracks
#          on my profile for future use

import requests
import configparser
import xlsxwriter
import json

def get_auth_token():
    '''
    Retrieve authentication token from config file
    '''

    config = configparser.ConfigParser()
    config.read('config.ini')
    AUTH_TOKEN = config['KEY']['AUTH_TOKEN']

    return AUTH_TOKEN

def create_xlsx():
    '''
    Create a CSV file with proper formatting and the following headings:
        - Track Name
        - Album Name
        - Artist(s)
        - Date Added 
        - Track URL
        - Popularity
        - Track ID
    '''

    # Initialize workbook and worksheet
    workbook = xlsxwriter.Workbook('spotifysongs.xlsx')
    worksheet = workbook.add_worksheet()

    # Create formatter for column
    heading_formatter = workbook.add_format({'bold': True, 'align': 'center'})

    # Set column widths
    worksheet.set_column(0, 7, 35, heading_formatter)

    # Create headings for columns
    headings = {'A1': 'Track Name', 'B1': 'Album Name', \
                'C1': 'Artist(s)', 'D1': 'Date Added', \
                'E1': 'Track URL', 'F1': 'Popularity', \
                'G1': 'Track ID'
                }

    # Create columns for headings
    for heading in headings:
        worksheet.write(heading, headings[heading])

    return worksheet, workbook

def close_xlsx(workbook):
    '''
    workbook: workbook file created for song data

    Close xlsx file after saving all data
    '''

    workbook.close()

def make_request(url, auth_token):
    '''
    url: url for spotify request

    Make request for a set of songs (limit of 50) including the offset
    '''

    # Initialize header and payload
    header = {'Authorization': 'Bearer {}'.format(auth_token)}
    payload = {'limit': 50}

    # Make request for specific url
    r = requests.get(url, headers = header, params = payload)

    return r

def write_row(worksheet, row, row_formatter, track_info):
    '''
    track: track information
    row: row to write track information to 

    Write row with specific headings in xlsx file from track
    '''

    # Get basic track information
    track_name = track_info['track']['name']
    album_name = track_info['track']['album']['name']
    date_added = track_info['added_at'].split("T")[0]
    track_url = track_info['track']['href']
    popularity = track_info['track']['popularity']
    track_id = track_info['track']['id']

    # Create list in case of multiple artists
    artists = ", ".join(list(map(lambda x: x['name'], track_info['track']['artists'])))

    # Create row of all basic track info for easy looping
    row_data = [track_name, album_name, artists, date_added, \
                track_url, popularity, track_id]

    # Loop through cols in row and write data
    for col in range(len(row_data)):
        worksheet.write(row, col, row_data[col], row_formatter)


def handle_error(response):
    '''
    Print out an appropriate error message

    response: String of response
    return: String containing response code and response message
    '''

    # Convert string response to dictionary
    response = json.loads(response)

    # Create error message
    response_status = response['error']['status']
    response_message = response['error']['message']

    error_msg = "Error {}: {}".format(response_status, response_message)
    
    return error_msg

def main():
    '''
    Get all song data from the Spotify API and save to excel file
    '''

    # Retrieve authentication token
    auth_token = get_auth_token()

    # Get worksheet and workbook pointer
    worksheet, workbook = create_xlsx()

    # Initialize row to 1 to account for header row
    row = 1

    # Initialize url for initial request
    url = "https://api.spotify.com/v1/me/tracks"

    # Create row formatter for all rows
    row_formatter = workbook.add_format({"bold": False, "align": "left"})

    # Iterate until all requests have been completed
    while True:

        # Perform initial request
        response = make_request(url, auth_token)

        # Check if request was valid
        if response.status_code == 200:
            response = response.json()

            # Append track information to sheet
            for track_info in response['items']:

                # Write row with specific headers
                write_row(worksheet, row, row_formatter, track_info)
                row += 1

            # Check if there are no songs remaining
            if response['next'] == None:
                break

            # Retrieve url for next request
            url = response['next']

        # Handle request errors
        else:
            error_msg = handle_error(response.text)
            print(error_msg)

    # Close csv file
    close_xlsx(workbook)

if __name__=="__main__":
    main()