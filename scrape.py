from formattingFuncs import getFantasyPoints, getPlayersFromTeam, getTeams, getPlayerData, formatLinks
import pandas as pd


teams = getTeams()
end_df = pd.DataFrame()
for team in teams:
    playerlist = getPlayersFromTeam(teams.index(team))
    links = formatLinks(playerlist,2022)
    for link in links:
        player_data, pic = getPlayerData(link)
        df = getFantasyPoints(player_data)
        df['cum_sum'] = df['FPoints'].cumsum()
        player_df = pd.DataFrame()
        player_df[playerlist[links.index(link)]]=df['cum_sum']
        #player_dict[]
        df3 = df.copy()
        df3['G'] = df['G'].replace('',float('NaN'))
        df3 = df3.dropna()
        df3['FP_avg'] = df3['cum_sum']/df3['G'].astype(int)
        df3['mins']=0
        for row in df3.index:
           mins = (int(df3['MP'][row].split(':')[0])*60+int(df3['MP'][row].split(':')[1]))/60
           df3.loc[row,'mins']=mins
        df3['cum_mins'] = df3['mins'].cumsum()
        df3['mins_avg'] = df3['cum_mins']/df3['G'].astype(int)

        #player_df['FP_avg']=df3['FP_avg']
        player_df = player_df.T
        player_df['team'] = team
        player_df.index.name = 'Player'
        player_df = player_df.reset_index()
        df4 = pd.melt(player_df,id_vars=['Player','team'],var_name='G',value_name='Points accumulated')
        df4['FP_avg'] = df3['FP_avg']
        df4['mins_avg'] = df3['mins_avg']
        end_df = end_df.append(df4)

end_df.to_excel('data.xlsx')