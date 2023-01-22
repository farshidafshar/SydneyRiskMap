#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.simplefilter("ignore")
import pandas as pd
import numpy as np
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium


# In[2]:


df_geo=gpd.read_file('app_geo.json')


# In[3]:


df_model_result=pd.read_csv('model_results.csv')


# In[4]:


st.set_page_config(layout="wide")
st.markdown('Welcome To Sydney Safety RiskMap (SSR) Demo Webapp')
select_months_of_crash=st.sidebar.multiselect(label='CrashMonth',
                                              options=df_model_result['Month of crash'].unique().tolist(),
                                               default=df_model_result['Month of crash'].unique().tolist()
                                              , help='Choose Atleast One Month')

select_intervals_of_crash=st.sidebar.multiselect(label='CrashInterval',
                                              options=df_model_result['Two-hour intervals'].unique().tolist(),
                                               default=df_model_result['Two-hour intervals'].unique().tolist()
                                              , help='Choose Atleast One Interval')

#select_urbanisation_of_crash=st.sidebar.multiselect(label='UrbanisationArea',
#                                              options=df_model_result['Urbanisation'].unique().tolist(),
#                                               default=df_model_result['Urbanisation'].unique().tolist()
#                                              , help='Choose Atleast One Area')

select_day_name_of_crash=st.sidebar.multiselect(label='DayofWeek',
                                              options=df_model_result['Day of week of crash'].unique().tolist(),
                                               default=df_model_result['Day of week of crash'].unique().tolist()
                                              , help='Choose Atleast One Day')
selected_model = st.radio("Choose a Model",
                ('OrderedForest','ExtremelyRandomizedTrees'))
if selected_model=='OrderedForest':
    all_select_cols=['DepVar','Vul_user_presense' ,'Speed limit_num','NoInjury_OForest', 'MinorInjury_OForest', 'MajorInjury_Fatal_OForest',
                     'Street of crash']
else:
    all_select_cols=['DepVar','Vul_user_presense' ,'Speed limit_num','NoInjury_ERT', 'MinorInjury_ERT', 'MajorInjury_Fatal_ERT',
                     'Street of crash']


# In[5]:


df_pvt_show=df_model_result.loc[(df_model_result['Month of crash'].isin(select_months_of_crash)&
                                df_model_result['Two-hour intervals'].isin(select_intervals_of_crash)&
                                df_model_result['Day of week of crash'].isin(select_day_name_of_crash))] \
[all_select_cols].pivot_table(index=['Street of crash'], values=[t for t in all_select_cols if t!='Street of crash'],
                                             aggfunc='mean').reset_index()\
                                            .rename(columns={'Street of crash':"StreetName",
                                                             'Speed limit_num':'SpeedLimit',
                                                             'Vul_user_presense':'VulnerableUserPresense'})
p1=df_pvt_show.filter(regex='MajorInjury_Fatal').mean(axis=1)*3
p2=df_pvt_show.filter(regex='MinorInjury').mean(axis=1)*2
p3=df_pvt_show.filter(regex='NoInjury').mean(axis=1)*1

df_pvt_show['PredictedRisk']=(p1+p2+p3)/3
df_pvt_show['ActualRisk']=df_pvt_show['DepVar']/3
df_pvt_show['geometry']=df_pvt_show.StreetName.map(dict(zip(df_geo.StreetName,df_geo.geometry)))
gdf_show=gpd.GeoDataFrame(df_pvt_show[['StreetName','geometry','SpeedLimit','VulnerableUserPresense','PredictedRisk','ActualRisk']])            .set_crs('epsg:4326')


# In[6]:


start_point=[-33.7673779,150.9488911]


m_pred=gdf_show.dropna(subset=['geometry']).reset_index(drop=True).set_crs('epsg:4326').explore(column='PredictedRisk'
                                                                                           ,cmap='RdYlGn_r'
                                                                                           ,tiles='cartodbdark_matter')


# In[7]:


m_actl=gdf_show.dropna(subset=['geometry']).reset_index(drop=True).set_crs('epsg:4326').explore(column='ActualRisk'
                                                                                           ,cmap='RdYlGn_r'
                                                                                           ,tiles='cartodbdark_matter')


# In[8]:


col1, col2 = st.columns(2)
col1.header("Actual")
col2.header("Prediction")
with col1:
    st_folium(m_actl, width=2704)
with col2:
    st_folium(m_pred, width=2704)  

