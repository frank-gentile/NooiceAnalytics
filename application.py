#%%
from espn_api.basketball import League
import data_m
import create_plot
from formattingFuncs import getFantasyPoints, getPlayersFromTeam, getTeams, getPlayerData, formatLinks
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


league_id = 18927521
year = 2022
if year < 2021:
    league = League(league_id=league_id,year=year,espn_s2='AEAPjrqlooj6OgnN07vPsJ7L50zi%2BJG1a8cwJI7K2BHWJGlO6UGWK8BfZqdiRhNAnkIsIaar2V5q3Q9QpopVvceB2t31SL%2FiCYXV9TR3H5GsYcuJEBz1DgR%2Flr%2BthvC5eCrlMpfOumiIVtImkp3IckpszoXegoNjQQljM57oxQJuOohtsJ9APcughN7Vr8buD836WCUuRrGLjBVdds6Jp7wZKhFNKo%2FrM4vxLBR%2ByAqi5IAsWulvFjHVuzKMpjKE1B8d8J2A5sQfwYRR%2FUrpDSv0', swid='{0549A5F6-57A7-493C-ABAC-909FE5E8DB00}')
else:
    league = League(league_id=league_id,year=year)

scores = dict()
scores_against = dict()

scores, scores_against = data_m.findScores(league,scores,scores_against)

df, df_against, df_joined = data_m.createDataFrame(scores,scores_against)


df_p = data_m.CreatePValues(df_joined)

fig = create_plot.getLuckSkillPlot(df,df_against)

violin_fig = create_plot.getViolinPlots(df)

heat_map = create_plot.PlotlyHeatmap(df_p)

end_df = pd.read_csv('data.xlsx')
                

animations = {'Scatter':px.scatter(end_df,x='FP_avg',y='mins_avg',color='team',animation_frame='G',size='Points accumulated',range_y=[10,48],range_x=[0,50],hover_name='Player', size_max=45
),'Bar':px.bar(end_df,x='team',y='Points accumulated',color='team',animation_frame='G',animation_group='Player',hover_name='Player',range_y=[0,15000])}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
application = app.server
app.title = 'Nooice Analytics Dashboard'
app.layout = html.Div([

    html.H1("Nooice Analytics Dashboard"),
    html.P('''The following graph contains player level fantasy data, showing the average fantasy points per game against minutes per game over time, with 
    the size of the points indicating the total fantasy points accumulated. '''),
    html.P("Select an animation:"),
    dcc.RadioItems(
        id='selection',
        options=[{'label': x, 'value': x} for x in animations],
        value='Scatter'
    ),
    dcc.Graph(id="graph"),
    html.P('''This Violin Plot shows the normalized distribution of weekly scores. 'Normalized' meaning your score for the week minus the 
    average score of your opponents. Wider violins indicate greater frequency of the range, while thinner violins greater variation in scores.
    Points on each plot are considered outliers'''),
    dcc.Graph(id="violin"),
    html.P('''This 'Luck Plot' describes the normalized 'points for' vs normalized 'points against' Each quadrant qualifies wins and losses
    as 'lucky' or 'unlucky' and 'good' or 'bad' '''),
    dcc.Graph(id="luck"),
    html.P('''This heatmap describes the p-value associated with a simple t-test with the null nypothesis that team2 > team1. For example, 
    if the underlying p-value is <0.05 you can safely reject the null and imply that team1 is better than team2. '''),   
    dcc.Graph(id="heat"),
    html.P('''Presented by Frunk Analytics LLC'''),   


])
@app.callback(
    Output("graph", "figure"),
    Output("violin", "figure"),
    Output("luck", "figure"),
    Output("heat","figure"), 
    [Input("selection", "value")])
def display_animated_graph(s):
    return animations[s], violin_fig, fig, heat_map
if __name__ == '__main__':
    app.run_server(debug=True)