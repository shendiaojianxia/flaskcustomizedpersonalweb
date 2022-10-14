from itertools import combinations
import quopri
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request


#Create lists to store data
authors = []
quotes = []

url = 'https://quotes.thefamouspeople.com/think-52.php'
page = requests.get(url)

#parse the text from the web, give the datas to BeautifulSoup to analyze
soup = BeautifulSoup(page.text, 'html.parser')

#Get all quotes
quoteText = soup.find_all('p', attrs = {'class':'text_content'})
for i in quoteText:
    quote = (i.text.strip().split('\n')[0])  #Only want the quotes, not ""s or ,s
    quotes.append(quote)
    

#Get all authors
authorText = soup.find_all('a', attrs={'class':'authorname'})
for j in authorText:
    author = (j.text.strip().split('\n')[0])
    authors.append(author)

combine_list = []
for i in range(100):
    combine_list.append(quotes[i] + authors[i])

#df = pd.DataFrame(combine_list, columns=['Quotes', 'Authors'])
#df.to_csv('bestquotes.csv', index=False)

df = pd.DataFrame(zip(quotes, authors), columns=['Quotes','Authors'])
df.to_html('bestquotes.html', index=False)