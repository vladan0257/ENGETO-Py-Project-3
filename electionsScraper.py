import requests
import pandas as pd
import re
import sys
from bs4 import BeautifulSoup as bs

def getHtmlContent(url: str) -> str:
    '''
    Universal function for getting HTML content from the given URL.

    Args:
        url (str): Any URL.
    '''
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.content
    else:
        print(f'Failed to get data from {url}. Status: {resp.status_code}')
        return None

def getUrlsList(url='https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ') -> list:
    '''
    Extract municipality URLs from a default URL.

    Args:
        url (str): Here as an implicit argument.
    '''
    content = getHtmlContent(url)

    if not content:
        return []
    
    soup = bs(content, 'html.parser')
    headerPattern = re.compile(r'^t(1[0-4]|[1-9])sa3$')
    urlTailsList = [
        td.find('a')['href']
        for td in soup.find_all('td', attrs={'class': 'center', 'headers': headerPattern})
        if td.find('a') is not None
    ]
    
    return [url.rsplit('/', 1)[0] + '/' + urlTail for urlTail in urlTailsList]

def getMunicipDetails(userUrl: str) -> dict:
    '''
    Extract identification details of a desired municipality: Store all municipialities' names, identification
    numbers and assemble URLs referrencing to votes collected within each municipalitiy's electoral district.
    
    Args:
         userUrl (str): Passed by user as a command-line argument.
    '''
    htmlContent = getHtmlContent(userUrl)
    municipDetails = []

    if htmlContent is not None:
        soup = bs(htmlContent, 'html.parser')
        tables = soup.find_all('table', class_='table')
        
        for table in tables:
            rows = table.find_all('tr')[2:]  # Skip header rows
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3 and not any('hidden_td' in td.get('class', []) for td in cols):
                    municipId = cols[0].get_text(strip=True)
                    municipName = cols[1].get_text(strip=True)
                    urlTail = cols[0].find('a')['href'] if cols[0].find('a') else None
                    urlFull = userUrl.rsplit('/', 1)[0] + '/' + urlTail if urlTail else None
                    
                    if urlFull:
                        municipDetails.append({'Kód obce': municipId, 'Název obce': municipName, 'Hlasování-url': urlFull})
    return municipDetails

def getAllVotingData(url: str) -> dict:
    '''
    Get general polls' statistics and votes collected by each party.
    Args:
         url (str): An URL referrencing to votes collected within each municipalitiy's electoral district.
    '''
    htmlContent = getHtmlContent(url)
    result = {
        'General Stats': {
            'Voliči v seznamu': '',
            'Vydané obálky': '',
            'Platné hlasy': ''
        },
        'Party Votes': {}
    }

    if htmlContent is not None:
        soup = bs(htmlContent, 'html.parser')

        # Extract general vote statistics
        generalStats = result['General Stats']
        generalStats['Voliči v seznamu'] = (
            soup.find('td', headers='sa2', attrs={'data-rel': 'L1'}).get_text(strip=True)
            if soup.find('td', headers='sa2', attrs={'data-rel': 'L1'}) else 'none'
        )
        generalStats['Vydané obálky'] = (
            soup.find('td', headers='sa3', attrs={'data-rel': 'L1'}).get_text(strip=True)
            if soup.find('td', headers='sa3', attrs={'data-rel': 'L1'}) else 'none'
        )
        generalStats['Platné hlasy'] = (
            soup.find('td', headers='sa6', attrs={'data-rel': 'L1'}).get_text(strip=True)
            if soup.find('td', headers='sa6', attrs={'data-rel': 'L1'}) else 'none'
        )

        # Extract party collected votes
        partyTables = soup.find_all('table', class_='table')
        for table in partyTables:
            rows = table.find_all('tr')[1:]  # Skip the header row
            for row in rows:
                partyNameElement = row.find('td', class_='overflow_name', headers='t1sa1 t1sb2')
                votesCountElement = row.find('td', class_='cislo', headers='t1sa2 t1sb3')

                if partyNameElement and votesCountElement:
                    partyName = partyNameElement.get_text(strip=True)
                    votesCount = votesCountElement.get_text(strip=True)
                    result['Party Votes'][partyName] = votesCount

    return result
#===================================================================================================
def main():

    print('Ziskavam seznam dostupnych odkazu...')
    urlsList = getUrlsList()

    if sys.argv[1] not in urlsList:
        print('Zadana URL adresa nebyla v seznamu dostupnych URL adres nalezena. Zadejte dostupnou adresu.')

    elif sys.argv[2] in urlsList and sys.argv[1].endswith('.csv'):
        print('Prvni argument ma byt URL adresa - odkaz na okres s volebnimi daty, druhy argument ma byt jmeno vystupniho souboru.', 
        'Vase argumenty jsou prehozene.', sep='\n')
    
    else:
        print('Zpracovavam data z Vasi URL adresy...')
        electData = []
        
        municipalities = getMunicipDetails(sys.argv[1])

        # Set to collect unique party names
        allParties = set()

        # Loop through each municipality's electoral districts to get votes data
        for municipality in municipalities:
            votesData = getAllVotingData(municipality['Hlasování-url'])
            municipality.update(votesData['General Stats'])  # Combine municipal data with general stats
            
            # Add parties to the set of party names
            allParties.update(votesData['Party Votes'].keys())
            electData.append(municipality)

        # Create a DataFrame and initialize party columns
        df = pd.DataFrame(electData)

        # Add party columns with default values
        for party in allParties:
            df[party] = None  # Initialize party columns with None

        # Fill in the party vote counts for each municipality
        for idx, municipality in df.iterrows():
            votesData = getAllVotingData(municipality['Hlasování-url'])['Party Votes']
            for party, votes in votesData.items():
                df.at[idx, party] = votes  # Assign votes to the respective party column

        # Erase 'Hlasování-url' column
        df = df.drop(columns=['Hlasování-url'])

        # Save to CSV
        scriptName = sys.argv[0]
        fileName = sys.argv[2]
        print(f'Zapisuji do souboru {fileName} a ukladam...')
        df.to_csv(fileName, index=False, encoding='utf-8-sig')
        print(f'Ukoncuji {scriptName}.')

if __name__ == '__main__':
    main()
