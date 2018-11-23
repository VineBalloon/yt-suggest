# Youtube Suggestion Scraper
Simple script using python3.6 and bs4 to scrape a YouTube video's recommendations

May or may not break in the future if YouTube decides to update its css classes.

# Installation
## Virtual Environments
If you haven't already, make sure you use virtual environments (venv) to avoid
polluting your system python packages.
[Get started with venv](https://realpython.com/python-virtual-environments-a-primer/)

Once you have your venv setup, you can proceed with installing the requirements.

## Requirements
Requirements are Python3.6 and pip. The rest can be installed using 
`requirements.txt` and pip.

In the root directory, run
```pip3 install --user -r requirements.txt```

If you feel like you're too cool for venv, let me share a cautionary tale. A
friend of mine blasted every pip requirement he needed with `sudo` and somehow
ended up with a `pip3` that symlinked to `python2`.

They now know better than that.

-- 
Vincent Chen
vincentchen2.033@gmail.com 
