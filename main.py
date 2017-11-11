# Name: main.py
# Author: Robin Goyal
# Last-Modified: November 10, 2017
# Purpose: Retrieve basic information regarding currently saved tracks
#          on my profile for future use

import requests
import configparser
import xlsxwriter

def get_auth_token():
    '''
    Retrieve authentication token from config file
    '''

    pass

def create_xlsx():
    '''
    Create a CSV file with proper formatting and the following headings:
        - Track ID
        - Track Name
        - Artist(s)
        - Album Name
        - Date Added 
        - Track URL
        - Popularity
    '''

    pass


def close_xlsx(workbook):
    '''
    workbook: workbook file created for song data

    Close xlsx file after saving all data
    '''

    pass

def make_request(url):
    '''
    url: url for spotify request

    Make request for a set of songs (limit of 50) including the offset
    '''

    pass

def write_row(row, track):
    '''
    track: track information
    row: row to write track information to 

    Write row with specific headings in xlsx file from track
    '''

    pass

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

    # Iterate until all requests 
    while True:

        # Perform initial request
        r = make_request(url)

        # Check if request was valid
        if r.status_code == 200:

            # Append track information to sheet
            for item in r['items']:

                # Write row with specific headers
                write_row(row, item)
                row += 1

            # Check if there are no songs remaining
            if r['next'] == None:
                break

            # Retrieve url for next request
            url = r['next']

        # Handle request errors
        # Initial handler is a print debug statement
        else:
            print(r.text)

    # Close csv file
    close_xlsx(workbook)

if __name__=="__main__":
    main()