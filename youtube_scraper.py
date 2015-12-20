import time
import requests
import pandas as pd
#Country specific sales data for movies
sales = pd.read_pickle('wiki_movies8')

#Youtube founded in 2005, not used for movie trailers until 2006/2007
new = sales[sales['year']>=2007]

#insert your own API key
api_key = 'AIzaSyDj6AjmDI45iB9DdrQ-a4t3McMpMj0MdaI'

for i, row in new[:].iterrows():
	time.sleep(0.1)
	title = row['title']
	year = str(row['year'])[:4]
	print title, year
	#search for movie title + trailer eg. "Transformers trailer"
	#only include search results in or before year of release - promotional material
	a = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&q='+title+'+trailer&publishedBefore=' + year + '-12-31T00%3A00%3A00Z&type=video&key='+api_key)
	a = a.json()
	try:
		v_id = a['items'][0]['id']['videoId']
	# if trailer isn't found
	except Exception,e:
		print str(e)
		continue
	print a['items'][0]['snippet']['title'].encode('utf-8')
	#Viewership statistics
	b = requests.get('https://www.googleapis.com/youtube/v3/videos?part=statistics&id='+v_id+'&key='+api_key)
	b = b.json()
	try:
		print b['items'][0]['statistics']['viewCount'], 'views'
		sales.set_value(i,'Views',b['items'][0]['statistics']['viewCount']);
	# if trailer isn't found
	except Exception,e:
		print str(e)
		continue
	#Whether the content is licensed
	c = requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id='+v_id+'&key='+api_key)
	c = c.json()
	print 'licensed:', c['items'][0]['contentDetails']['licensedContent']
	if c['items'][0]['contentDetails']['licensedContent'] == 'True':
		sales.set_value(i,'licensed',True);
	else:
		sales.set_value(i,'licensed',False);
	print
sales.to_pickle('wiki_movies8')
