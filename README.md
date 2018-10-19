# search-engine
A basic search engine which performs crawling, indexing, retrival, ranking and error detection. Uses flask for hosting and scrapy for crawling.

This project is primarily in Python. It mentions 'Julia' in github code % as I have used .jl extension as an output file for scrapy.

## How to run:
To install scrapy and flask use:

`pip3 install scrapy`

`pip3 install flask`

I am using nltk library for Lemming.
To install nltk:

`pip3 install nltk`

You will have to install wordnet for Lemming.
Enter the code in the **python shell**:

`nltk.download('wordnet')`

I have provided many test links in .jl files.
To start crawling move to the **getLinks** directory and enter:

`scrapy crawl links -o outputfile.ext`

where ext is extension of your choice.

Similarly to index those directories use:

`scrapy crawl indexing`

**Note: In getLinks/getLinks/spiders/indexing.py change the file name in func getLinks() to one you want to index**

Once indexing is done you will get a data.csv file.
Now you can run a flask server inside **website/** dir.
To run a flask server use:

`export FLASK_APP=webQuery.py`

`flask run`

Just open the following link in a webbrowser to run the search-engine:

`http://127.0.0.1:5000/`