# coding=UTF-8
import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# Usage:news-json-converter.py news1 news2 ... 
def main():
    es = Elasticsearch()

    argumentNum = len(sys.argv)
    id_base = 0
    for idx, filename in enumerate(sys.argv):
        if (filename == 'news-json-converter.py'):
	    continue
	print(str(filename))
	fileptr = open(str(filename), 'r')
	#json_fileptr = open( str(filename)+'.json' , 'w')
	listOfjson = []

	for line in fileptr:
	    linelen = len(line)
	    MATCH_CHAR_NUM = 3

	    if '@GA' in line[0:MATCH_CHAR_NUM]:
	        #print('Start a record')
		    pass
	    elif '@U:' in line[0:MATCH_CHAR_NUM]:
	    	#print(line[MATCH_CHAR_NUM:linelen])
		    url = line[MATCH_CHAR_NUM:linelen]
	    elif '@T:' in line[0:MATCH_CHAR_NUM]:
	    	#print(line[MATCH_CHAR_NUM:linelen])
		    title = line[MATCH_CHAR_NUM:linelen]
	    elif '@B:' in line[0:MATCH_CHAR_NUM]:
	    	#print('Body start:\n')
		pass
	    else:
	        #print(line)
		    content = line
	        #title,url,content all ok
		oneRecord = [title, url, content]
		listOfjson.append(oneRecord)
		#listOfjson.append({'title':title, 'url':url, 'content':content})
	        #json.dump({'title':title, 'url':url, 'content':content}, json_fileptr)
		#Wrong format...
        #json.dump(listOfjson, json_fileptr)
	
	#Start elasticsearch bulk api : one file one bulk call
	recordNum = len(listOfjson)
	
        actions = [
	    {
	        "_index":"news",
	        "_type":"document",
	        "_id":i+id_base,
	        "_source": {
	            "title":listOfjson[i][0].decode('utf-8'),
		    "url":listOfjson[i][1].decode('utf-8'),
		    "content":listOfjson[i][2].decode('utf-8')
	        }
	    }
	    for i in range(0,recordNum)
	]
	helpers.bulk(es, actions)
	id_base+=recordNum
	
	fileptr.close()
	#json_fileptr.close()
	


if __name__ == '__main__':
    main()
