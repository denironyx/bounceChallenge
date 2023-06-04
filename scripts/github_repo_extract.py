# Import libraries
import requests
import pandas as pd
import os

# To Do:
# - Write a test to verify the repo we are pulling from
# - Request error try and catch
# - Count the number of repo fetched and exported

# Step 1 - Set up headers
    # fetch github token
user_account = 'bounceapp'
github_token = os.environ.get('GITHUB_TOKEN')

headers = {
    'User-Agent': 'vscode terminal',
    'Authorization': 'Token '+github_token
}

# Step 2 - Extract all repo name
# Start the page pagination with 1
page_num = 1

# Create empty list
pages = []

# Custom Duplicate Checker
def duplicate_checker(values):
        def has_duplicates(values):
            if len(values) != len(set(values)):
                return True
            else:
                return False
        if has_duplicates(values):
            duplicate_in_coin = values.duplicated(subset=['names'])
            if duplicate_in_coin.any():
                values = values.loc[~duplicate_in_coin].reset_index(drop = True)
                return values

def scrape_github_data():
    # Waiting until things break
    while True:
        print("------")
        print(f"Page: {page_num}")
        url = f"https://api.github.com/users/{user_account}/repos?page={page_num}"
        
        # Establish url request 
        response = requests.get(url, headers=headers)

        # Test 1: Code here will only run if the request is successful
        if(response.status_code == 200):
            print('The request was a success!')
            
            # Decode the JSON response into aa dictionary and use the data
            data = response.json()

            #Test 2: Debug by printing out the first data extracted
            try:
                print(data[0]['full_name'])
            except:
                print("There was an error while fetching the data")
                break

        # Code here will break on failed request
        else:
            print('There is a failed request! ', response.status_code)
        
        # if we find repos name in a page, append them to our list
        pages.append(data)
        
        # Checking if we are getting data from the right source
        if(pages[0][0]['owner']['login'].upper() == user_account.upper()):
            print(f"Looking good! {pages[0][0]['owner']['login']}")
        else:
            print('Warning: we are getting data from the wrong source')

        # increase the page count by 1
        page_num = page_num + 1
        
    # loop pages to check for empty pages
    for page in pages:
        if page == []:
            print(f"There is no repos in this page: {pages.index(page)}")
            break

    # count the number of repos found
    len(pages[0])

    # Extract the repo names
    repo_names = []
    forks = []
    for page in pages:
        for repo in page:
            try:
                repo_names.append(repo['full_name'].split("/")[1])
                forks.append(repo['forks'])
            except:
                pass

    # create a dataframe and store the values in it
    repo_data = pd.DataFrame()
    repo_data['name'] = repo_names
    repo_data['number_of_forks'] = forks

    # Check for duplicate with this custom duplicate checker
    duplicate_checker(repo_data)
    
    return repo_data 

# Export data
def export_to_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False)

# Scrape GitHub data and store it in a dataframe
df = scrape_github_data()

# Export the dataframe to a CSV file
export_to_csv(df, "github_data.csv")