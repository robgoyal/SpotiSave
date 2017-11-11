## SpotiSave

### Purpose

A Python script designed to export all saved songs from Spotify to an Excel file. This will allow me to easily view all my songs, apply specific filters, and save the songs in case of some freak accident regarding the Spotify data deleting all my saved songs.

### Functionality

The functionality of this project will initially be completely basic:
    - One time run to save all songs
    - Save a certain set of headings:
        - Track ID 
        - Track Name
        - Artist(s)
        - Album Name
        - Date Added
        - Link to spotify URL
        - Popularity

### Future 

The above may be the only functionality included for the purpose of this project.

### Requirements

#### Authentication Token 

This project requires account creation for Spotify and obtaining an authentication token from the API console in the Spotify API. 

Save the authentication token in a config.ini file with the contents:

```
[KEY]
AUTH_TOKEN = "your-auth-token"
```

#### Required Libraries

- requests
- configparser
- xlsxwriter