# Import Libraries
import requests
import pandas as pd

# To Do:
# - Create a class
# - Write a test to verify the repo we are pulling from
# - Request error try and catch
# - Count the number of repo fetched and exported

# Step 1 - Set up headers
    # fetch github token

class GitHubScraper:
    def __init__(self, user_account, github_token):
        self.user_account = user_account
        self.github_token = github_token
        self.page_num = 1
        self.pages = []
        self.headers = {
            'User-Agent': 'vscode terminal',
            'Authorization': 'Token ' + github_token
        }

    def scrape_github_data(self):
        # Scrape GitHub data - Waiting until things break
        while True:
            print("------")
            print(f"Page: {self.page_num}")
            url = f"https://api.github.com/users/{self.user_account}/repos?page={self.page_num}"
            # Establish url request 
            response = requests.get(url, headers=self.headers)

            # This will only run if the request is successful
            if response.status_code == 200:
                print('The request was a success!')

                # Decode the JSON response into aa dictionary and use the data
                data = response.json()

                # Debug by printing out the first data extracted
                try:
                    print(data[0]['full_name'])
                except:
                    print("There was an error while fetching the data")
                    break
            # Code here will break on failed request
            else:
                print('There is a failed request! ', response.status_code)

            # if we find repos name in a page, append them to our list
            self.pages.append(data)

            # Checking if we are getting data from the right source
            if self.pages[0][0]['owner']['login'].upper() == self.user_account.upper():
                print(f"Looking good! {self.pages[0][0]['owner']['login']}")
            else:
                print('Warning: we are getting data from the wrong source')

            self.page_num += 1

        # Check for empty pages
        for page in self.pages:
            if page == []:
                print(f"There are no repos on this page: {self.pages.index(page)}")
                break

        # Extract repo names and forks
        repo_names = []
        forks = []
        for page in self.pages:
            for repo in page:
                try:
                    repo_names.append(repo['full_name'].split("/")[1])
                    forks.append(repo['forks'])
                except:
                    pass

        # Create dataframe to store the data
        repo_data = pd.DataFrame()
        repo_data['name'] = repo_names
        repo_data['number_of_forks'] = forks
        print("------")
        return repo_data

    # Customer duplicate checker
    @staticmethod
    def duplicate_checker(dataframe):
        # Check for duplicate entries in the dataframe
        def has_duplicates(values):
            if len(values) != len(set(values)):
                return True
            else:
                return False

        if has_duplicates(dataframe['name']):
            duplicate_in_coin = dataframe.duplicated(subset=['name'])
            if duplicate_in_coin.any():
                dataframe = dataframe.loc[~duplicate_in_coin].reset_index(drop=True)
        return dataframe

    @staticmethod
    def export_to_csv(dataframe, filename):
        # Export dataframe to a CSV file
        dataframe.to_csv(filename, index=False)

    def scrape_and_export(self, filename):
        # Scrape GitHub data, remove duplicates, and export to CSV
        df = self.scrape_github_data()
        df = self.duplicate_checker(df)
        self.export_to_csv(df, filename)

scraper = GitHubScraper(user_account='bounceapp', github_token='xxxxxx')
scraper.scrape_and_export('data/github_data.csv')

scraper.scrape_github_data()