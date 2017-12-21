#2018

# Capstone code - for Campaign cycle 2018 
# Alice Topping
# Python Capstone Project

# outline


# house members data: name, ID, state, district 
# finance: total distributions
# district info: total members, total votes in last election?

import requests
import simplejson as json
import yaml
import pandas as pd
import csv
import plotly as plotly
import plotly.plotly as py
import plotly.graph_objs as go
import colorlover as cl

from capstone_code import members

def finance(fec_id):

	disbursements=[]

	data=[]

	for i in xrange(len(fec_id)):
		try:
			url= "https://api.propublica.org/campaign-finance/v1/2018/candidates/{}.json".format(fec_id[i])
			headers= {'X-API-Key':'API KEY'}
			f = requests.get(url,headers=headers).json()
			f1 = f['results'][0]
			#disbursements.append(f1["total_disbursements"])
			data.append(f1)
		except KeyError:
			continue 

		df= pd.DataFrame(data)

	df_sum = df.groupby('mailing_state', as_index=False)[['total_contributions']].sum().rename(columns={'mailing_state':'state','total_contributions' : 'total_contributions'})

	df_sum_pac = df.groupby('mailing_state', as_index=False)[['total_from_pacs']].sum().rename(columns={'mailing_state':'state','total_from_pacs' : 'total_from_pacs'})

	df_sum_ind = df.groupby('mailing_state', as_index=False)[['total_from_individuals']].sum().rename(columns={'mailing_state':'state','total_from_individuals' : 'total_from_individuals'})
	
	df_count = df.groupby('mailing_state', as_index=False)[['id']].count().rename(columns={'mailing_state':'state','id' : 'rep_count'})

	df_all= pd.merge(df_sum, df_count, on='state')

	df_all= pd.merge(df_all, df_sum_pac, on= 'state')

	df_all= pd.merge(df_all, df_sum_ind, on= 'state')

	df_all['average_contributions']= df_all['total_contributions'] / df_all['rep_count']

	df_all['average_pac'] = df_all['total_from_pacs'] / df_all['rep_count']

	df_all['average_ind'] = df_all['total_from_individuals'] / df_all['rep_count']

	df_all['pct_pac'] = (df_all['total_from_pacs'] / df_all['total_contributions']) * 100
 
	df_all= df_all.round(2)

	return df_all

def plot_2018(df_all):
	for col in df_all.columns:
		df_all[col] = df_all[col].astype(str)

	scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

	ryb = cl.scales['5']['div']['RdYlBu'];

	df_all['text'] = df_all['state'] + '<br>' +\
    'Number of Represetatives '+df_all['rep_count'] + '<br>'+\
    'Average Total Contribution '+df_all['average_contributions']

	data = [ dict(type='choropleth',
        colorscale = ryb,
        autocolorscale = False,
        locations = df_all['state'],
        z = df_all['average_contributions'].astype(float),
        locationmode = 'USA-states',
        text = df_all['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "USD")
        ) ]
	#print data
	layout = dict(
        title = 'Average total contribution to House candidates in 2018 election (Hover for breakdown)',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
	#print layout
	fig = dict( data=data, layout=layout )
	py.plot(fig, filename='US-rep-cloropleth-map')

def plot_pac_2018(df_all):
	for col in df_all.columns:
		df_all[col] = df_all[col].astype(str)

	scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
	ryb = cl.scales['5']['div']['RdYlBu'];

	df_all['text'] = df_all['state'] + '<br>' +\
    'Number of Represetatives '+df_all['rep_count'] + '<br>'+\
    'Average Total Contributions from PAC '+df_all['average_pac']

	data = [ dict(type='choropleth',
        colorscale = ryb,
        autocolorscale = False,
        locations = df_all['state'],
        z = df_all['average_pac'].astype(float),
        locationmode = 'USA-states',
        text = df_all['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "USD")
        ) ]
	#print data
	layout = dict(
        title = 'Average total contributions from Political Action Committee to House candidates in 2018 election (Hover for breakdown)',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
	#print layout
	fig = dict( data=data, layout=layout )
	py.plot(fig, filename='US-rep-PAC-cloropleth-map')

def plot_ind_2018(df_all):
	for col in df_all.columns:
		df_all[col] = df_all[col].astype(str)

	scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
	ryb = cl.scales['5']['div']['RdYlBu'];

	df_all['text'] = df_all['state'] + '<br>' +\
    'Number of Represetatives '+df_all['rep_count'] + '<br>'+\
    'Average Total Contributions from Individuals '+df_all['average_ind']

	data = [ dict(type='choropleth',
        colorscale = ryb,
        autocolorscale = False,
        locations = df_all['state'],
        z = df_all['average_ind'].astype(float),
        locationmode = 'USA-states',
        text = df_all['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "USD")
        ) ]
	#print data
	layout = dict(
        title = 'Average total contributions from individuals to House candidates in 2018 election (Hover for breakdown)',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
	#print layout
	fig = dict( data=data, layout=layout )
	py.plot(fig, filename='US-rep-ind-cloropleth-map')

def plot_pct_pac_2018(df_all):
	for col in df_all.columns:
		df_all[col] = df_all[col].astype(str)

	scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
	ryb = cl.scales['5']['div']['RdYlBu'];

	df_all['text'] = df_all['state'] + '<br>' +\
    'Number of Represetatives '+df_all['rep_count'] + '<br>'+\
    'Percentage of Total Contributions from PACs'+df_all['pct_pac']

	data = [ dict(type='choropleth',
        colorscale = ryb,
        autocolorscale = False,
        locations = df_all['state'],
        z = df_all['pct_pac'].astype(float),
        locationmode = 'USA-states',
        text = df_all['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "USD")
        ) ]
	#print data
	layout = dict(
        title = 'Percentage of total contributions from PACs to House candidates in 2018 election (Hover for breakdown)',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
	#print layout
	fig = dict( data=data, layout=layout )
	py.plot(fig, filename='US-rep-pct_pac-cloropleth-map')

if __name__=="__main__":
	fec_id= members()
	finance(fec_id)
	df_all= finance(fec_id)
	plot_2018(df_all)
	plot_pac_2018(df_all)
	plot_ind_2018(df_all)
	plot_pct_pac_2018(df_all)
