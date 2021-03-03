import argparse
import gspread
from requests import get
from datetime import datetime
#from math import floor


def poke_api(offset=None, limit=None):
    try:
        payload = {} if offset is None else {'offset': offset, 'limit': limit}
        print("Payload: {}".format(payload))
        req = get('https://pokeapi.co/api/v2/pokemon/', params=payload)
        
        if req.status_code == 200:
            response = req.json()
            return response
        
        return []

    except Exception:
        raise
        
def get_pokemons(page=None): 
    limit = 20
    page = 0 if page is None else page
    offset = limit * (page - 1)
    
    try:
        response = poke_api(offset, limit)
        
        print("offset: {0} page: {1} limit: {2}".format(offset,page,limit))
        
        results = response.get('results', [])
        count = response.get('count')
        total_pages = round(count / limit)
        
        print("number of pokemons: {} in {} pages".format(count,total_pages))
        
        if (page > total_pages or page < 1):
            print("Please verify the page number")
        else:
            update_spreedsheet(results)
            
    except Exception:
        raise

def update_spreedsheet(data=None): 
    try:
        gc = gspread.service_account("service_account.json")
        worksheet = gc.open("Pokemons")
        sheet = worksheet.sheet1
        row_number = 1
        
        for pokemon in data:
            row = []
            row.append(pokemon['name'])
            row.append(pokemon['url'])
            
            col_values = sheet.col_values(1)
            
            if pokemon['name'] in col_values:
                row_to_update = int(col_values.index(pokemon['name']) + 1)
                print("updating row {} ...".format(row_to_update))
                date_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                sheet.update_cell(row_to_update, 1, str(pokemon['name']))
                sheet.update_cell(row_to_update, 2, str(pokemon['url']))
                sheet.update_cell(row_to_update, 3, str(date_time))
            else:
                print("inserting row number {}".format(row_number))
                sheet.insert_row(row, row_number)
                row_number += 1
            
    except gspread.exceptions.APIError as e:
        print("API Error: ", e)
    except Exception:
        raise
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This application write a spreadsheet with all the pokemons, if pokemon already exists will be updated.')
    parser.add_argument('--page', type=int, help='page number for pagination', default=1)
    args = parser.parse_args()
    
    get_pokemons(page=args.page)