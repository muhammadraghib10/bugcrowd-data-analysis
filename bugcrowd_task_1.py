from bs4 import BeautifulSoup
import requests
import json
import time
import csv
"""
Step 1: Data Extraction 1
Write a script in Python 3.7+ that retrieves the data of all programs from https://bugcrowd.com/programs and saves the 
results in a CSV file. The program name and the program URL should be saved.

Step 3: Data Analysis
Write a script in Python 3.7+ that reads in the program information obtained in step 2 for all programs and 
searches the text for dollar amounts. Extract the minimum and maximum dollar amount per program found in the text and create a result list with columns Name , URL , MinBounty , and MaxBounty .

Step 4: Result processing
Evaluate the min and max dollar amounts obtained in step 3 and generate a graph of the frequency of min and 
max dollar amounts (histogram). Round the values to full 1000s. As before, you can create a script in Python 
3.7+ or a programming language of your choice, or use a spreadsheet program.

Step 5: Planning further steps
The program information texts loaded in step 2 contain a lot of other interesting information in addition to the monetary rewards. However, these differ greatly across the programs and rarely follow a uniform pattern in terms of content. How would you go about structuring the texts automatically and converting thematically similar blocks (e.g. "Out of Scope" lists or "Exclusion" lists) into a uniform format?

No program is explicitly required here, just a short description of your procedure.
"""
def extract_data(url, total_pages, output_filename):
    """
    Task 1
    params:
    -> url:url of website from which we want to reterive data
    -> total pages: Represents total number of pages available on bugcrowd program tab 
    -> output file name: string
    return value: 
    -> bool. True if data extraction is completed and data is stored in a csv file / false otherwise.
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
            header = ['name', 'program_url', 'min_rewards', 'max_rewards']
            writer = csv.DictWriter(file, fieldnames = header)
            for item in programs_list:
                writer.writerow({
                    'name':item.get('name'),
                    'program_url':url+item.get('program_url'),
                    'min_rewards':item.get('min_rewards'),
                    'max_rewards':item.get('max_rewards')
                })
    except Exception as e:
        print("Error while writing programs data to a csv file. Error: ",e)



if __name__ == "__main__":
    url = "https://bugcrowd.com/programs"
    # Task 1
    extract_data(url, 14,"output.csv")
