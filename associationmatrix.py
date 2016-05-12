# Build Word Relation Map
import sys, getopt, csv, json
import numpy as np
import itertools as it
from copy import deepcopy
from collections import Counter, OrderedDict
from pprint import pprint

def main(argv):
    inputfile = ""
    outputfile = "output_map.json"
    tag_column = 0
    retweet_count_column = 0
    
    if len(argv) == 0:
        print 'You must pass some parameters. Use \"-h\" to help.'
        return

    if len(argv) == 1 and argv[0] == '-h':
        print """\nTo use this script, you just need to specify the location of the csv file with your data
            This script will build a data map that models unique word associations
            -i, --inputfile 
            -o, --outputfile
            -t, --tag-column
            -r, --retweet-count-column
            
            \nExample:\n
            python relationmap.py -i inputfile.csv -o outputfile.json -c 8 -r 3 \n"""
        return
    
    try:
        opts, args = getopt.getopt(argv, "i:o:t:r:", ("inputfile=", "outputfile=", "tag-column=", "retweet-count-column="))
        
        for opt,arg in opts:
            if opt in ("-i", "--inputfile"):
                inputfile = arg
            elif opt in ("-o", "--outputfile"):
                outputfile = arg
            elif opt in ("-t", "--tag-column"):
                tag_column = int(arg)  
            elif opt in ("-r", "--retweet-count-column"):
                retweet_count_column = int(arg)       
            else:
                print("Command specified is not supported")
    except arg:
        print 'Arguments parse error, try -h' + arg
        
    try:
        # read csv
        # get entries for association matrix     
        uniqueItems = {} #term frequency
        column_info = ""
        
        with open(inputfile, 'rb') as f:
            delim = csv.Sniffer().sniff(f.read(1024), delimiters=";,")
            f.seek(0)
            reader = csv.reader(f, delim)           
            for row in reader:
                try:
                    if row[tag_column]:
                        column_info = row[tag_column]
                        retweets = row[retweet_count_column] #inconsistent way to find retweet column TODO: allow user to specify which column contains retweet number from command line
                        item_list = column_info.split(" ")                    
                        item_list = [item.lower() for item in item_list]
                        
                        for item in item_list:
                            if item in uniqueItems.keys():
                                uniqueItems[item] = uniqueItems[item] + max(1, int(retweets))
                            else:
                                uniqueItems[item] = max(1, int(retweets))
                except:
                    e = sys.exc_info()[1]
                    print("Error: %s" % e)
                    print("@ row %d  %s" % (sys.exc_info()[2].tb_lineno, row))
                    
        # build association matrix  
        num_unique_items = len(uniqueItems.keys())                                          
        uniqueItems_idx = {item.lower(): count for item, count in zip(uniqueItems.keys(), range(0, len(uniqueItems.keys())))}   # assign each item a numeric index
                                     
        # there may be a way to accomplish in one pass over the data, rather than two...this was coded for speed not efficiency                                     
        associationMatrix = np.zeros((num_unique_items, num_unique_items))
        item_list = []
        with open(inputfile, 'rb') as f:
            delim = csv.Sniffer().sniff(f.read(1024), delimiters=";,")
            f.seek(0)
            reader = csv.reader(f, delim) 
            for row in reader:
                try:
                    if row[tag_column]:
                        column_info = row[tag_column]
                        item_list = column_info.split(" ")
                        item_list = [item.lower() for item in item_list]
                        
                        i = j = uniqueItems_idx[item_list[0]]
                        # get all pairwise combinations of items
                        for pair in it.combinations(item_list, 2): 
                            i = uniqueItems_idx[pair[0]]                        
                            j = uniqueItems_idx[pair[1]]
                        
                        associationMatrix[i,j] = associationMatrix[i,j] + max(1, int(row[retweet_count_column]))
                        
                except:
                    e = sys.exc_info()[1]
                    print("Error: %s" % e)
                    print("@ row %d  %s" % (sys.exc_info()[2].tb_lineno, row))
    
        item_entry  = OrderedDict()
        item_entry["name"] =  ""                        # hashtag
        item_entry["degree"] =  0                       # number of other hashtags associated with name
        item_entry["associated_names"] =  []            # names of those hashtags
        item_entry["name_frequency"] =  0               # how frequently "name" occurs in the dataset
        item_entry["associated_name_frequencies"] =  [] # how frequently those hashtags occur in the dataset       
        
        itemAssociations = []
        for name in uniqueItems.keys():  
            new_item = deepcopy(item_entry)                  
            new_item["name"] = "diversity" + ("." + name) 
            new_item["name_frequency"] = uniqueItems[name]            
            itemAssociations.append(new_item)
        
        nz = np.nonzero(associationMatrix)
        x_idx = nz[0]
        y_idx = nz[1]      
        keys = uniqueItems.keys()
        
        for x, y  in zip( x_idx,  y_idx):
            item = keys[x]
            assoc_item = keys[y]
            freq = associationMatrix[x,y]
            
            entry = itemAssociations[x]
            entry["associated_names"].append("diversity." + assoc_item)  
            entry["associated_name_frequencies"].append(freq) # TODO: dirty
        
        for entry in itemAssociations:
            entry["degree"] = len(entry["associated_names"]) 
        
        # update         
        j = json.dumps(itemAssociations, indent=4)
        print(j)
        print("Writing to file %s" % outputfile)
        f = open(outputfile, 'w')
        print >> f, j
        f.close()
    except arg:
        e = sys.exc_info()[0]
        print( "Error: %s -> %s" % (e, commandString) )


if __name__ == "__main__":
    print("WORD RELATIONS:  ")
    main(sys.argv[1:])