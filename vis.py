import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn

cols_use = ['case_id',
            'trade_nm',
            'legal_name',
            'street_addr_1_txt',
            'cty_nm',
            'st_cd',
            'zip_cd',
            'naic_cd',
            'naics_code_description',
            'case_violtn_cnt',
            'cmp_assd_cnt',
            'ee_violtd_cnt',
            'bw_atp_amt',
            'flsa_bw_atp_amt',
            'flsa_ee_atp_cnt',
            'flsa_mw_bw_atp_amt',
            'flsa_ot_bw_atp_amt',
            'flsa_15a3_bw_atp_amt',
            'flsa_cmp_assd_amt',
            'findings_start_date',
            'findings_end_date']

datadir = 'data'

judgements_files = 'SJOjudgements2-3.csv'
data_dic_file = 'whd_data_dictionary.csv'
whisard = 'whd_whisard.csv'

judgements = pd.read_csv(datadir + '/' + judgements_files)
data_dic = pd.read_csv(datadir + '/' + data_dic_file)
df_whiz = pd.read_csv(datadir + '/' + whisard)

df_zip = pd.read_csv('data/sandbox/zip_code_database_all_us.csv')

# join whisard and zip and save
# pd.merge(df_whiz, df_zip, left_on='zip_cd', right_on='zip').to_csv('data/processedWhdData/whd_whisard.joinedCounty.csv')

# processed data
df_whiz_zip = pd.read_csv('data/processedWhdData/whd_whisard.joinedCounty.csv', index_col=0)
# df_whiz_h = pd.read_csv('data/processedWhdData/whd_whisard.naicHumanReadableLevels.csv')


# convert to datetime
df_whiz_zip['findings_start_date'] = pd.to_datetime(df_whiz_zip[df_whiz_zip['findings_start_date']>'2000']['findings_start_date'])
df_whiz_zip['findings_end_date'] = pd.to_datetime(df_whiz_zip[df_whiz_zip['findings_end_date']>'2000']['findings_end_date'])

# get year
df_whiz_zip['findings_start_date_y'] = df_whiz_zip['findings_start_date'].apply(lambda x: x.year)
df_whiz_zip['findings_end_date_y'] = df_whiz_zip['findings_end_date'].apply(lambda x: x.year)

# county rank
year = 2010
county_rank = df_whiz_zip[df_whiz_zip['findings_start_date_y']==year].groupby(['state', 'county']).size().sort_values()
top10_counties = county_rank[:-10:-1]
top10_counties = top10_counties.reset_index()

df_demo = pd.read_csv('data/census/county_wide_demographic-%04d.csv' % year, index_col=0)

pd.merge(top10_counties, df_demo, left_on=['state', 'county'] , right_on=['STABNAME', 'CTYNAME'])

top10_demo = pd.merge(top10_counties, df_demo, left_on=['state', 'county'] , right_on=['STABNAME', 'CTYNAME']).set_index('county')

# visualize demographics for these counties
for cty in top10_demo.index:

    ax = top10_demo.loc[cty][5:17].plot.pie(figsize=(6,6), autopct='%.2f', labels=None, title=top10_demo.loc[cty]['state'] + ': ' + cty)
    ax.legend(loc=3, labels=top10_demo.columns[5:17])
    ax.set_ylabel('')
    plt.show()


# # visualize count of lvl2 naic description
# fig, ax = plt.subplots(figsize=(6,8))
# df_whiz_h.groupby('naic_description_lvl2').size().plot(kind='bar', ax=ax)
# fig.show()


# df_whiz_zip.groupby(['findings_start_date_y', 'st_cd']).size().plot()
df_whiz_zip.groupby(['findings_start_date_y']).size().plot()
plt.xlim([2007, 2016])
plt.show()


# df_whiz['findings_start_date'] = pd.to_datetime(df_whiz[df_whiz['findings_start_date']>'1900']['findings_start_date'])
# df_whiz['findings_end_date'] = pd.to_datetime(df_whiz[df_whiz['findings_end_date']>'1900']['findings_end_date'])

df_whiz_zip['findings_start_date_m'] = df_whiz_zip['findings_start_date'].apply(lambda x: x.month)
df_whiz_zip['findings_end_date_m'] = df_whiz_zip['findings_end_date'].apply(lambda x: x.month)

