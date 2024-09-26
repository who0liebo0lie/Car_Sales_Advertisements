#import libraris 
import pandas as pd 
import streamlit as st
import plotly.express as px
vehicles=pd.read_csv('./vehicles_us.csv')

# Data clearning
#check for duplicates
print(vehicles.duplicated().sum())
#check for empty cells 
print(vehicles.isna().sum())
#fill in empty values of object datatypes
vehicles['paint_color']=vehicles['paint_color'].fillna('NA')
#fill in empty values for float and object types
vehicles[['model_year', 'cylinders', 'odometer', 'is_4wd']]=vehicles[['model_year', 'cylinders', 'odometer', 'is_4wd']].fillna(0)
#turn float types to integers 
vehicles['model_year']=vehicles['model_year'].astype(int)
vehicles['cylinders']=vehicles['cylinders'].astype(int)
vehicles['is_4wd']=vehicles['is_4wd'].astype(int)
vehicles.head()
#fill in empty values for object data type
vehicles['paint_color']=vehicles['paint_color'].fillna('NA')
#check replacements successful 
print(vehicles.isna().sum())
#model column contains both the manufacturer and model information so split them into seperate columns to be able to evaluate. 
vehicles[['manufacturer', 'model']]=vehicles['model'].str.split(" ", n=1, expand=True)
#Convert date_posted to datetime datatype and extract year into a new column  
vehicles['date_posted']=pd.to_datetime(vehicles['date_posted']) 
vehicles['year_posted'] = vehicles['date_posted'].dt.year 
#create dataframe where missing model_year is excluded 
vehicles_edited=vehicles[vehicles['model_year'] !=0]
vehicles_edited['model_year'].min()
#calculate age of each car
vehicles_edited['age_of_car']=vehicles_edited['year_posted']-vehicles_edited['model_year']


# task 1 show your data
#Filter to find unique manufacturers
manufacturer_choice=vehicles['manufacturer'].unique()

#graphs from jupyter notebook 
#price distribution by manufacturer 
manufacturer_type=vehicles.groupby('manufacturer')['price'].sum().reset_index()
#representation of if a diesel or gas car sells faster 
gas_type=vehicles.groupby('fuel').agg({'days_listed':'median'})
#what is the most common color for an Acura 
visual=vehicles_edited.groupby(['manufacturer','paint_color'])['paint_color'].count()
visual.head()
# task 2 draw a plot


#plot vehicles types by manufacturer
st.header('Market Details for Used Cars')
st.write('Select the manufacturer from dopdown to filter data')
#create a drop down menu 
select_menu = st.selectbox('Select the manufacturer',manufacturer_choice)

#create a slider to select the year
min_year, max_year=int(vehicles['model_year'][vehicles['model_year'] != 0].min()), int(vehicles['model_year'].max())
year_range=st.slider('Choose beginning and ending years',value= (min_year, max_year), min_value=min_year, max_value=max_year)
year_range[0]
year_range[1]

user_year_range=list(range(year_range[0], year_range[1]+1))
vehicles_filtered=vehicles[(vehicles['manufacturer'] == select_menu) & (vehicles.model_year.isin(list(user_year_range)))]
st.table(vehicles_filtered)


st.header('Used Car Price Analysis')
st.write('Find which factors influence price the most:transmission, fuel, body type or running condition')
list_for_hist=['transmission', 'fuel', 'type', 'condition']
select_variable = st.selectbox('Select the factor to evaluate for price distribution', list_for_hist)

#create a figure
fig1 = px.histogram(vehicles, x='price', color=select_variable)
fig1.update_layout(title="<b> Price effect of {}<b>".format(select_variable))
st.plotly_chart(fig1)

def age_of_car(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-9'
    elif x>=10 and x<15: return '10-14'
    elif x>=15 and x<20: return '15-20'
    else: return '>20'

vehicles_edited['age_category']=vehicles_edited['age_of_car'].apply(age_of_car)

list_for_scatter = ['odometer', 'cylinders', 'condition'] 
choice_for_scatter = st.selectbox('Price dependency on', list_for_scatter)

fig2=px.scatter(vehicles_edited, x='price', y=choice_for_scatter, color='age_of_car')
fig2.update_layout(title="<b> Price effect of {}<b>".format(choice_for_scatter))

st.plotly_chart(fig2)
