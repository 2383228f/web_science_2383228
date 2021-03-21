# web_science_2383228

How to run code:
All required code is included in the file: emotionCrawler.py.

To run code, simply open with an ide and select the run command, or use 'python run emotionCrawler' in the command line. The code is preset to search for 40 tweets using '#happiness', clean them and insert them into a MongoDB database on the localhost named emotions.happyTweets. 

There may be exceptions due to uninstalled components during the import phase, which can be resolved by runnning 'pip install' in terminal to download the missing components. MongoDB Compass is needed to run with the code, as this is where pymongo will send the twitter information.  

###########################

Once the code is run, new tweet entries will have been created in the MongoDB database referenced in the code. These entries will include
the cleaned text and label fields, along with all other tweet information that the Rest API provides. 

###########################

Data:
Stored in the 'data' folder are six .csv files, each containing the required information on a certain class of tweet. 
These are in the form: 

Clean (text field) | created_at | full_text (original tweet text) | label | crowd_label (crowdsourced label for subset of tweets)

As whitespace is preserved, to properly view the full_text column you may have to expand the height of the rows. 