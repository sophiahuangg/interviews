# Interviews
This is the main repo we will use for the Lowe Institute's interview process for the automation team. You are expected to fork this repo and work on your own fork (or create your own and just keep this as a reference). The point of this assessment is to ensure that you can work with, or at least quickly learn, the basics of some packages you will be using a lot -- namely, `pandas`, `plotly`, and `requests` (for our actual work, we will be using `aiohttp` in conjunction with `asyncio`, but we will train you on those if necessary). We do not expect this to be an incredibly difficult or long task, and should be able to be completed in less than 3 hours.

# Installing Packages

The packages you need for this interview are `dotenv`, `plotly`, `pandas`, `requests`, and maybe `numpy`. To install them, run

```bash
pip install python-dotenv plotly pandas requests numpy
```

Note if you are using a computer with Apple silicon (M1 chip), the installation process will likely fail on `numpy` / `pandas` (as it requires `numpy`). If this happens, please reach out to Abhi (auppal22@cmc.edu).

You are permitted to use any other packages that do not violate the rules below as well.

# The Problem

You need to pull some data from [The Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/). Specifically, the series you need are the following:

- Quarterly Total Nonfarm Employment (ID [PAYEMS](https://fred.stlouisfed.org/series/PAYEMS#0)) from 2000 through 2020
- Quarterly Real Gross Domestic Product (ID [GDPC1](https://fred.stlouisfed.org/series/GDPC1)) from 2000 through 2020
- Quarterly Consumer Price Index (ID [CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL#0)) from 2000 through 2020

This data must be pulled from the [FRED API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html) using a programming language of your choice (**preferably Python** since that's what we mainly use, but any other language is acceptable for this interview as well). That is, you cannot download this data from FRED manually. You should follow the following workflow:

1. Fork this repository (or create a new one where you will work). If you create a new one, make sure to use the `python` format for `.gitignore`!
2. Get an API key from FRED -- instructions for this can be found [here](https://fred.stlouisfed.org/docs/api/api_key.html). You will need to sign up for a research account for FRED, in which you will also need to provide a reason for requesting an API key. Provide a reason along the lines of "I am writing an automated data pipeline for my school's research institute (the Lowe Institute of Political Economy), where we produce analyses that include some FRED data. This API key will be used for development and testing code prior to deployment." Do **NOT** use this wording exactly, but write something along these lines
3. Gather the above series from FRED using queries to their API. Documentation can be found [here](https://fred.stlouisfed.org/docs/api/fred/series_observations.html)
4. Join the series together into one dataframe and rename the columns into something meaningful (this can be done in either order)
5. Save this dataframe as a `.csv` file with an appropriate name
6. Plot two of these time series on the same plot, with time as the horizontal axis. Style the plot to your personal preference. You may need to use two separate y-axes (see https://www.originlab.com/doc/Origin-Help/Double-Y-Graph for an example)
7. Plot two of these series against each other in a scatterplot
8. Generate a histogram of one of the series
9. Save all plots as appropriately named `.png` files
10. Once these plots are completed, find two more series and pull them 
11. Plot these two series either (1) against each other in a scatterplot **OR** (2) together as one time series plot. Once again, style the plot to your personal preference. Once again, save this as a `.png` file
12. Email the link to your repo where you have produced this work **no later than 11:59pm on September 12th.** We will get back to you once all projects are submitted. Submit to auppal22@cmc.edu and bbenitez22@cmc.edu. In your submission, if it is not immediately obvious where the important files are (code and plots), let us know
13. If you also wish to be considered for the forecast team, please let us know in the same email you submit your project in. We need to know this ahead of time so we can adjust your interview accordingly

Remmeber, we are not necessarily testing your ability to perform all of these steps from memory. A lot of what we do depends on picking up new things quickly when we need to use them. Don't be afraid to consult Google or ask Abhi (auppal22@cmc.edu) or Bettina (bbenitez22@cmc.edu) for assistance at any step of the way. Part of what we want to see is how you handle problems you don't know the answer to -- it's better to ask 50 questions and turn in a finished final product than to ask none and turn in something unfinished!

# Rules

Some basic ground rules that must be established. We will not consider an application that violates these rules

1. No usage of a pre-built API wrapper built for FRED is allowed for any reason. This includes looking at any source code for said wrappers
2. No collaboration is permitted
3. If you get anything from online, cite it and explain what is happening at each step with comments. If we find plagiarized code that is completely uncommented, we will assume you do not actually understand what your code is doing.
4. Do not write your API key explicitly in any scripts. Instead, include your API key in a `.env` file and either source it in the shell you are running your script with before running it (via `source /path/to/file/.env`) or using the [`python-dotenv`](https://pypi.org/project/python-dotenv/) package. An example of how to use it is below.

The reason for the final rule is that our repositories are public -- we do not want API keys sitting out in the open. `.env` files are listed under our `.gitignore` file, so these files will not end up in any remote repository.

# Some Tips

1. You will be pulling multiple series. Any time you need to do something more than once, use or write a function for it! Bonus points for type hints and good documentation (docstrings and comments in the code)
2. Rather than hard-coding the URL in, use the `params` argument in `requests.get()`, which will form the URL for you (see example below -- or the [requests docs](https://docs.python-requests.org/en/master/user/quickstart/)).
3. You don't need to do anything super complicated -- remember that this is meant to test your core competencies, not if you can build a complex system from scratch. We do not need you to write a fully functioning API wrapper, just something that accomplishes this particular task.
4. If you are using Python, the only packages you should need are `pandas`, `plotly`, and `requests`. You will also need `load_dotenv()` from the `dotenv` package -- as shown above. You are welcome to use more libraries for plot styling or anything else (`seaborn` or `matplotlib`, for example) -- but that is up to your discretion
5. Style points matter in your plots! We are looking for, among other things, good data communication. Play around with the plot styling options for a bit (but don't stress it too much)! Our suggestion is to first always look for themes and/or templates that fit the style you're hoping to achieve
6. Comment, comment, comment -- code only you can understand is useless code
7. Along that line, try to make your code as readable as possible -- we do have to read it after all :)

Crude example of using `requests.get()` and `load_dotenv()`:

There needs to be a file in your root directory called `.env`. In it, have the following line:

```bash
Name_of_api_key_env_variable="EXAMPLEKEY123"
```

Now in your Python script, you can do:

```python
import os
import requests
from dotenv import load_dotenv, find_dotenv

def req(value1: str, value2: str):

  payload = {'arg1': value1, 'arg2': value2}
  
  # Load in the environment variables
  
  path_to_dotenv = find_dotenv() # NOTE: You will likely not need to do this
  load_dotenv(path_to_dotenv) # NOTE: This often works without any arguments -- try that first
  
  apikey = os.environ.get("Name_of_api_key_env_variable", None) # Returns None if there is no variable with that name
  
  # Can add a try/except here with an assert to check if apikey is not None
  
  payload["key"] = apikey
  
  r = requests.get('https://httpbin.org/get', params=payload)
  
  # This will send a GET request to
  # https://httpbin.org/get?arg1=value1&arg2=value2&key=149EXAMPLEKEY1023
  
  return r.json()
```
