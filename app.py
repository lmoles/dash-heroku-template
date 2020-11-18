import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

md_txt = '''


The General Social Survey (GSS) collects American socioeconomic data, including public opinions related to society. It has been conducted since 1972 by the University of Chicago with the goal of providing insight into social trends that is easily accessible to those who may be interested. [GSS](http://www.gss.norc.org/About-The-GSS)
'''

tabs = gss_clean.groupby('sex').agg({'income':'mean','job_prestige':'mean','socioeconomic_index':'mean', 'education':'mean'}).round(2)
tabs = tabs.reset_index().rename(columns={'job_prestige':'Occupational Prestige',
                                   'socioeconomic_index':'Socioeconomic Index',
                                  'income':'Income',
                                  'education':'Education',
                                  'sex':'Sex'})
table = ff.create_table(tabs)

gss_clean.male_breadwinner = gss_clean.male_breadwinner.astype('category')
gss_clean.male_breadwinner = gss_clean.male_breadwinner.cat.reorder_categories(['strongly disagree',
                                                                               'disagree',
                                                                               'agree',
                                                                               'strongly agree'])
bars = gss_clean.groupby(['sex','male_breadwinner']).size().reset_index().rename(columns={0:'count'})
barplot = px.bar(bars, x='male_breadwinner', y='count', color='sex', barmode='group',
                 labels={'count':'Count', 'male_breadwinner':'Response', 'sex':'Sex'})

fig_scatter = px.scatter(gss_clean, x='job_prestige', y='income', color='sex', 
                         hover_data=['education','socioeconomic_index'],
                         trendline='ols',
                         labels={'income':'Income', 'job_prestige':'Occupational Prestige', 'sex':'Sex'})

box1 = px.box(gss_clean, x='income', y='sex', color='sex',
             labels={'income':'Income', 'sex':'Sex'})
box1.update_layout(showlegend=False)

box2 = px.box(gss_clean, x='job_prestige', y='sex', color='sex',
             labels={'job_prestige':'Occupational Prestige', 'sex':'Sex'})
box2.update_layout(showlegend=False)

gss2 = gss_clean[['income','sex','job_prestige']]
gss2['prestige_cat'] = pd.cut(gss2.job_prestige, bins=6, labels=['Very Low',
                                                                'Low',
                                                                'Medium-Low',
                                                                'Medium-High',
                                                                'High',
                                                                'Very High'])

gss2 = gss2.dropna()
boxes = px.box(gss2, 
             x='income', 
             y='sex',
             color='sex',
             facet_col='prestige_cat', 
             facet_col_wrap=2,
             category_orders={'prestige_cat':['Very Low',
                                            'Low',
                                            'Medium-Low',
                                            'Medium-High',
                                            'High',
                                            'Very High']},
              labels={'income':'Income', 'prestige_cat':'Occupational Prestige', 'sex':'Sex'})
boxes.update_layout(showlegend=False)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1('Understanding the Gender Wage Gap'),
        dcc.Markdown(children = md_txt),
        html.H2('Results by Gender'),
        dcc.Graph(figure=table),
        html.H2('Should Males be Providers?'),
        dcc.Graph(figure=barplot),
        html.H2('Comparing Income and Job Prestige'),
        dcc.Graph(figure=fig_scatter),
        html.H2('Income by Sex'),
        dcc.Graph(figure=box1),
        html.H2('Occupational Prestige by Sex'),
        dcc.Graph(figure=box2),
        html.H2('Income by Prestige Categories'),
        dcc.Graph(figure=boxes)
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
