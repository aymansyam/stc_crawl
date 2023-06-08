# stc_crawl

To start the crawler, first install the dependencies using Pip:
``` 
$ pip install -r requirements.txt
```

Go to project directory
```
$ cd stc
```

Start the spider
```
$ scrapy crawl products
```

You will get a file called data.json at the project root which will have the scrapped data. You can change the output to any supported format by scrapy as such:

```
$ scrapy crawl products -O output.csv
```

This will output the file in csv format.

If you are getting any null items, increase sleep duration under selenium_get() method. Otherwise, you can decrease for better performance.