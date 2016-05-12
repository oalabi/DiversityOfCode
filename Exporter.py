import sys,getopt,got,datetime

def main(argv):

	if len(argv) == 0:
		print 'You must pass some parameters. Use \"-h\" to help.'
		return
		
	if len(argv) == 1 and argv[0] == '-h':
		print """\nTo use this jar, you can pass the folowing attributes:
    username: Username of a specific twitter account (without @)
       since: The lower bound date (yyyy-mm-aa)
       until: The upper bound date (yyyy-mm-aa)
 querysearch: A query text to be matched
   maxtweets: The maximum number of tweets to retrieve

 \nExamples:
 # Example 1 - Get tweets by username [barackobama]
 python Export.py --username 'barackobama' --maxtweets 1\n

 # Example 2 - Get tweets by query search [europe refugees]
 python Export.py --querysearch 'europe refugees' --maxtweets 1\n

 # Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
 python Export.py --username 'barackobama' --since 2015-09-10 --until 2015-09-12 --maxtweets 1\n"""
		return
	accessmode = "a+" # default
	outputfile = "data/output_got.csv" # default

	try:
		opts, args = getopt.getopt(argv, "", ("username=", "since=", "until=", "querysearch=", "maxtweets=", "accessmode=" , "outputfile="))
		print(opts)
		tweetCriteria = got.manager.TweetCriteria()
		
		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg
				
			elif opt == '--since':
				tweetCriteria.since = arg
				
			elif opt == '--until':
				tweetCriteria.until = arg
				
			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg
				
			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
                
			elif opt == '--accessmode':
				accessmode = arg
 
			elif opt == '--outputfile':
				outputfile = arg
		
		outputFile = open(outputfile, accessmode) 
		
		# outputFile.write('sep=;\n searchterm;username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
		
		print('----------------------------------------\nSearching for \'%s\'...\n' % tweetCriteria.querySearch)
		
		for t in got.manager.TweetManager.getTweets(tweetCriteria):
			outputFile.write('\n%s;%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (tweetCriteria.querySearch, t.username.encode(sys.stdout.encoding, 'replace'), t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text.encode(sys.stdout.encoding, 'replace'), t.geo, t.mentions, t.hashtags, t.id, t.permalink))
		
		outputFile.close()
		
		print("Done. Output in file %s." % outputfile)
		
	except arg:
		print 'Arguments parser error, try -h' + arg

if __name__ == '__main__':
	main(sys.argv[1:])