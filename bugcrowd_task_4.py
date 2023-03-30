
import pandas as pd
import matplotlib.pyplot as plt

"""
Step 4: Result processing
Evaluate the min and max dollar amounts obtained in step 3 and generate a graph of the frequency of min and 
max dollar amounts (histogram). Round the values to full 1000s. As before, you can create a script in Python 
3.7+ or a programming language of your choice, or use a spreadsheet program.

"""

def import_from_csv(file_name):
    """
    ->input: filename
    -> output: dataframe containing bugcrowd programs data
    -> data example: (program_name, program_link, min_reward, max_reward)<->(OneTrust,https://bugcrowd.com/onetrust,300.0,6500.0)
    """
    data_df = pd.DataFrame()
    try:
        data_df = pd.read_csv(file_name, encoding="ISO-8859-1", names = ["program_name","program_url","min_bounty","max_bounty"])
    except Exception as e:
        print("Error while reading data from {file_name}. Error:{error}".format(file_name=file_name, error=e))
    
    return data_df

def display_bounties_histogram(min_bounty, max_bounty):
    """
    -> input:min_bounty, max_bounty. Both are dict objects.
       Each contain the bounty value and its number of occurences in the data.
    -> output: It displays a histogram.
    """

    histogram_input_1 = [min_bounty['value'] for i in range(min_bounty['occurrences'])]
    histogram_input_2 = [max_bounty['value'] for i in range(max_bounty['occurrences'])]
    histogram_input = histogram_input_1 + histogram_input_2
    plt.hist(histogram_input)
    plt.ylabel("Number of Occurences")
    plt.xlabel("Min bounty / Max bounty")
    plt.title("Bug crowd minimum maximum bounty occurences histogram")
    plt.show()
    pass
if __name__ == "__main__":
    data_df = import_from_csv("updated_programs_data.csv")

    # task 4
    min_bounty = {
        "value": 0,
        "occurrences":0
    }
    max_bounty = {
        "value": 0,
        "occurrences":0
    }
    # Finding min bounty  and its occurences
    min_bounty['value']= data_df["min_bounty"].drop_duplicates(keep='first').nsmallest(1, keep='first').iloc[0]
    min_bounty["occurrences"] = data_df["min_bounty"].value_counts()[min_bounty['value']]
    # Finding max bounty and its occurences
    max_bounty['value'] = data_df["max_bounty"].nlargest(1).iloc[0]
    max_bounty["occurrences"] =  data_df["max_bounty"].value_counts()[max_bounty["value"]]

   # Displaying min bounty and max bounty
    print(min_bounty)
    print(max_bounty)

    # Displaying min, max bounties histogram
    display_bounties_histogram(min_bounty, max_bounty)
    # plt.hist(data_df['min_bounty'], histtype='bar', bins=13)
    # plt.show()

    