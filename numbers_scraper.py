import re
import httplib
import urllib2
import requests
from bs4 import BeautifulSoup
import pylab
import pandas as pd
from scipy import stats

link = 'http://www.the-numbers.com/movie/budgets/all'
html = urllib2.urlopen(link)
soup = BeautifulSoup(html,'html5lib')
table = soup.find('table')
cats = table.find_all('tr')
a = cats[0]
data = []
entries = cats[1:]
for entry in entries:
	rows = entry.find_all('td')
	new = []
	for i in range(len(rows)):
		# number
		if i%6 == 0:
			new.append(int(rows[i].get_text()))
		# year
		if i%6 == 1:
			value = rows[i].get_text()
			j = value.rfind('/')
			new.append(int(value[j+1:]))
		# movie title
		if i%6 == 2:
			new.append(rows[i].get_text())
		# budget
		if i%6 == 3:
			value = rows[i].get_text()
			result = int(value.replace('$','').replace(',',''))
			new.append(result)
		# domestic box office
		if i%6 == 4:
			value = rows[i].get_text()
			result = int(value.replace('$','').replace(',',''))
			new.append(result)
		# worldwide box office
		if i%6 == 5:
			value = rows[i].get_text()
			result = int(value.replace('$','').replace(',',''))
			new.append(result)
	# skip null entries
	if len(new) >0:		
		data.append(new)
numbers = pd.DataFrame(data, columns=['number','date','movie','budget','domestic','worldwide'])
print numbers
numbers.to_pickle('the-numbers')