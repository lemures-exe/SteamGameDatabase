# SteamGameDatabase
Before running this you will need to add your API_KEY + STEAM_ID to a .env file in the same directory.
You can get your Steam API Key from the following URL: https://steamcommunity.com/dev/apikey
You can get your Steam ID from going to Steam > Account Details (Under **ACCOUNT NAME**)

This Python application will create a .csv file in the same directory as itself. It collects the following information:
* Game Title
* Hours Played
* App ID
* Release Date
* Developer
* Publisher
* Genre
* Mode
* Last Played Date

I decided to limit the amount of genres for some of the games because certain games have 5+ so I decided to limit it just to 2 currently but this can be changed if you needed.
## API's Needed To Run

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `API_KEY` | `string` | **Required**. Your Steam API key |

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `STEAM_ID`      | `string` | **Required**. Your Steam ID |

## Similar Projects

[GetDataFromSteam - Sak32009](https://github.com/Sak32009/GetDataFromSteam-SteamDB)

## Authors

- [@lemures-exe](https://github.com/lemures-exe)

## License

**SteamGameDatabase** is licensed under the [MIT License.](https://choosealicense.com/licenses/mit/)

