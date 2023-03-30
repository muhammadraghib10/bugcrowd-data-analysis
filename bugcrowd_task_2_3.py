from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time
"""
Step 2: Data Extraction 2
Write a script in Python 3.7+ that gets the program information (the text in the "Program details" tab) for 
each of the programs. In particular, take the program URL from the CSV file generated in step 1.

Step 3: Data Analysis
Write a script in Python 3.7+ that reads in the program information obtained in step 2 for all programs and 
searches the text for dollar amounts. Extract the minimum and maximum dollar amount per program found
in the text and create a result list with columns Name , URL , MinBounty , and MaxBounty .
"""
def import_complete_data_from_csv(file_name):
    """
    Usage: In case we store all 4 attributes in first task then no need for second task. 
    ->input: filename
    -> output: dataframe containing bugcrowd programs data
    -> data example: (program_name, program_link, min_reward, max_reward)<->(OneTrust,https://bugcrowd.com/onetrust,300.0,6500.0)
    """
    data_df = pd.DataFrame()
    try:
        data_df = pd.read_csv(file_name, encoding="ISO-8859-1", names=["program_name","program_link"])
    except Exception as e:
        print("Error while reading data from {file_name}. Error:{error}".format(file_name=file_name, error=e))
    
    return data_df

def import_from_csv(file_name):
    """
    ->input: filename
    -> output: dataframe containing bugcrowd programs data
    -> data example: (program_name, program_link)<->(OneTrust,https://bugcrowd.com/onetrust)
    """
    data_df = pd.DataFrame()
    try:
        data_df = pd.read_csv(file_name, encoding="ISO-8859-1", names=["program_name","program_link"])
    except Exception as e:
        print("Error while reading data from {file_name}. Error:{error}".format(file_name=file_name, error=e))
    
    return data_df

def process_program_detail_data(program_name, program_url):
    """
    ->input: program_name, program_url. Both params are of type string.
    ->output: program dict object of type dictionary
    -> example {
                    "program_name":OneTrust,
                    "program_url":https://bugcrowd.com/onetrust,
                    "min_bounty":300.0,
                    "max_bounty":6500.0
                }

    """
    program_dict = program_dict = {
                    "program_name":program_name,
                    "program_url":program_url,
                    "min_bounty":float("nan"),
                    "max_bounty":float("nan")
                }
    text = ""
    try:
        # Task 2 Retrieve program details data in text form for each available program 
        response_data = requests.get(program_url)
        if response_data.status_code == 200:
            # Task 3 find reward and return program detail dict object
            response_html = BeautifulSoup(response_data.text, "html.parser")
            programs_data = response_html.find("span", {"class": "bc-stat__fig"})
            if programs_data:
                text = programs_data.contents[0]
            junk_value = re.findall( r"\n", text)
            if programs_data and not junk_value:
                bounty = find_reward_amount_from_text(str(programs_data.contents[0]))
                program_dict["min_bounty"], program_dict["max_bounty"] = bounty[0], bounty[1]
    except Exception as e:
        print("Error while reading data from {program_url}. Error:{error}".format(program_url=program_url, error=e))
    
    # Debug print
    print(program_dict)
    return program_dict
    

def find_reward_amount_from_text(text):
    """
    -> input: text containing reward
    -> example: 100$ – 2000$
    -> output: list containing min bounty, max bounty. example[100,2000]
    """
    try:
        bounty = []
        result = re.findall('Points', text)
        if result:
            text = text.replace('Points ', '0')    
        text = text.replace('$', '')   
        text = text.replace(',', '')   
        bounty = text.split('–')
    except Exception as e:
        print("Error while finding reward amount from {text}. Error:{error}".format(text=text, error=e))

    return bounty


if __name__ == "__main__":
    # Importing programs data from csv file 
    programs_data_df = import_from_csv("output_programs_data.csv")
    programs_details_df = pd.DataFrame(columns = ["program_name","program_url","min_bounty","max_bounty"])
    for program in programs_data_df.iterrows():
        program_data = process_program_detail_data(program[1][0], program[1][1])
        programs_details_df = programs_details_df.append(program_data, ignore_index=True)
    
    # writing updated data with 4 values-> program_name, program_url, min_bounty, max_bounty using task 2 and task 3
    programs_details_df.to_csv("updated_programs_data.csv", index=False, header=False)
    print(programs_details_df.info())
        

    
