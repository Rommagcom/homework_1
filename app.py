import requests
import json
import os
import yaml
from requests import HTTPError
from config import Config
from datetime import date

def app(config, process_dates = None):

    if not process_dates:
        date_to_process = config['directory']
        process_dates = date_to_process['dates_to_process'] #If parameter is null getting dates from config
    
    url = config['url']+'/auth'
    my_headers = {'Content-Type' : 'application/json'}
    params= {"username": config['username'], "password": config['password']}

    json_data = json.dumps(params)
    
    response = requests.post(url, data=json_data,headers=my_headers)

    resp_auth = response.json()

    if response.status_code == 200: #If request is success getting order details
        
        for process_date in process_dates:
            os.makedirs(os.path.join(config['directory'], process_date),exist_ok=True) # Directory creation
        
            url = config['url']+'/out_of_stock'
            my_headers = {'Authorization' :'JWT ' + resp_auth['access_token']}
            params= {'date': process_date }

            try:
                response = requests.get(url, params=params, headers = my_headers)
            
                if response.status_code == 200: #if response is ok writing results to files
                    product_ids = list(response.json())
                    for product_id in product_ids:
                        with open (os.path.join(config['directory'],process_date, str(product_id['product_id'])+'.json'),'w') as json_file:
                            json.dump(product_id,json_file)
                else: 
                    print("Please check your connection or input parameters")

            except HTTPError:
                print("Error")

    else:
        print("Please check your connection")


if __name__=='__main__':
    config = Config(os.path.join('.','config.yaml'))
    process_date = ['2021-01-02','2021-01-03','2021-01-04']
    app(config.get_config('rd_api_app'),process_date)