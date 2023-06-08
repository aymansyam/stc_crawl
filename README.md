# Scrapy Crawler Implementation

This crawler, written in Python using Scrapy framework, has 2 crawlers for stc.com.sa and for mewa.gov.sa.

mewa.gov.sa: the crawler will dump a list of html files to the root folder 
stc.com.sa: the crawler will grab a list of products for sale and output the names in a json file

To start the crawler, first install the dependencies using Pip:
``` 
$ pip install -r requirements.txt
```

Go to project directory (stc or mewa)
```
$ cd stc
```

Start the spider 

for mewa:
```
$ scrapy crawl general
```

for stc:
```
$ scrapy crawl products
```
For mewa, you will get the list of html files in mewa_dump at the root folder.

For stc, you will get a file called data.json at the project root which will have the scrapped data. You can change the output to any supported format by scrapy as such:

```
$ scrapy crawl products -O output.csv
```

This will output the file in csv format.

If you are getting any null items, increase sleep duration under selenium_get() method. Otherwise, you can decrease for better performance.