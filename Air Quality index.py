#!/usr/bin/env python
# coding: utf-8

# pandas (import pandas as pd): Pandas is a powerful library for data manipulation and analysis. It provides data structures like DataFrame for efficient data handling.
# 
# plotly.express (import plotly.express as px): Plotly Express is a high-level wrapper for Plotly that makes it easy to create various types of interactive plots with less code.
# 
# plotly.io (import plotly.io as pio): Plotly IO provides functions for working with the Plotly library, including setting default templates for plots.
# 
# plotly.graph_objects (import plotly.graph_objects as go): Plotly Graph Objects is a lower-level interface for creating more customized and complex plots compared to Plotly Express.
# 
# pio.templates.default = "plotly_white": This line sets the default template for Plotly plots to use a white background. Plotly provides various templates (e.g., "plotly_dark", "plotly_white", etc.) that you can choose based on your preference.

# In[1]:


import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default ="plotly_white"


# In[2]:


data =pd.read_csv("C:\\Users\\User\\Downloads\\delhiaqi.csv")
print(data.head())


# In[3]:


data['date'] =pd.to_datetime(data['date'])


# The describe() function returns a DataFrame that includes statistics such as count, mean, std (standard deviation), min, 25%, 50%, 75%, and max for each numerical column in the original DataFrame.

# In[4]:


print(data.describe())


# Now let’s have a look at the intensity of each pollutant over time in the air quality:

# In[5]:


#time series plot for each air poulluant
fig =go.Figure()
for pollutant in ['co','no','no2','o3','so2','pm2_5','pm10','nh3']:
    fig.add_trace(go.Scatter(x=data['date'],y=data[pollutant],mode ='lines',name =pollutant))
fig.update_layout(title ="time series analysis air pollutant",xaxis_title="date",yaxis_title="ug/m^3")
fig.show()


# Now, before moving forward, we need to calculate the air quality index and its category. AQI is typically computed based on the concentration of various pollutants, and each pollutant has its sub-index. Here’s how we can calculate AQI:

# In[6]:


#define AQi breakpoint and corresponding aqi values
aqi_breakpoints = [
    (0, 12.0, 50), (12.1, 35.4, 100), (35.5, 55.4, 150),
    (55.5, 150.4, 200), (150.5, 250.4, 300), (250.5, 350.4, 400),
    (350.5, 500.4, 500)
]

def calculate_aqi(pollutant_name, concentration):
    for low, high, aqi in aqi_breakpoints:
        if low <= concentration <= high:
            return aqi
    return None

def calculate_overall_aqi(row):
    aqi_values = []
    pollutants = ['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']
    for pollutant in pollutants:
        aqi = calculate_aqi(pollutant, row[pollutant])
        if aqi is not None:
            aqi_values.append(aqi)
    return max(aqi_values)

# Calculate AQI for each row
data['AQI'] = data.apply(calculate_overall_aqi, axis=1)

# Define AQI categories
aqi_categories = [
    (0, 50, 'Good'), (51, 100, 'Moderate'), (101, 150, 'Unhealthy for Sensitive Groups'),
    (151, 200, 'Unhealthy'), (201, 300, 'Very Unhealthy'), (301, 500, 'Hazardous')
]

def categorize_aqi(aqi_value):
    for low, high, category in aqi_categories:
        if low <= aqi_value <= high:
            return category
    return None

# Categorize AQI
data['AQI Category'] = data['AQI'].apply(categorize_aqi)
print(data.head())


# Now, let’s have a look at the AQI of Delhi in January:

# 

# In[7]:


#aqi over time
fig =px.bar(data,x='date',y='AQI',title='AQi of delhi in jan')
fig.update_xaxes(title ='Date')
fig.update_yaxes(title ='AQI')
fig.show()


# In[8]:


fig =px.histogram(data,x='date',color='AQI Category',title='AQi of delhi in jan')
fig.update_xaxes(title ='Date')
fig.update_yaxes(title ='count')
fig.show()


# pollutant_colors = px.colors.qualitative.Plotly is used to assign a qualitative color palette from Plotly to the variable pollutant_colors. This palette is then used in your plot to specify the colors of different categories.

# In[9]:


# define poullant  and their color
pollutants = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
pollutant_colors = px.colors.qualitative.Plotly
# caL the sum of pollutant concentration
total_con=data[pollutants].sum()
#create a dataframe for the concentation
con_data=pd.DataFrame({"Pollutant":pollutants,"Concentration":total_con})

 #Create a donut plot for pollutant concentrations
fig = px.pie(con_data, names="Pollutant", values="Concentration",
             title="Pollutant Concentrations in Delhi",
             hole=0.4, color_discrete_sequence=pollutant_colors)

# Update layout for the donut plot
fig.update_traces(textinfo="percent+label")
fig.update_layout(legend_title="Pollutant")

# Show the donut plot
fig.show()
print(data.head())


# The corr() method calculates the Pearson correlation coefficient between each pair of columns in the DataFrame data[pollutants], where pollutants is a list of column names representing different pollutants.
# 
# The formula for the Pearson correlation coefficient between two variables, X and Y, is given by:
# 
# r=(X1-)

# In[10]:


corr_matrix= data[pollutants].corr()
fig=px.imshow(corr_matrix,x=pollutants,y=pollutants,title ='correlaation between pollutants')
fig.show()


# pd.to_datetime(data['date']). The dt.hour part extracts the hour component from each datetime in the series.
# 
# Here's a breakdown:
# 
# pd.to_datetime(data['date']): Converts the 'date' column in your DataFrame to a datetime format.
# .dt.hour: Accesses the hour component of each datetime in the resulting datetime series.
# 
# 
# This line groups your DataFrame by the 'hour' column and calculates the mean (average) AQI for each hour. The result is stored in a new DataFrame called hourly_avg_aqi. The reset_index() is used to convert the grouped result back to a DataFrame and reset the index, so 'hour' becomes a regular column again.

# In[11]:


#extract the hour from the date
data['hour'] =pd.to_datetime(data['date']).dt.hour

#cal hourly aver AQI
hourly_avg_aqi = data.groupby('hour')['AQI'].mean().reset_index()
fig =px.line(hourly_avg_aqi,x='hour',y='AQI',title="hourly Avg aqi trend")
fig.update_layout(xaxis_title="hour of day",yaxis_title='Average AQI')
fig.show()


# In[12]:


# Average AQI by Day of the Week
data['Day_of_Week'] = data['date'].dt.day_name()
average_aqi_by_day = data.groupby('Day_of_Week')['AQI'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
fig = px.bar(average_aqi_by_day, x=average_aqi_by_day.index, y='AQI', 
              title='Average AQI by Day of the Week')
fig.update_xaxes(title="Day of the Week")
fig.update_yaxes(title="Average AQI")
fig.show()


# In[ ]:





# In[ ]:




