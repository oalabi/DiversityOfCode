# DiversityOfCode
An interdisciplinary study observing conversations of diversity in technology through  a combination of close readings of individual texts; analytics including sentiment analysis, text clustering, and lexical analysis; and visualizations, we seek to reveal features of these texts’ vocabularies, rhetorical and affective strategies, and semantic patterns. We will remain alert to any evidence of potential conscious and unconscious bias, relationships, or patterns within and between the corpora on Twitter. 

# Original Source: https://github.com/Jefferson-Henrique/GetOldTweets-python

# Get and model relationships between Tweets and analyze the conversation of diversity in technology programatically, socially, and culturally

A project written in Python to get diversity tweets, using Jeffrey Henrique's GetTWeets API to bypass some limitations of Twitter Official API and obtain data on diversity conversations on Twitter both at a macro-level (e.g. hashtag/user analysis) as well as ona micro-level (e.g.text analyitics, contextualizing sarcasm in heated topics such as diversity, etc).


## Details
Twitter Official API has the bother limitation of time constraints, you can't get older tweets than a week. Some tools provide access to older tweets but in the most of them you have to spend some money before. We searched for tools to help and stumbled across Jefferson Henrique's workaround that tackled this problem directly. He has analyzed how Twitter Search through a browser works: basically when you enter on Twitter page a scroll loader starts; to obtain more tweets, you scroll down and tweets are fetched through calls to a JSON provider. We have modified this script to fetch and write certain key diversity terms:

terms = ['#girlswhocode', 'diversity in tech', 'minorities in tech', 'minority in tech', 'underrepresented in tech', 'diversity in computer science', 'tech women of color','diversity tech minority','diversity in technology', 'women in tech', 'LGBTQ in tech', 'technology blogger']



## Components 
** diversity_scraper.py **
To use this script, you can pass the folowing attributes:
    username: Username of a specific twitter account (without @)
    since: The lower bound date (yyyy-mm-dd)
    until: The upper bound date (yyyy-mm-dd)
    querysearch: query term unless default diversty query terms are preferred? ("'?'" for default diversity term search) 
    maxtweets: The maximum number of tweets to retrieve (default 10)
    accessmode: whether to append or overwrite the data/output file ("a" , "w+") (default "a")
       
    Examples:
    YOU MUST SPECIFY AN OUTPUT FILE! 
    # Example 1 - Get tweets by username [barackobama]
    python diversity_scraper.py --username 'barackobama' --maxtweets 1 --outputfile "barack.csv"\n

    # Example 2 - Get tweets by query search [europe refugees]
    python diversity_scraper.py --querysearch 'europe refugees' --maxtweets 1 --outputfile "barack.csv"\n

    # Example 3 - Get tweets by query search using default query terms
    python diversity_scraper.py --querysearch '*' --maxtweets 1 --outputfile "barack.csv"\n
     
    # Example 4 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
     python diversity_scraper.py --username 'barackobama' --since 2015-09-10 --until 2015-09-12 --maxtweets 1 --outputfile "barack.csv"
     
** associationmatrix.py**
To use this script, you need to specify the location of the csv file with the data generated using diversity_scraper.py
This script will build a data map that models unique word associations
    -i, --inputfile 
    -o, --outputfile
    -t, --tag-column
    -r, --retweet-count-column
            
    ** Example: **
    python relationmap.py -i inputfile.csv -o outputfile.json -c 8 -r 3
    
## GetTweets API
- **Tweet:** Model class to give some informations about a specific tweet.

- id (str)
  
- permalink (str)
  
- username (str)
  
- text (str)
  
- date (date)
  
- retweets (int)
  
- favorites (int)
  
- mentions (str)
  
- hashtags (str)
  
- geo (str)



- **TweetManager:** A manager class to help getting tweets in **Tweet**'s model.
  
- getTweets (**TwitterCriteria**): Return the list of tweets retrieved by using an instance of **TwitterCriteria**. 


- **TwitterCriteria:** A collection of search parameters to be used together with **TweetManager**.
  
- setUsername (str): An optional specific username from a twitter account. Without "@".
  
- setSince (str. "yyyy-mm-dd"): A lower bound date to restrict search.
  
- setUntil (str. "yyyy-mm-dd"): An upper bound date to restrist search.
  
- setQuerySearch (str): A query text to be matched.
  
- setMaxTweets (int): The maximum number of tweets to be retrieved. If this number is unsetted or lower than 1 all possible tweets will be retrieved.
  

- **Main:** Examples of how to use.


- **Exporter:** Export tweets to a csv file named "output_got.csv".



## Examples of python usage
- Get tweets by username

``` python
	
	tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
	
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	  
    
	print tweet.text
```    


- Get tweets by query search

``` python
	
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('europe refugees').setSince("2015-05-01").setUntil("2015-09-30").setMaxTweets(1)
	
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	  
    
	print tweet.text
```    


- Get tweets by username and bound dates

``` python
	
	tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2015-09-10").setUntil("2015-09-12").setMaxTweets(1)
	
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	  
    
	print tweet.text
```    



## Examples of command-line usage
- Get help use

```
    python Exporter.py -h
``` 


- Get tweets by username
```
    
	python Exporter.py --username 'barackobama' --maxtweets 1
```    

- Get tweets by query search

```
    python Exporter.py --querysearch 'europe refugees' --maxtweets 1
```    

- Get tweets by username and bound dates

```
    python Exporter.py --username 'barackobama' --since 2015-09-10 --until 2015-09-12 --maxtweets 1

