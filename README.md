**INTRODUCTION:**	<br />
The script electionsScraper.py serves as an tool for collecting and downloading data of the Czech parliamentary election beying held in 2017. It scrapes data from one particular region called "okres" (There's no equivalent word for that term in english as far as I am concerned.) from the basket of all that regions in the Czech Republic and downloads them to a csv format file. For it to work, user must call the script in command line environment with two arguments. First is URL address refferencing to one particular "okres" and second is a desired name of the final csv file. Naming of the file is restricted in no way other than it needs to have a "csv" suffix.<br />

**REQUIREMENTS:** <br />
Before initiating the script, make sure all Python libraries are at your disposal. The most straightforward way, when you don't want to check them all one by one, is their installation straight from the file requirements.txt. In order to do that, open your terminal and navigate to directory, where all the files including electionsScraper.py and requirements.txt are located and type: pip3 install -r requirements.txt. <br />

**INITIATION OF THE SCRIPT:**	<br />
In the command line type-in: <br />
python electionsScraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2103" vysledky_kladno.csv <br /><br />
![term1](https://github.com/user-attachments/assets/0dc71f93-8137-436a-b3d1-08887d694fb5)<br />
You will get results from the area called Kladno. For all other available regions, the URL is always behind the 2nd cross-check field. Click on it, copy-paste the adress into your command line and add name of the file. <br />
![chooseRegion](https://github.com/user-attachments/assets/be092d7a-001d-4dd9-b749-3323eac221e5)
 <br />

**SCRIPT PROGRESS REMARKS:**	<br />
![term2](https://github.com/user-attachments/assets/9efd4aff-8c3e-44a0-8a1e-8d89e1594165)

