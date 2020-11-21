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
The American Association of University Women (AAUW) states that women earn substantially less than men when measured by median income. They mention legal concerns, differing gender distributions by industry, and differences in regional attitude as factors that contribute to a wage gap. [AAUW](https://www.aauw.org/resources/research/simple-truth/)

The General Social Survey (GSS) collects American socioeconomic data, including public opinions related to society. It has been conducted since 1972 by the University of Chicago with the goal of providing insight into social trends that is easily accessible to those who may be interested. [GSS](http://www.gss.norc.org/About-The-GSS)
'''

# clean data for grouped plots
groups = ['sex','region','education']
questions = ['satjob','relationship','male_breadwinner','men_bettersuited','child_suffer','men_overwork']

gss_clean.male_breadwinner = gss_clean.male_breadwinner.astype('category')
gss_clean.male_breadwinner = gss_clean.male_breadwinner.cat.reorder_categories(['strongly disagree',
                                                       'disagree',
                                                       'agree',
                                                       'strongly agree'])
gss_clean.relationship = gss_clean.relationship.astype('category')
gss_clean.relationship = gss_clean.relationship.cat.reorder_categories(['strongly disagree',
                                                       'disagree',
                                                       'agree',
                                                       'strongly agree'])
gss_clean.child_suffer = gss_clean.child_suffer.astype('category')
gss_clean.child_suffer = gss_clean.child_suffer.cat.reorder_categories(['strongly disagree',
                                                       'disagree',
                                                       'agree',
                                                       'strongly agree'])
gss_clean.men_overwork = gss_clean.men_overwork.astype('category')
gss_clean.men_overwork = gss_clean.men_overwork.cat.reorder_categories(['strongly disagree',
                                                       'disagree',
                                                       'neither agree nor disagree',
                                                       'agree',
                                                       'strongly agree'])

gss_clean.men_bettersuited = gss_clean.men_bettersuited.astype('category')
gss_clean.men_bettersuited = gss_clean.men_bettersuited.cat.reorder_categories(['disagree','agree'])

gss_clean.satjob = gss_clean.satjob.astype('category')
gss_clean.satjob = gss_clean.satjob.cat.reorder_categories(['very dissatisfied',
                                                           'a little dissat',
                                                           'mod. satisfied',
                                                           'very satisfied'])

# set colors
bcg = 'mintcream'
alt1 = 'darkseagreen'
alt2 = 'ivory'
alt_txt = 'white'


# table
tabs = gss_clean.groupby('sex').agg({'income':'mean','job_prestige':'mean','socioeconomic_index':'mean', 'education':'mean'}).round(2)
tabs = tabs.reset_index().rename(columns={'job_prestige':'Occupational Prestige',
                                   'socioeconomic_index':'Socioeconomic Index',
                                  'income':'Income',
                                  'education':'Education',
                                  'sex':'Sex'})
table = ff.create_table(tabs, colorscale=[alt1,alt2,bcg])
table.update_layout(height=180, width=800,
                   paper_bgcolor=alt1,
                   plot_bgcolor=alt1)

# barplot
gss_clean.male_breadwinner = gss_clean.male_breadwinner.astype('category')
gss_clean.male_breadwinner = gss_clean.male_breadwinner.cat.reorder_categories(['strongly disagree',
                                                                               'disagree',
                                                                               'agree',
                                                                               'strongly agree'])
bars = gss_clean.groupby(['sex','male_breadwinner']).size().reset_index().rename(columns={0:'count'})
barplot = px.bar(bars, x='male_breadwinner', y='count', color='sex', barmode='group',
                 labels={'count':'Count', 'male_breadwinner':'Response', 'sex':'Sex'}) 
barplot.update_layout(height=400, width=600,
                     paper_bgcolor=alt1,
                      plot_bgcolor=bcg,
                     font={'color':alt_txt})

# scatter plot
fig_scatter = px.scatter(gss_clean, x='job_prestige', y='income', color='sex', 
                         hover_data=['education','socioeconomic_index'],
                         trendline='ols',
                         labels={'income':'Income', 'job_prestige':'Occupational Prestige', 'sex':'Sex'})
fig_scatter.update_layout(height=600, width=800,
                         paper_bgcolor=alt1,
                         plot_bgcolor=bcg,
                         font={'color':alt_txt})

# first boxplot
box1 = px.box(gss_clean, x='income', y='sex', color='sex',
             labels={'income':'Income', 'sex':'Sex'})
box1.update_layout(showlegend=False,
                   height=350, width=600,
                   paper_bgcolor=alt1,
                   plot_bgcolor=bcg,
                   font={'color':alt_txt})

# second boxplot
box2 = px.box(gss_clean, x='job_prestige', y='sex', color='sex',
             labels={'job_prestige':'Occupational Prestige', 'sex':'Sex'})
box2.update_layout(showlegend=False,
                   height=350, width=600,
                   paper_bgcolor=alt1,
                   plot_bgcolor=bcg,
                   font={'color':alt_txt})

# boxplot grid
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
boxes.update_layout(showlegend=False,
                   height=750, width=800,
                   paper_bgcolor=alt1,
                   plot_bgcolor=bcg,
                   font={'color':alt_txt})


# build dashboard
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1('Understanding the Gender Wage Gap'),
        html.Div([
            dcc.Markdown(children = md_txt, style={'color':alt_txt})
        ], style={'backgroundColor':alt1}),
        html.H2('Average Results by Gender'),
        dcc.Graph(figure=table),
        html.H2('Responses to Survey Questions'),
        html.Div([
            html.Div([
                html.H4('Question'),
                dcc.Dropdown(id='question',
                            options=[{'label': i, 'value': i} for i in questions],
                            value='male_breadwinner'
                            ),
                html.H4('Grouping'),
                dcc.Dropdown(id='color',
                            options=[{'label': i, 'value': i} for i in groups],
                            value='sex'
                            )
            ], style={'width': '25%', 'float': 'left'}),
            html.Div([
                dcc.Graph(id='graph')
            ], style={'width': '70%', 'float': 'right', 'display':'inline-block'})
        ]),
        html.H2('Comparing Income and Job Prestige'),
        dcc.Graph(figure=fig_scatter),
        html.H2('Income by Sex'),
        dcc.Graph(figure=box1),
        html.H2('Occupational Prestige by Sex'),
        dcc.Graph(figure=box2),
        html.H2('Income by Prestige Categories'),
        dcc.Graph(figure=boxes)
    ],
    style={'backgroundColor':bcg}
)

@app.callback(Output(component_id='graph',component_property='figure'), 
             [Input(component_id='question',component_property='value'),
             Input(component_id='color',component_property='value')])

def make_figure(x, color):
    bars = gss_clean.groupby([color,x]).size().reset_index().rename(columns={0:'count'})
    barplot = px.bar(bars, x=x, y='count', color=color, barmode='group',
                         labels={'count':'Count', x:'Response'}) 
    barplot.update_layout(paper_bgcolor=alt1,
                         plot_bgcolor=bcg,
                         font={'color':alt_txt})
    return barplot

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
