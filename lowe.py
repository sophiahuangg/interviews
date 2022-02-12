import pandas as pd,requests, plotly.graph_objects as go,  plotly.express as px, os
from dotenv import load_dotenv
from plotly.subplots import make_subplots


# Using requests library to create urls

def req(series: str, start: str, end: str, json: str): 
  '''
  {param} series: The series we are looking at (PAYEMS, GDPC1, and CPIAUCSL)
  {param} start: Observation start date (default: 1776-07-04)
  {param} end: Observation end date (default: 9999-12-31)
  {param} json: File type to send
  {type} str, str, str, str
  {return} Json file of what we get from using requests.get

  '''

  payload = {'series_id': series, 'observation_start': start, 'observation_end': end, 'file_type': json}
  load_dotenv() # Searches for .env file in root directory
  api_key = os.environ.get("Api_Key", None) # Extracting the API Key from the .env file, returns None if there is nothing with this name there
  payload["api_key"]=api_key

  r = requests.get('https://api.stlouisfed.org/fred/series/observations', params=payload) # Going to retrieve data from this command using the parameters specified above
  return r.json()
  
  
  
  
# Gathering series from FRED 

PAYEMS = req("PAYEMS","2000-01-01","2020-12-31", "json") # Calling function from above to create a url then json file with these parameters

GDPC1 = req("GDPC1", "2000-01-01", "2020-12-31","json") # Because we want to look at data from 2000 to 2020,
                                                        # I chose the range to be the first day of 2000 to the last day of 2020

CPIAUCSL=req("CPIAUCSL", "2000-01-01", "2020-12-31", "json")





# Joining the series together into one dataframe

df1 = pd.json_normalize(PAYEMS, record_path=['observations']) 
df1.rename(columns={'value':'Total Nonfarm Employment Value'}, inplace=True) # Source: https://www.geeksforgeeks.org/how-to-rename-columns-in-pandas-dataframe/


df2 = pd.json_normalize(GDPC1, record_path=['observations'])
df2.rename(columns={'value':'Real Gross Domestic Product Value'}, inplace=True)


df3 = pd.json_normalize(CPIAUCSL, record_path=['observations']) 
"""
Source: https://towardsdatascience.com/how-to-convert-json-into-a-pandas-dataframe-100b2ae1e0d8

Because the data frame had a nested list, I wanted to first extract the data from the "observations".
record_path=['observations'] tells me I'm looking into the observation column at the dictionary inside of it
The pd.json_normalize then takes the realtime_start, realtime_end, date, and value within each observation and creates a column for each
I decided not to set meta = anything because the observation start, end, and file type parameters were the same for the three and I didn't want to confuse the dates with the actual date.

"""
df3.rename(columns={'value':'Consumer Price Index Value'}, inplace=True) # Renaming "value" column to "Consumer Price Index Value" in my third dataframe so I know what I am working with

merged_df=pd.merge(df1, df3, how="outer") # Creating a new variable to store my joined first dataframe and second dataframe
merged_df1=pd.merge(merged_df, df2, how="outer") # Using the new variable I just created w/ my first and second dataframes to join it with my third dataframe
merged_df1.drop("realtime_start", axis=1, inplace=True)
merged_df1.drop("realtime_end", axis=1, inplace=True) # Deleting the columns named realtime_start and realtime_end since we don't need it, source: https://www.nbshare.io/notebook/199139718/How-To-Drop-One-Or-More-Columns-In-Pandas-Dataframe/





# Saving dataframe as a .csv file

merged_df1.to_csv(r"/Users/sophia/Desktop/Lowe/FRED_DF1.csv") # Source: https://stackoverflow.com/questions/16923281/writing-a-pandas-dataframe-to-csv-file
# Specifying which folder I want to place my csv file with the name "Data_FRED.csv" in





# Plotting two of the time series on the same plot, with time as the horizontal axis

df = pd.read_csv("/Users/sophia/Desktop/Lowe/FRED_DF1.csv") #Source: https://plotly.com/python/plot-data-from-csv/  
                                                             # Using pandas to read in the new csv I just created
fig=make_subplots(specs=[[{"secondary_y": True}]]) # Source: https://plotly.com/python/multiple-axes/#two-y-axes
# Indicating that we want two y-axes in our plot
fig.add_trace(
  go.Scatter(x=df["date"], y=df["Consumer Price Index Value"], name="Consumer Price Index", line=dict(color="rgb(160, 97, 119)")),
  secondary_y=False
) # Plotting this data using date and CPI, changing the line color, and signifying that this is not the one associated with our second y-axis
fig.add_trace(
  go.Scatter(x=df["date"], y=df["Total Nonfarm Employment Value"], name="Total Nonfarm Employment", line=dict(color="rgb(104, 133, 92)")), # Changing color of line, Source: https://stackoverflow.com/questions/58188816/plotly-how-to-set-line-color
  secondary_y=True
) # Adding this data to our plot and signifying that it is associated with our second y-axis

fig.update_xaxes(title_text="Year<br><br>Source: FRED Economic Research</sup>") # Creating X axis label, breaking to a new line, writing source
fig.update_yaxes(title_text="Consumer Price Index Value", secondary_y=False, linecolor="rgb(160, 97, 119)", title_font=dict(color="rgb(160, 97, 119)"), linewidth = 4.5) # Creating Y axis label for first variable and changing color/boldness of axis
fig.update_yaxes(title_text="Thousands of Persons", secondary_y=True, linecolor="rgb(104, 133, 92)", title_font=dict(color="rgb(104, 133, 92)"), linewidth = 4.5) # Creating Y axis label for second variable and changing color/boldness of axis

fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01),
    title_text="How CPI and Total Nonfarm Employment Change Over Time")
# Source: https://plotly.com/python/legend/
# Moving legend from the top rightt corner to the top left corner within the graph and creating a graph title
fig.update_xaxes(
    dtick="M24",
    tickformat="%B <br> %Y")
# Source: https://plotly.com/python/time-series/
# Changing x-axis tick labels, has a label for every 24 months and displays the month and the year
fig.show()





# Plotting a histogram

fig=px.histogram(df, x="date", y="Real Gross Domestic Product Value", nbins= 21, color_discrete_sequence=["darkseagreen"])
# Source: https://plotly.com/python/histograms/  
# Creating histogram from my dataframe (df), choosing number of bins I want in my histogram, setting color of bins to "darkseagreen"

fig.update_xaxes(showgrid=True, title_text="Date")
fig.update_yaxes(title_text="GDP in Billions of Chained 2012 Dollars")
fig.update_traces(marker_line_width=0.75,marker_line_color="white") # Source: https://stackoverflow.com/questions/67255139/how-to-change-the-edgecolor-of-an-histogram-in-plotly
# Creating a white border around the bins of my histogram to show each bin individually
fig.update_layout(title="GDP from 2000-2020")
fig.update_xaxes(
    dtick="M24",
    tickformat="%B <br> %Y")
fig.show()




# Plotting a scatterplot

fig=px.scatter(df, x=df["Total Nonfarm Employment Value"], y=df["Consumer Price Index Value"], color_discrete_sequence=["salmon"], title="CPI vs Nonfarm Employment Value")
# Creating a scatterplot through our dataframe with the x-axis data from Total Nonfarm Employment Value and the y-axis data from CPI
# Changing color of scatterplot points to be "salmon"
# Source: https://plotly.com/python/line-and-scatter/

fig.show()





# Pulling data from two more series

RPM = req("RAILPMD11","2000-01-01","2020-12-31", "json") # https://fred.stlouisfed.org/series/RAILPMD11

ARPM = req("AIRRPMTSID11","2000-01-01","2020-12-31", "json") # https://fred.stlouisfed.org/series/AIRRPMTSID11

df_2 = pd.json_normalize(RPM, record_path=['observations']) # Creating a new dataframe with ASM
print(df_2)
df_2.rename(columns={'value':'Rail Passenger Miles'}, inplace=True) 
df2_2=pd.json_normalize(ARPM, record_path=['observations']) # Creating a new dataframe with Vehicle Miles Traveled
df2_2.rename(columns={'value':'Air Revenue Passenger Miles'}, inplace=True)

merged_df2=pd.merge(df_2, df2_2, how="outer") # Merging the two new dataframes together, outer join to specify that if the dataframe has a missing value, it will put NaN instead of deleting the whole row
final_df=pd.merge(merged_df1, merged_df2, how="outer") # Joining the two dataframes made previously together to make one big dataframe with data from all of the series
final_df.drop("realtime_start", axis=1, inplace=True)
final_df.drop("realtime_end", axis=1, inplace=True)
final_df.to_csv(r"/Users/sophia/Desktop/Lowe/FULL_JOINED_DF.csv") # Saving the big dataframe as a CSV





# Plotting another time series plot

df = pd.read_csv("/Users/sophia/Desktop/Lowe/FULL_JOINED_DF.csv") #Source: https://plotly.com/python/plot-data-from-csv/  
                                                                  # Using pandas to read in the new csv I just created
fig=make_subplots(specs=[[{"secondary_y": True}]]) # Source: https://plotly.com/python/multiple-axes/#two-y-axes
fig.add_trace(
  go.Scatter(x=df["date"], y=df["Rail Passenger Miles"], name="Rail Passenger Miles", line=dict(color="rgb(128, 177, 211)")), # Changing color of line, Source: https://stackoverflow.com/questions/58188816/plotly-how-to-set-line-color
  secondary_y=False
) 
fig.add_trace(
  go.Scatter(x=df["date"], y=df["Air Revenue Passenger Miles"], name="Air Revenue Passenger Miles", line=dict(color="rgb(253, 180, 98)")), 
  secondary_y=True
) 

fig.update_xaxes(title_text="Year<br><br>Source: FRED Economic Research</sup>") # Creating X axis label, breaking to a new line, writing source
fig.update_yaxes(title_text="Number of Miles", secondary_y=False, linecolor="rgb(128, 177, 211)", title_font=dict(color="rgb(128, 177, 211)"), linewidth = 4.5) # Creating Y axis label for first variable and changing the color to match the line it corresponds to
fig.update_yaxes(title_text="Thousands of Passenger Miles", secondary_y=True, linecolor="rgb(253, 180, 98)", title_font=dict(color="rgb(253, 180, 98)"), linewidth = 4.5) # Creating Y axis label for second variable and changing the color to match the line it corresponds to

fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01),
    title_text="How Rail Passenger Miles and Air Revenue Passenger Miles Change Over Time"
) 
fig.update_xaxes(
    dtick="M24",
    tickformat="%B <br> %Y")

fig.show()


