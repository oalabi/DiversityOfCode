# Diversity in Coding: GetOldTweetsWrapper
import os
import sys, getopt

terms = ['#girlswhocode', 'diversity in tech', 'minorities in tech', 'minority in tech', 'underrepresented in tech', 'diversity in computer science', 'tech women of color','diversity tech minority','diversity in technology', 'women in tech', 'LGBTQ in tech', 'technology blogger']


def main(argv):
    if len(argv) == 0:
        print 'You must pass some parameters. Use \"-h\" to help.'
        return

    if len(argv) == 1 and argv[0] == '-h':
        print """\nTo use this script, you can pass the folowing attributes:
       username: Username of a specific twitter account (without @)
       since: The lower bound date (yyyy-mm-dd)
       until: The upper bound date (yyyy-mm-dd)
       querysearch: query term unless default diversty query terms are preferred? ("'?'" for default diversity term search) 
       maxtweets: The maximum number of tweets to retrieve (default 10)
       accessmode: whether to append or overwrite the data/output file ("a" , "w+") (default "a")
       
     \nExamples:
     YOU MUST SPECIFY AN OUTPUT FILE 
     # Example 1 - Get tweets by username [barackobama]
     python diversity_scraper.py --username 'barackobama' --maxtweets 1 --outputfile "barack.csv"\n

     # Example 2 - Get tweets by query search [europe refugees]
     python diversity_scraper.py --querysearch 'europe refugees' --maxtweets 1 --outputfile "barack.csv"\n

     # Example 3 - Get tweets by query search using default query terms
     python diversity_scraper.py --querysearch '*' --maxtweets 1 --outputfile "barack.csv"\n
     
     # Example 4 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
     python diversity_scraper.py --username 'barackobama' --since 2015-09-10 --until 2015-09-12 --maxtweets 1 --outputfile "barack.csv"\n"""
        return

    username = ""
    since = ""
    until = ""
    querySearch = "'?'"
    maxTweets = 10
    accessMode = "a" # default
    commandString = "Exporter.py"
    outfile = "data/output.csv"
    
    # get command line args to pass to Exporter.py
    try:
        opts, args = getopt.getopt(argv, "", ("username=", "since=", "until=", "querysearch=", "maxtweets=", "accessmode=", "outputfile="))
        
        for opt,arg in opts:
            if opt == '--username':
                username = arg
                commandString = commandString + (" --username %s" % username)
            elif opt == '--since':
                since = arg
                commandString = commandString + (" --since %s" % since)
            elif opt == '--until':
                until = arg
                commandString = commandString + (" --until %s" % until)
            elif opt == '--querysearch':
                querySearch = arg
                commandString = commandString + (" --querysearch ?")                
            elif opt == '--maxtweets':
                maxTweets = int(arg)
                commandString = commandString + (" --maxtweets %i" % maxTweets)
            elif opt == '--accessmode':
                accessMode = arg
                commandString = commandString + (" --accessmode %s" % accessMode)
            elif opt == '--outputfile':   
                outfile = arg
                commandString = commandString + (" --outputfile %s" % outfile)
        
        # Note:  if you select a accessmode that overwrites, you will lose the header in your final file
        
        outputFile = open(outfile, "w") 
        outputFile.write('sep=;\n searchterm;username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
        outputFile.close()
            
        print("QuerySearch: ", querySearch)
        
        if (querySearch == "'?'"):
            # cycle through diversity terms and write to file            
            for term in terms:
                newCommandString = commandString;
                print(newCommandString)
                try:
                    if "querysearch" in newCommandString:
                        newCommandString = newCommandString.replace("?",  ("\"" + term + "\"")) 
                    else:          
                        newCommandString = newCommandString + (" --querysearch %s" % ("\"" + term + "\"")) 
                except:
                    print("Error in how default query was specified")
                
                print("Passing command arguments: %s" % newCommandString)
                
                os.system(newCommandString)                      
        else:
            terms = querySearch.split(",")
            print("Terms: ", terms)
            for term in terms:                
                newCommandString = commandString.replace("?",  ("\"" + term + "\"")) 
                print("Passing command arguments: %s" % newCommandString)            
                os.system(newCommandString)                      

    except:
        e = sys.exc_info()[0]
        print( "Error: %s -> %s" % (e, commandString) )
        
if __name__ == '__main__':
    main(sys.argv[1:])   