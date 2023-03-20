#This tool is a Twitter scraper that allows users to input a Twitter username and select the number of tweets to scrape. 
#It provides three options for the amount of tweets to scrape: all tweets, the latest 100 tweets, or a custom number of tweets specified by the user. 
#It also allows users to input a filter for specific keywords or phrases to scrape.
#
#The tool uses the snscrape library to scrape tweets and stores the scraped data in a pandas DataFrame. 
#It then exports the data to a CSV file with the Twitter username as the filename. 
#The GUI includes a status label to update users on the progress of the scraping and a link label to provide a link to the latest scraped tweet. 
#The tool also includes a function to open the link in a web browser. The GUI is built with the tkinter library.
#
#to compile it in one file do:
#pyinstaller --onefile --hidden-import snscrape.modules SaS_on_Twitter.py
#
import tkinter as tk
import snscrape.modules
import snscrape.modules.twitter as sntwitter
import pandas as pd
import webbrowser


class TwitterScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Twitter Scraper")

        # Create username entry and label
        self.username_label = tk.Label(master, text="Enter Twitter username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        # Create filter entry and label
        self.filter_label = tk.Label(master, text="Enter filter (optional):")
        self.filter_label.pack()
        self.filter_entry = tk.Entry(master)
        self.filter_entry.pack()

        # Create amount options and label
        self.amount_label = tk.Label(master, text="Select number of tweets to scrape:")
        self.amount_label.pack()
        self.var = tk.StringVar(value="all")
        self.amount_radiobutton_all = tk.Radiobutton(master, text="All tweets", variable=self.var, value="all")
        self.amount_radiobutton_all.pack()
        self.amount_radiobutton_100 = tk.Radiobutton(master, text="100 tweets", variable=self.var, value="100")
        self.amount_radiobutton_100.pack()

        # Create custom amount entry
        self.custom_amount_entry = tk.Entry(master)
        self.custom_amount_entry.pack()

        # Create start button
        self.start_button = tk.Button(master, text="Start", command=self.start_scraping)
        self.start_button.pack()

        # Create status and link labels
        self.status_label = tk.Label(master, text="")
        self.status_label.pack()
        self.link_label = tk.Label(master, text="")
        self.link_label.pack()

    def start_scraping(self):
        # Get username, filter, and amount options
        username = self.username_entry.get()
        filter_query = self.filter_entry.get()
        amount = self.var.get()

        # Use custom amount entry if specified
        if self.custom_amount_entry.get():
            amount = int(self.custom_amount_entry.get())

        if amount == "all":
            amount = None

        # Create list to store tweet data
        tweets_list = []

        # Use TwitterSearchScraper to scrape data and append tweets to list
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"from:{username} {filter_query}").get_items()):
            if amount and i >= int(amount):
                break

            # Append tweet data to list
            tweets_list.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username, tweet.url])

            # Update status label with number of tweets scraped
            self.status_label.config(text=f"Scraped {i+1} tweets")

            # Update link label with link to latest scraped tweet
            self.link_label.config(text=tweet.url)
            self.link_label.bind("<Button-1>", lambda event, link=tweet.url: self.open_tweet_link(link))

            # Update GUI
            self.master.update()

        # Create DataFrame from tweet list
        tweets_df = pd.DataFrame(tweets_list, columns=["Datetime", "Tweet Id", "Text", "Username", "URL"])

        # Export DataFrame to CSV file
        tweets_df.to_csv(f"{username}_tweets.csv", index=False)

        # Update status label with scraping complete message
        self.status_label.config(text=f"Scraping complete: {len(tweets_list)} tweets scraped")

    def open_tweet_link(self, link):
        webbrowser.open(link)


if __name__ == "__main__":
    root = tk.Tk()
    gui = TwitterScraperGUI(root)
    root.mainloop()
