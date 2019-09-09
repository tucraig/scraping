# scraping
Boilerplate Code / Tutorial for Web Scraping

Scraping is totally a trial and error process. It's best dealt in a case-by-case basis. I've included a few examples, though, that highlight different ways of scraping data from websites.

I've made it so all you have to do is download this repository as a zip, extract, and start coding. But that means you have to work from this directory, which isn't the best practice. You can follow along below if you want to install it on your machine.

# Installing Stuff
There are 2 components for web scraping: a process for getting the data from the web and a process for parsing it. Python is probably the easiest to understand so I'm going to use that today.The same concepts apply to other languages, though. And the two libraries I'll make use of are Requests and Beautiful Soup.

You'll need 4 things:
 - Python
 - Pip (Python Package/Module Manager)
 - Requests (Python Module)
 - BeautifulSoup4 (Python Module)
 
You can install everything super quickly:
```
python -m pip install requests bs4 lxml --user
```

# Finding Your Dataset
The world wide web is your oyster, I feel like you can make a dataset out of anything these days.

Some good ones include making requests to public APIs (Twitter, Spotify, Google, etc), websites with tables (Davidson, ESPN, etc), and websites with formatted information (NYTimes, Google Search, etc). But if it exists on the web, you can scrape it. Some pages are harder than others, but it can be done. Websites follow a similar structure to one anther, so feel free to follo this process and apply it to other websites that interest you.

I'm going to use ESPN, the Twitter API, and the Davidson Website as examples for this demo.

# The Setup
After you've got everything installed, make a directory to keep track of your things. If you download this repository it'll make a "scraping-master" directory, so I'll refer to everything in relation to that. Feel free to rename it, though.

Open terminal and enter the following:
```
cd $(find . -iname 'scraping-master')
```

The main file is going to be 'scraping.py'

# Actually Scraping
The are 3 elements of scraping: the url, the sauce, and the soup. The url is where you want to point Requests, it's where the data is stored on the web. The sauce is what's returned from requests -- it's the data, it just doesn't make sense yet. And then the soup is what you're after -- you're able to start to understand the data at this point.

You can edit the url to the page that has your data, and know that it's possible to nest request sessions within one another. You might make a script to go to one page and then open another and get more data from there. I've used this in paginated pages, or to access data that stems from a calendar.

## Step 1: the url
Go to the website with your source (ESPN) and navigate until you have the data on the screen. Copy that url and paste it into the code (in your url variable).
## Step 2: the sauce
This is what the website spits back at you. It's html, but not quite parsable. We pass this to bs4, though, and it gets parsed.
## Step 3: the soup
This is where we grab the information from. This is an object you can query. Some combination of find ("...":{"class":"..."}).get("...").
## Step 4: the output
Now that you've found the information you want, you can throw it out into a csv. You might write the file line by line based on table rows in the sauce, you could also pick up your own information from the website and throw that into a file.
