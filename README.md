INTRODUCTION:	
The script electionsScraper.py serves as an tool for collecting and downloading data of the Czech parliamentary election beying held in 2017. It scrapes data from one particular region called "okres" (There's no equivalent word for that term in english as far as I am concerned.) from the basket of all that regions in the Czech Republic and downloads them to a csv format file. For it to work, user must call the script in command line environment with two arguments. First is URL address refferencing to one particular "okres" and second is a desired name of the final csv file. Naming of the file is restricted in no way other than it needs to have a "csv" suffix.

EXAMPLE OF THE COMMAND:	
python electionsScraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2103" vysledky_kladno.csv

FOLLOWING PROGRESS REMARKS:	
Ziskavam seznam dostupnych odkazu...
Zpracovavam data z Vasi URL adresy...
Zapisuji do souboru vysledky_kladno.csv a ukladam...
Ukoncuji electionsScraper.py.
