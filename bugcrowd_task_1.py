from bs4 import BeautifulSoup
import requests
import json
import time
import csv
"""
Step 1: Data Extraction 1
Write a script in Python 3.7+ that retrieves the data of all programs from https://bugcrowd.com/programs and saves the 
results in a CSV file. The program name and the program URL should be saved.
"""

def extract_data(url, total_pages, output_filename):
    """
    Task 1
    params:
    -> url:url of website from which we want to reterive data
    -> total pages: Represents total number of pages available on bugcrowd program tab 
    -> output file name: string
    """
    try:
        start_page = 0
        programs_data_list = []
        for curr_page in range(start_page, total_pages):
            params ={
                "sort[]": "promoted-desc",
                "page[]": curr_page
            }
            response_data = requests.get(url, params=params)
            if response_data.status_code == 200:
                response_html = BeautifulSoup(response_data.text, "html.parser")
                programs_data = response_html.find("div", {"class": "react-component react-component-program-search-app"})
                # print(programs_data.attrs["data-react-props"])
                programs_data_list.extend(json.loads(programs_data.attrs["data-react-props"])['programs'])
                
                print("Now Reading page", curr_page, "Total programs uptil now=", len(programs_data_list))
            else:
                print("Unable to retrieve data from specified url. Html status code returned = {status_code}".format(status_code=response_data.status_code))

        write_programsdata_to_csv("https://bugcrowd.com", output_filename, programs_data_list)
    except Exception as e:
        print(e)

def write_programsdata_to_csv(url, file_name, programs_list):
    try:
        # Write programs data to csv file
        file = open(file_name, 'w', newline ='')
        with file:
            """
            Note: The commented code is for storing minimum and maximum bounty.
                  Bounty data is also available in html element with label (data-react-props),
                  If we directly store this data in csv then task data extraction 2 becomes
                  redundent.
            """
            header = ['name', 'program_url']#, 'min_rewards', 'max_rewards']
            writer = csv.DictWriter(file, fieldnames = header)
            for item in programs_list:
                writer.writerow({
                    'name':item.get('name'),
                    'program_url':url+item.get('program_url'),
                    # 'min_rewards':item.get('min_rewards'),
                    # 'max_rewards':item.get('max_rewards')
                })
    except Exception as e:
        print("Error while writing programs data to a csv file. Error: ",e)



if __name__ == "__main__":
    url = "https://bugcrowd.com/programs"
    # Task 1
    extract_data(url, 14,"output_programs_data.csv")