# df_ncases = pd.DataFrame(df_whiz.groupby(['findings_start_date_y', 'st_cd']).size())

df_whiz_zip.groupby(['findings_end_date_m']).size().plot()
plt.show()


states = df_whiz_zip['st_cd'].unique()[:-1]

cts_by_st_y = []
for st in states:
    df_whiz_zip[df_whiz_zip['st_cd'] == st].groupby('findings_start_date_y').size()
    df_tmp = pd.DataFrame(df_whiz_zip[df_whiz_zip['st_cd'] == st].groupby('findings_start_date_y').size())
    df_tmp.columns = [st]
    cts_by_st_y.append(df_tmp)


cts_by_st_y = pd.concat(cts_by_st_y, axis = 1)

states_vis = cts_by_st_y.max(axis=0).sort_values(ascending=False).iloc[:10].index

ax = cts_by_st_y[states_vis].plot()
ax.set_xlim([2000, 2016])
plt.show()

# load US census data to get population
popd = pd.read_csv('data/census/original/ST-EST00INT-ALLDATA.csv')
popd[(popd['SEX']==0) & (popd['ORIGIN']==0) & (popd['AGEGRP']==0) & (popd['RACE']==0)]

pop_states = popd[(popd['SEX']==0) & (popd['ORIGIN']==0) & (popd['AGEGRP']==0) & (popd['RACE']==0)]
pop_states_2000 = pop_states.iloc[1:]
pop_states_2000 = pop_states_2000[
    ['NAME', u'POPESTIMATE2000', u'POPESTIMATE2001',
     u'POPESTIMATE2002', u'POPESTIMATE2003', u'POPESTIMATE2004',
     u'POPESTIMATE2005', u'POPESTIMATE2006', u'POPESTIMATE2007',
     u'POPESTIMATE2008', u'POPESTIMATE2009', u'POPESTIMATE2010']]
pop_states_2000.index = pop_states_2000.NAME

popd = pd.read_csv('data/census/original/SC-EST2015-ALLDATA6.csv')

pop_states_2015 = popd[(popd['SEX']==0) & (popd['ORIGIN']==0)].groupby('NAME').sum()
pop_states_2015 = pop_states_2015.iloc[:, 9:]
pop_states_2015 = pop_states_2015[
    [u'POPESTIMATE2010', u'POPESTIMATE2011', u'POPESTIMATE2012',
     u'POPESTIMATE2013', u'POPESTIMATE2014', u'POPESTIMATE2015']]

pop_states = pd.concat([pop_states_2000.iloc[:,:-1], pop_states_2015], axis=1)
pop_states = pop_states.drop('NAME', axis=1)

st_abbrv = pd.read_csv('data/census/original/state_table.csv')
st_abbrv = st_abbrv.set_index('name')

# change index into abbreviation
pop_states.index = st_abbrv.loc[pop_states.index]['abbreviation']
pop_states.columns = range(2000, 2016)
pop_states.index = [u'AL', u'AK', u'AZ', u'AR', u'CA', u'CO', u'CT',
                    u'DE', 'DC', u'FL', u'GA', u'HI', u'ID', u'IL', u'IN', u'IA',
                    u'KS', u'KY', u'LA', u'ME', u'MD', u'MA', u'MI', u'MN', u'MS',
                    u'MO', u'MT', u'NE', u'NV', u'NH', u'NJ', u'NM', u'NY', u'NC',
                    u'ND', u'OH', u'OK', u'OR', u'PA', u'RI', u'SC', u'SD', u'TN',
                    u'TX', u'UT', u'VT', u'VA', u'WA', u'WV', u'WI', u'WY']


"""
AS - american samoa
GU - guam
MP - Northern Mariana Islands
PR - Puerto Rico
VI - US Virgin Island
"""

cts = cts_by_st_y.loc[range(2000, 2016)]
cts = cts.drop(['AS', 'GU', 'MP', 'PR'], axis=1)

# VI -> VA

for st in cts.columns:
    for yr in cts.index:
        cts[st][yr] /= pop_states[yr][st]


ax = cts[states_vis].plot()
ax.set_xlim([2000, 2016])
plt.show()


states_vis = cts.max(axis=0).sort_values(ascending=False).iloc[:10].index


print pd.concat([cts_by_st_y.max(axis=0).sort_values(ascending=False),
                 cts.max(axis=0).sort_values(ascending=False)], axis=1)

