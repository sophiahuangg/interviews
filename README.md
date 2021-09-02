# Interviews
This is the main repo we will use for the Lowe Institute's interview process for the automation team. You are expected to fork this repo and work on your own fork (or create your own and just keep this as a reference). The point of this assessment is to ensure that you can work with, or at least quickly learn, the basics of some packages you will be using a lot -- namely, `pandas`, `matplotlib.pyplot`, and `requests` (more accurately, we will be using `aiohttp` in conjunction with `asyncio`, but we will train you on those if necessary). We do not expect this to be an incredibly difficult or long task, and should be able to be completed in less than 3 hours.

# The Problem

You need to pull some data from [The Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/). Specifically, the series you need are the following:

- Quarterly Total Nonfarm Employment (ID [PAYEMS](https://fred.stlouisfed.org/series/PAYEMS#0)) from 2000 through 2020
- Real Gross Domestic Product (ID [GDPC1](https://fred.stlouisfed.org/series/GDPC1)) from 2000 through 2020
- Consumer Price Index (ID [CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL#0)) from 2000 through 2020

This data must be pulled from the [FRED API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html) using a programming language of your choice (preferably Python since that's what we mainly use, but any other language is acceptable for this interview as well). That is, you cannot download this data from FRED manually. You should follow the following workflow:

1. Get an API key from FRED -- instructions for this can be found [here](https://fred.stlouisfed.org/docs/api/api_key.html). You will need to sign up for a research account for FRED, in which you will also need to provide a reason for requesting an API key. Provide a reason along the lines of "I am writing an automated data pipeline for my school's research institute (the Lowe Institute of Political Economy), where we produce analyses that include some FRED data. This API key will be used for development and testing code prior to deployment." Do **NOT** use this wording exactly, but write something along these lines.
2. Gather the above series from FRED. Documentation can be found [here](https://fred.stlouisfed.org/docs/api/fred/series_observations.html)
3. Join the series together into one dataframe and rename the columns into something meaningful (this can be done in either order)
4. Save this dataframe as a `.csv` file with an appropriate name
5. Plot all three time series on the same plot, with time as the horizontal axis. Style the plot to your personal preference
6. Plot two of these series against each other in a scatterplot
7. Generate a histogram of one of the series
8. Save all plots as appropriately named `.png` files
9. Once these plots are completed, find two more series and pull them 
10. Plot these two series either (1) against each other in a scatterplot **OR** (2) together as one time series plot. Once again, style the plot to your personal preference. Once again, save this as a `.png` file.
11. Email the link to your repo where you have produced this work **no later than 11:59pm on September 12th.** We will get back to you once all projects are submitted

Remmeber, we are not necessarily testing your ability to perform all of these steps from memory. A lot of what we do depends on picking up new things quickly when we need to use them. Don't be afraid to consult Google or ask Abhi or Bettina for assistance at any step of the way. Part of what we want to see is how you handle problems you don't know the answer to -- it's better to ask 50 questions and turn in a finished final product than to ask none and turn in something unfinished!

# Rules

Some basic ground rules that must be established. We will not consider an application that violates these rules

1. No usage of a pre-built API wrapper built for FRED is allowed for any reason. This includes looking at any source code for said wrappers
2. No collaboration is permitted
3. If you get anything from online, cite it and explain what is happening at each step with comments. If we find plagiarized code that is completely uncommented, we will assume you do not actually understand what your code is doing.
4. Do not write your API key explicitly in any scripts. Instead, include your API key in a `.env` file and either source it in the shell you are running your script with before running it (via `source /path/to/file/.env`) or (preferably) using the [`python-dotenv`](https://pypi.org/project/python-dotenv/) package. An example of how to use it is below:

# Some Tips

1. You will be pulling multiple series. Any time you need to do something more than once, use or write a function for it! Bonus points for type hints
2. Rather than hard-coding the URL in, use the `params` argument in `requests.get()`, which will form the URL for you (see example below -- or the [requests docs](https://docs.python-requests.org/en/master/user/quickstart/)).
3. You don't need to do anything super complicated -- remember that this is meant to test your core competencies, not if you can build a complex system from scratch. We do not need you to write a fully functioning API wrapper, just something that accomplishes this task.
4. If you are using Python, the only packages you should need are `pandas`, `matplotlib.pyplot`, and `requests`. You will also need `load_dotenv()` from the `dotenv` package -- as shown above. You are welcome to use more libraries for plot styling or anything else (`seaborn`, for example) -- but that is up to your discretion
5. Style points matter in your plots! We are looking for, among other things, good data communication. Play around with the plot styling options for a bit!
6. Comment, comment, comment -- code means nothing if you can't understand it
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
