'''
This script creates the table output for average deficits, noninterest
spending, and revenues as a percent of GDP by party control.
'''

# Import packages
import numpy as np
import pandas as pd
import os
from scipy.stats import t as tdist
import statsmodels.api as sm

# Set paths to work across Mac/Windows/Linux platforms
cur_path = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(cur_path, 'data')
party_data_path = os.path.join(data_dir, 'deficit_party_data.csv')

'''
-------------------------------------------------------------------------------
Create pandas DataFrames and Column Data Source data objects
-------------------------------------------------------------------------------
'''

# Reading data from CVS (deficit_party_data.csv) and create two DataFrames for
# each time period
main_df = pd.read_csv(party_data_path,
                      dtype={'year': np.int64,
                             'deficit_gdp': np.float64,
                             'receipts_gdp': np.float64,
                             'spend_int_gdp': np.float64,
                             'spend_nonint_gdp': np.float64,
                             'spend_tot_gdp': np.float64,
                             'president': 'str',
                             'president_party': 'str',
                             'congress_number': np.int64,
                             'congress_session': np.int64,
                             'dem_whitehouse': np.int64,
                             'dem_senateseats': np.int64,
                             'rep_senateseats': np.int64,
                             'other_senateseats': np.int64,
                             'dem_senate_maj': np.int64,
                             'total_senateseats': np.int64,
                             'dem_houseseats': np.int64,
                             'rep_houseseats': np.int64,
                             'other_houseseats': np.int64,
                             'dem_house_maj': np.int64,
                             'total_houseseats': np.int64},
                      skiprows=3)
df_20 = main_df[(main_df['year'] >= 1947) & (main_df['year'] <= 2020)]
df_21 = main_df[(main_df['year'] >= 1947) & (main_df['year'] <= 2021)]

# Add 2021 forecast data to df_21 (from CBO July 2021 "Additional Information
# About the Updated Budget and Economic Outlook: 2021 to 2031")
df_21['deficit_gdp'].iloc[-1] = -13.406
df_21['receipts_gdp'].iloc[-1] = 17.15
df_21['spend_int_gdp'].iloc[-1] = 1.477
df_21['spend_nonint_gdp'].iloc[-1] = 21.703 + 7.377
df_21['spend_tot_gdp'].iloc[-1] = 1.477 + 21.703 + 7.377

'''
-------------------------------------------------------------------------------
Generate the table output from the dataframes
-------------------------------------------------------------------------------
'''
# Create Full control (WH + Sen + HouseRep) Republican control df for 1947-2020
cntrl_all_rep_20_df = \
    df_20[(df_20['president_party'] == 'Republican') &
          (df_20['dem_senate_maj'] == 0) &
          (df_20['dem_house_maj'] == 0)]

avg_def_gdp_all_rep_20 = cntrl_all_rep_20_df['deficit_gdp'].mean()
std_def_gdp_all_rep_20 = cntrl_all_rep_20_df['deficit_gdp'].std()
n_def_gdp_all_rep_20 = cntrl_all_rep_20_df['deficit_gdp'].count()

avg_nis_gdp_all_rep_20 = cntrl_all_rep_20_df['spend_nonint_gdp'].mean()
std_nis_gdp_all_rep_20 = cntrl_all_rep_20_df['spend_nonint_gdp'].std()
n_nis_gdp_all_rep_20 = cntrl_all_rep_20_df['spend_nonint_gdp'].count()

avg_rev_gdp_all_rep_20 = cntrl_all_rep_20_df['receipts_gdp'].mean()
std_rev_gdp_all_rep_20 = cntrl_all_rep_20_df['receipts_gdp'].std()
n_rev_gdp_all_rep_20 = cntrl_all_rep_20_df['receipts_gdp'].count()

# Create Full control (WH + Sen + HouseRep) Republican control df for 1947-2021
cntrl_all_rep_21_df = \
    df_21[(df_21['president_party'] == 'Republican') &
          (df_21['dem_senate_maj'] == 0) &
          (df_21['dem_house_maj'] == 0)]

avg_def_gdp_all_rep_21 = cntrl_all_rep_21_df['deficit_gdp'].mean()
std_def_gdp_all_rep_21 = cntrl_all_rep_21_df['deficit_gdp'].std()
n_def_gdp_all_rep_21 = cntrl_all_rep_21_df['deficit_gdp'].count()

avg_nis_gdp_all_rep_21 = cntrl_all_rep_21_df['spend_nonint_gdp'].mean()
std_nis_gdp_all_rep_21 = cntrl_all_rep_21_df['spend_nonint_gdp'].std()
n_nis_gdp_all_rep_21 = cntrl_all_rep_21_df['spend_nonint_gdp'].count()

avg_rev_gdp_all_rep_21 = cntrl_all_rep_21_df['receipts_gdp'].mean()
std_rev_gdp_all_rep_21 = cntrl_all_rep_21_df['receipts_gdp'].std()
n_rev_gdp_all_rep_21 = cntrl_all_rep_21_df['receipts_gdp'].count()

# Create Full control (WH + Sen + HouseRep) Democrat control df for 1947-2020
cntrl_all_dem_20_df = \
    df_20[(df_20['president_party'] == 'Democrat') &
          (df_20['dem_senate_maj'] == 1) &
          (df_20['dem_house_maj'] == 1)]

avg_def_gdp_all_dem_20 = cntrl_all_dem_20_df['deficit_gdp'].mean()
std_def_gdp_all_dem_20 = cntrl_all_dem_20_df['deficit_gdp'].std()
n_def_gdp_all_dem_20 = cntrl_all_dem_20_df['deficit_gdp'].count()

avg_nis_gdp_all_dem_20 = cntrl_all_dem_20_df['spend_nonint_gdp'].mean()
std_nis_gdp_all_dem_20 = cntrl_all_dem_20_df['spend_nonint_gdp'].std()
n_nis_gdp_all_dem_20 = cntrl_all_dem_20_df['spend_nonint_gdp'].count()

avg_rev_gdp_all_dem_20 = cntrl_all_dem_20_df['receipts_gdp'].mean()
std_rev_gdp_all_dem_20 = cntrl_all_dem_20_df['receipts_gdp'].std()
n_rev_gdp_all_dem_20 = cntrl_all_dem_20_df['receipts_gdp'].count()

# Create Full control (WH + Sen + HouseRep) Democrat control df for 1947-2021
cntrl_all_dem_21_df = \
    df_21[(df_21['president_party'] == 'Democrat') &
          (df_21['dem_senate_maj'] == 1) &
          (df_21['dem_house_maj'] == 1)]

avg_def_gdp_all_dem_21 = cntrl_all_dem_21_df['deficit_gdp'].mean()
std_def_gdp_all_dem_21 = cntrl_all_dem_21_df['deficit_gdp'].std()
n_def_gdp_all_dem_21 = cntrl_all_dem_21_df['deficit_gdp'].count()

avg_nis_gdp_all_dem_21 = cntrl_all_dem_21_df['spend_nonint_gdp'].mean()
std_nis_gdp_all_dem_21 = cntrl_all_dem_21_df['spend_nonint_gdp'].std()
n_nis_gdp_all_dem_21 = cntrl_all_dem_21_df['spend_nonint_gdp'].count()

avg_rev_gdp_all_dem_21 = cntrl_all_dem_21_df['receipts_gdp'].mean()
std_rev_gdp_all_dem_21 = cntrl_all_dem_21_df['receipts_gdp'].std()
n_rev_gdp_all_dem_21 = cntrl_all_dem_21_df['receipts_gdp'].count()

# Create Full control (WH + Sen + HouseRep) split control df for 1947-2020
cntrl_all_spl_20_df = \
    df_20[((df_20['president_party'] == 'Republican') &
           ((df_20['dem_senate_maj'] == 1) |
            (df_20['dem_house_maj'] == 1))) |
           ((df_20['president_party'] == 'Democrat') &
            ((df_20['dem_senate_maj'] == 0) |
             (df_20['dem_house_maj'] == 0)))]

avg_def_gdp_all_spl_20 = cntrl_all_spl_20_df['deficit_gdp'].mean()
std_def_gdp_all_spl_20 = cntrl_all_spl_20_df['deficit_gdp'].std()
n_def_gdp_all_spl_20 = cntrl_all_spl_20_df['deficit_gdp'].count()

avg_nis_gdp_all_spl_20 = cntrl_all_spl_20_df['spend_nonint_gdp'].mean()
std_nis_gdp_all_spl_20 = cntrl_all_spl_20_df['spend_nonint_gdp'].std()
n_nis_gdp_all_spl_20 = cntrl_all_spl_20_df['spend_nonint_gdp'].count()

avg_rev_gdp_all_spl_20 = cntrl_all_spl_20_df['receipts_gdp'].mean()
std_rev_gdp_all_spl_20 = cntrl_all_spl_20_df['receipts_gdp'].std()
n_rev_gdp_all_spl_20 = cntrl_all_spl_20_df['receipts_gdp'].count()

# Create Full control (WH + Sen + HouseRep) split control df for 1947-2021
cntrl_all_spl_21_df = \
    df_21[((df_21['president_party'] == 'Republican') &
           ((df_21['dem_senate_maj'] == 1) |
            (df_21['dem_house_maj'] == 1))) |
           ((df_21['president_party'] == 'Democrat') &
            ((df_21['dem_senate_maj'] == 0) |
             (df_21['dem_house_maj'] == 0)))]

avg_def_gdp_all_spl_21 = cntrl_all_spl_21_df['deficit_gdp'].mean()
std_def_gdp_all_spl_21 = cntrl_all_spl_21_df['deficit_gdp'].std()
n_def_gdp_all_spl_21 = cntrl_all_spl_21_df['deficit_gdp'].count()

avg_nis_gdp_all_spl_21 = cntrl_all_spl_21_df['spend_nonint_gdp'].mean()
std_nis_gdp_all_spl_21 = cntrl_all_spl_21_df['spend_nonint_gdp'].std()
n_nis_gdp_all_spl_21 = cntrl_all_spl_21_df['spend_nonint_gdp'].count()

avg_rev_gdp_all_spl_21 = cntrl_all_spl_21_df['receipts_gdp'].mean()
std_rev_gdp_all_spl_21 = cntrl_all_spl_21_df['receipts_gdp'].std()
n_rev_gdp_all_spl_21 = cntrl_all_spl_21_df['receipts_gdp'].count()

# Create Senate control (WH + Sen) Republican control df for 1947-2020
cntrl_whsen_rep_20_df = \
    df_20[(df_20['president_party'] == 'Republican') &
          (df_20['dem_senate_maj'] == 0)]

avg_def_gdp_whsen_rep_20 = cntrl_whsen_rep_20_df['deficit_gdp'].mean()
std_def_gdp_whsen_rep_20 = cntrl_whsen_rep_20_df['deficit_gdp'].std()
n_def_gdp_whsen_rep_20 = cntrl_whsen_rep_20_df['deficit_gdp'].count()

avg_nis_gdp_whsen_rep_20 = cntrl_whsen_rep_20_df['spend_nonint_gdp'].mean()
std_nis_gdp_whsen_rep_20 = cntrl_whsen_rep_20_df['spend_nonint_gdp'].std()
n_nis_gdp_whsen_rep_20 = cntrl_whsen_rep_20_df['spend_nonint_gdp'].count()

avg_rev_gdp_whsen_rep_20 = cntrl_whsen_rep_20_df['receipts_gdp'].mean()
std_rev_gdp_whsen_rep_20 = cntrl_whsen_rep_20_df['receipts_gdp'].std()
n_rev_gdp_whsen_rep_20 = cntrl_whsen_rep_20_df['receipts_gdp'].count()

# Create Senate control (WH + Sen) Republican control df for 1947-2021
cntrl_whsen_rep_21_df = \
    df_21[(df_21['president_party'] == 'Republican') &
          (df_21['dem_senate_maj'] == 0)]

avg_def_gdp_whsen_rep_21 = cntrl_whsen_rep_21_df['deficit_gdp'].mean()
std_def_gdp_whsen_rep_21 = cntrl_whsen_rep_21_df['deficit_gdp'].std()
n_def_gdp_whsen_rep_21 = cntrl_whsen_rep_21_df['deficit_gdp'].count()

avg_nis_gdp_whsen_rep_21 = cntrl_whsen_rep_21_df['spend_nonint_gdp'].mean()
std_nis_gdp_whsen_rep_21 = cntrl_whsen_rep_21_df['spend_nonint_gdp'].std()
n_nis_gdp_whsen_rep_21 = cntrl_whsen_rep_21_df['spend_nonint_gdp'].count()

avg_rev_gdp_whsen_rep_21 = cntrl_whsen_rep_21_df['receipts_gdp'].mean()
std_rev_gdp_whsen_rep_21 = cntrl_whsen_rep_21_df['receipts_gdp'].std()
n_rev_gdp_whsen_rep_21 = cntrl_whsen_rep_21_df['receipts_gdp'].count()

# Create Senate control (WH + Sen) Democrat control df for 1947-2020
cntrl_whsen_dem_20_df = \
    df_20[(df_20['president_party'] == 'Democrat') &
          (df_20['dem_senate_maj'] == 1)]

avg_def_gdp_whsen_dem_20 = cntrl_whsen_dem_20_df['deficit_gdp'].mean()
std_def_gdp_whsen_dem_20 = cntrl_whsen_dem_20_df['deficit_gdp'].std()
n_def_gdp_whsen_dem_20 = cntrl_whsen_dem_20_df['deficit_gdp'].count()

avg_nis_gdp_whsen_dem_20 = cntrl_whsen_dem_20_df['spend_nonint_gdp'].mean()
std_nis_gdp_whsen_dem_20 = cntrl_whsen_dem_20_df['spend_nonint_gdp'].std()
n_nis_gdp_whsen_dem_20 = cntrl_whsen_dem_20_df['spend_nonint_gdp'].count()

avg_rev_gdp_whsen_dem_20 = cntrl_whsen_dem_20_df['receipts_gdp'].mean()
std_rev_gdp_whsen_dem_20 = cntrl_whsen_dem_20_df['receipts_gdp'].std()
n_rev_gdp_whsen_dem_20 = cntrl_whsen_dem_20_df['receipts_gdp'].count()

# Create Senate control (WH + Sen) Democrat control df for 1947-2021
cntrl_whsen_dem_21_df = \
    df_21[(df_21['president_party'] == 'Democrat') &
          (df_21['dem_senate_maj'] == 1)]

avg_def_gdp_whsen_dem_21 = cntrl_whsen_dem_21_df['deficit_gdp'].mean()
std_def_gdp_whsen_dem_21 = cntrl_whsen_dem_21_df['deficit_gdp'].std()
n_def_gdp_whsen_dem_21 = cntrl_whsen_dem_21_df['deficit_gdp'].count()

avg_nis_gdp_whsen_dem_21 = cntrl_whsen_dem_21_df['spend_nonint_gdp'].mean()
std_nis_gdp_whsen_dem_21 = cntrl_whsen_dem_21_df['spend_nonint_gdp'].std()
n_nis_gdp_whsen_dem_21 = cntrl_whsen_dem_21_df['spend_nonint_gdp'].count()

avg_rev_gdp_whsen_dem_21 = cntrl_whsen_dem_21_df['receipts_gdp'].mean()
std_rev_gdp_whsen_dem_21 = cntrl_whsen_dem_21_df['receipts_gdp'].std()
n_rev_gdp_whsen_dem_21 = cntrl_whsen_dem_21_df['receipts_gdp'].count()

# Create Senate control (WH + Sen) split control df for 1947-2020
cntrl_whsen_spl_20_df = \
    df_20[((df_20['president_party'] == 'Republican') &
           (df_20['dem_senate_maj'] == 1)) |
          ((df_20['president_party'] == 'Democrat') &
           (df_20['dem_senate_maj'] == 0))]

avg_def_gdp_whsen_spl_20 = cntrl_whsen_spl_20_df['deficit_gdp'].mean()
std_def_gdp_whsen_spl_20 = cntrl_whsen_spl_20_df['deficit_gdp'].std()
n_def_gdp_whsen_spl_20 = cntrl_whsen_spl_20_df['deficit_gdp'].count()

avg_nis_gdp_whsen_spl_20 = cntrl_whsen_spl_20_df['spend_nonint_gdp'].mean()
std_nis_gdp_whsen_spl_20 = cntrl_whsen_spl_20_df['spend_nonint_gdp'].std()
n_nis_gdp_whsen_spl_20 = cntrl_whsen_spl_20_df['spend_nonint_gdp'].count()

avg_rev_gdp_whsen_spl_20 = cntrl_whsen_spl_20_df['receipts_gdp'].mean()
std_rev_gdp_whsen_spl_20 = cntrl_whsen_spl_20_df['receipts_gdp'].std()
n_rev_gdp_whsen_spl_20 = cntrl_whsen_spl_20_df['receipts_gdp'].count()

# Create Senate control (WH + Sen) split control df for 1947-2021
cntrl_whsen_spl_21_df = \
    df_21[((df_21['president_party'] == 'Republican') &
           (df_21['dem_senate_maj'] == 1)) |
          ((df_21['president_party'] == 'Democrat') &
           (df_21['dem_senate_maj'] == 0))]

avg_def_gdp_whsen_spl_21 = cntrl_whsen_spl_21_df['deficit_gdp'].mean()
std_def_gdp_whsen_spl_21 = cntrl_whsen_spl_21_df['deficit_gdp'].std()
n_def_gdp_whsen_spl_21 = cntrl_whsen_spl_21_df['deficit_gdp'].count()

avg_nis_gdp_whsen_spl_21 = cntrl_whsen_spl_21_df['spend_nonint_gdp'].mean()
std_nis_gdp_whsen_spl_21 = cntrl_whsen_spl_21_df['spend_nonint_gdp'].std()
n_nis_gdp_whsen_spl_21 = cntrl_whsen_spl_21_df['spend_nonint_gdp'].count()

avg_rev_gdp_whsen_spl_21 = cntrl_whsen_spl_21_df['receipts_gdp'].mean()
std_rev_gdp_whsen_spl_21 = cntrl_whsen_spl_21_df['receipts_gdp'].std()
n_rev_gdp_whsen_spl_21 = cntrl_whsen_spl_21_df['receipts_gdp'].count()

# Create House control (WH + HouseRep) Republican control df for 1947-2020
cntrl_whhou_rep_20_df = \
    df_20[(df_20['president_party'] == 'Republican') &
          (df_20['dem_house_maj'] == 0)]

avg_def_gdp_whhou_rep_20 = cntrl_whhou_rep_20_df['deficit_gdp'].mean()
std_def_gdp_whhou_rep_20 = cntrl_whhou_rep_20_df['deficit_gdp'].std()
n_def_gdp_whhou_rep_20 = cntrl_whhou_rep_20_df['deficit_gdp'].count()

avg_nis_gdp_whhou_rep_20 = cntrl_whhou_rep_20_df['spend_nonint_gdp'].mean()
std_nis_gdp_whhou_rep_20 = cntrl_whhou_rep_20_df['spend_nonint_gdp'].std()
n_nis_gdp_whhou_rep_20 = cntrl_whhou_rep_20_df['spend_nonint_gdp'].count()

avg_rev_gdp_whhou_rep_20 = cntrl_whhou_rep_20_df['receipts_gdp'].mean()
std_rev_gdp_whhou_rep_20 = cntrl_whhou_rep_20_df['receipts_gdp'].std()
n_rev_gdp_whhou_rep_20 = cntrl_whhou_rep_20_df['receipts_gdp'].count()

# Create House control (WH + HouseRep) Republican control df for 1947-2021
cntrl_whhou_rep_21_df = \
    df_21[(df_21['president_party'] == 'Republican') &
          (df_21['dem_house_maj'] == 0)]

avg_def_gdp_whhou_rep_21 = cntrl_whhou_rep_21_df['deficit_gdp'].mean()
std_def_gdp_whhou_rep_21 = cntrl_whhou_rep_21_df['deficit_gdp'].std()
n_def_gdp_whhou_rep_21 = cntrl_whhou_rep_21_df['deficit_gdp'].count()

avg_nis_gdp_whhou_rep_21 = cntrl_whhou_rep_21_df['spend_nonint_gdp'].mean()
std_nis_gdp_whhou_rep_21 = cntrl_whhou_rep_21_df['spend_nonint_gdp'].std()
n_nis_gdp_whhou_rep_21 = cntrl_whhou_rep_21_df['spend_nonint_gdp'].count()

avg_rev_gdp_whhou_rep_21 = cntrl_whhou_rep_21_df['receipts_gdp'].mean()
std_rev_gdp_whhou_rep_21 = cntrl_whhou_rep_21_df['receipts_gdp'].std()
n_rev_gdp_whhou_rep_21 = cntrl_whhou_rep_21_df['receipts_gdp'].count()

# Create House control (WH + HouseRep) Democrat control df for 1947-2020
cntrl_whhou_dem_20_df = \
    df_20[(df_20['president_party'] == 'Democrat') &
          (df_20['dem_house_maj'] == 1)]

avg_def_gdp_whhou_dem_20 = cntrl_whhou_dem_20_df['deficit_gdp'].mean()
std_def_gdp_whhou_dem_20 = cntrl_whhou_dem_20_df['deficit_gdp'].std()
n_def_gdp_whhou_dem_20 = cntrl_whhou_dem_20_df['deficit_gdp'].count()

avg_nis_gdp_whhou_dem_20 = cntrl_whhou_dem_20_df['spend_nonint_gdp'].mean()
std_nis_gdp_whhou_dem_20 = cntrl_whhou_dem_20_df['spend_nonint_gdp'].std()
n_nis_gdp_whhou_dem_20 = cntrl_whhou_dem_20_df['spend_nonint_gdp'].count()

avg_rev_gdp_whhou_dem_20 = cntrl_whhou_dem_20_df['receipts_gdp'].mean()
std_rev_gdp_whhou_dem_20 = cntrl_whhou_dem_20_df['receipts_gdp'].std()
n_rev_gdp_whhou_dem_20 = cntrl_whhou_dem_20_df['receipts_gdp'].count()

# Create House control (WH + HouseRep) Democrat control df for 1947-2021
cntrl_whhou_dem_21_df = \
    df_21[(df_21['president_party'] == 'Democrat') &
          (df_21['dem_house_maj'] == 1)]

avg_def_gdp_whhou_dem_21 = cntrl_whhou_dem_21_df['deficit_gdp'].mean()
std_def_gdp_whhou_dem_21 = cntrl_whhou_dem_21_df['deficit_gdp'].std()
n_def_gdp_whhou_dem_21 = cntrl_whhou_dem_21_df['deficit_gdp'].count()

avg_nis_gdp_whhou_dem_21 = cntrl_whhou_dem_21_df['spend_nonint_gdp'].mean()
std_nis_gdp_whhou_dem_21 = cntrl_whhou_dem_21_df['spend_nonint_gdp'].std()
n_nis_gdp_whhou_dem_21 = cntrl_whhou_dem_21_df['spend_nonint_gdp'].count()

avg_rev_gdp_whhou_dem_21 = cntrl_whhou_dem_21_df['receipts_gdp'].mean()
std_rev_gdp_whhou_dem_21 = cntrl_whhou_dem_21_df['receipts_gdp'].std()
n_rev_gdp_whhou_dem_21 = cntrl_whhou_dem_21_df['receipts_gdp'].count()

# Create House control (WH + HouseRep) split control df for 1947-2020
cntrl_whhou_spl_20_df = \
    df_20[((df_20['president_party'] == 'Republican') &
           (df_20['dem_house_maj'] == 1)) |
          ((df_20['president_party'] == 'Democrat') &
           (df_20['dem_house_maj'] == 0))]

avg_def_gdp_whhou_spl_20 = cntrl_whhou_spl_20_df['deficit_gdp'].mean()
std_def_gdp_whhou_spl_20 = cntrl_whhou_spl_20_df['deficit_gdp'].std()
n_def_gdp_whhou_spl_20 = cntrl_whhou_spl_20_df['deficit_gdp'].count()

avg_nis_gdp_whhou_spl_20 = cntrl_whhou_spl_20_df['spend_nonint_gdp'].mean()
std_nis_gdp_whhou_spl_20 = cntrl_whhou_spl_20_df['spend_nonint_gdp'].std()
n_nis_gdp_whhou_spl_20 = cntrl_whhou_spl_20_df['spend_nonint_gdp'].count()

avg_rev_gdp_whhou_spl_20 = cntrl_whhou_spl_20_df['receipts_gdp'].mean()
std_rev_gdp_whhou_spl_20 = cntrl_whhou_spl_20_df['receipts_gdp'].std()
n_rev_gdp_whhou_spl_20 = cntrl_whhou_spl_20_df['receipts_gdp'].count()

# Create House control (WH + HouseRep) split control df for 1947-2021
cntrl_whhou_spl_21_df = \
    df_21[((df_21['president_party'] == 'Republican') &
           (df_21['dem_house_maj'] == 1)) |
          ((df_21['president_party'] == 'Democrat') &
           (df_21['dem_house_maj'] == 0))]

avg_def_gdp_whhou_spl_21 = cntrl_whhou_spl_21_df['deficit_gdp'].mean()
std_def_gdp_whhou_spl_21 = cntrl_whhou_spl_21_df['deficit_gdp'].std()
n_def_gdp_whhou_spl_21 = cntrl_whhou_spl_21_df['deficit_gdp'].count()

avg_nis_gdp_whhou_spl_21 = cntrl_whhou_spl_21_df['spend_nonint_gdp'].mean()
std_nis_gdp_whhou_spl_21 = cntrl_whhou_spl_21_df['spend_nonint_gdp'].std()
n_nis_gdp_whhou_spl_21 = cntrl_whhou_spl_21_df['spend_nonint_gdp'].count()

avg_rev_gdp_whhou_spl_21 = cntrl_whhou_spl_21_df['receipts_gdp'].mean()
std_rev_gdp_whhou_spl_21 = cntrl_whhou_spl_21_df['receipts_gdp'].std()
n_rev_gdp_whhou_spl_21 = cntrl_whhou_spl_21_df['receipts_gdp'].count()

'''
-------------------------------------------------------------------------------
Print the table output
-------------------------------------------------------------------------------
'''

print('Avg. deficits-to-GDP by party control table output: 1947-2020 and ' +
      '1947-2021')
print('Republican control & ' + "{:.1f}".format(avg_def_gdp_all_rep_20) +
      ' & ' + "{:.1f}".format(avg_def_gdp_whsen_rep_20) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whhou_rep_20) + ' & ' +
      "{:.1f}".format(avg_def_gdp_all_rep_21) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whsen_rep_21) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whhou_rep_21) + ' \\\\[-0.5mm]')
print('            & (' + "{:.1f}".format(std_def_gdp_all_rep_20) + ') & (' +
      "{:.1f}".format(std_def_gdp_whsen_rep_20) + ') & (' +
      "{:.1f}".format(std_def_gdp_whhou_rep_20) + ') & (' +
      "{:.1f}".format(std_def_gdp_all_rep_21) + ') & (' +
      "{:.1f}".format(std_def_gdp_whsen_rep_21) + ') & (' +
      "{:.1f}".format(std_def_gdp_whhou_rep_21) + ') \\\\[-0.5mm]')
print('            & $N$=' + str(n_def_gdp_all_rep_20) + ' & $N$=' +
      str(n_def_gdp_whsen_rep_20) + ' & $N$=' + str(n_def_gdp_whhou_rep_20) +
      ' & $N$=' + str(n_def_gdp_all_rep_21) + ' & $N$=' +
      str(n_def_gdp_whsen_rep_21) + ' & $N$=' + str(n_def_gdp_whhou_rep_21) +
      ' \\\\')
print('Democrat control & ' + "{:.1f}".format(avg_def_gdp_all_dem_20) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whsen_dem_20) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whhou_dem_20) + ' & ' +
      "{:.1f}".format(avg_def_gdp_all_dem_21) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whsen_dem_21) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whhou_dem_21) + ' \\\\[-0.5mm]')
print('            & (' + "{:.1f}".format(std_def_gdp_all_dem_20) + ') & (' +
      "{:.1f}".format(std_def_gdp_whsen_dem_20) + ') & (' +
      "{:.1f}".format(std_def_gdp_whhou_dem_20) + ') & (' +
      "{:.1f}".format(std_def_gdp_all_dem_21) + ') & (' +
      "{:.1f}".format(std_def_gdp_whsen_dem_21) + ') & (' +
      "{:.1f}".format(std_def_gdp_whhou_dem_21) + ') \\\\[-0.5mm]')
print('            & $N$=' + str(n_def_gdp_all_dem_20) + ' & $N$=' +
      str(n_def_gdp_whsen_dem_20) + ' & $N$=' + str(n_def_gdp_whhou_dem_20) +
      ' & $N$=' + str(n_def_gdp_all_dem_21) + ' & $N$=' +
      str(n_def_gdp_whsen_dem_21) + ' & $N$=' + str(n_def_gdp_whhou_dem_21) +
      ' \\\\')
print('Split control & ' + "{:.1f}".format(avg_def_gdp_all_spl_20) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whsen_spl_20) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whhou_spl_20) + ' & ' +
      "{:.1f}".format(avg_def_gdp_all_spl_21) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whsen_spl_21) + ' & ' +
      "{:.1f}".format(avg_def_gdp_whhou_spl_21) + ' \\\\[-0.5mm]')
print('            & (' + "{:.1f}".format(std_def_gdp_all_spl_20) + ') & (' +
      "{:.1f}".format(std_def_gdp_whsen_spl_20) + ') & (' +
      "{:.1f}".format(std_def_gdp_whhou_spl_20) + ') & (' +
      "{:.1f}".format(std_def_gdp_all_spl_21) + ') & (' +
      "{:.1f}".format(std_def_gdp_whsen_spl_21) + ') & (' +
      "{:.1f}".format(std_def_gdp_whhou_spl_21) + ') \\\\[-0.5mm]')
print('            & $N$=' + str(n_def_gdp_all_spl_20) + ' & $N$=' +
      str(n_def_gdp_whsen_spl_20) + ' & $N$=' + str(n_def_gdp_whhou_spl_20) +
      ' & $N$=' + str(n_def_gdp_all_spl_21) + ' & $N$=' +
      str(n_def_gdp_whsen_spl_21) + ' & $N$=' + str(n_def_gdp_whhou_spl_21) +
      ' \\\\')

print('')
print('Avg. noninterest spending-to-GDP by party control table output: ' +
      '1947-2020 and 1947-2021')
print('Republican control & ' + "{:.1f}".format(avg_nis_gdp_all_rep_20) +
      ' & ' + "{:.1f}".format(avg_nis_gdp_whsen_rep_20) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whhou_rep_20) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_all_rep_21) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whsen_rep_21) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whhou_rep_21) + ' \\\\[-0.5mm]')
print('            & (' + "{:.1f}".format(std_nis_gdp_all_rep_20) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whsen_rep_20) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whhou_rep_20) + ') & (' +
      "{:.1f}".format(std_nis_gdp_all_rep_21) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whsen_rep_21) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whhou_rep_21) + ') \\\\[-0.5mm]')
print('            & $N$=' + str(n_nis_gdp_all_rep_20) + ' & $N$=' +
      str(n_nis_gdp_whsen_rep_20) + ' & $N$=' + str(n_nis_gdp_whhou_rep_20) +
      ' & $N$=' + str(n_nis_gdp_all_rep_21) + ' & $N$=' +
      str(n_nis_gdp_whsen_rep_21) + ' & $N$=' + str(n_nis_gdp_whhou_rep_21) +
      ' \\\\')
print('Democrat control & ' + "{:.1f}".format(avg_nis_gdp_all_dem_20) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whsen_dem_20) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whhou_dem_20) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_all_dem_21) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whsen_dem_21) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whhou_dem_21) + ' \\\\[-0.5mm]')
print('            & (' + "{:.1f}".format(std_nis_gdp_all_dem_20) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whsen_dem_20) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whhou_dem_20) + ') & (' +
      "{:.1f}".format(std_nis_gdp_all_dem_21) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whsen_dem_21) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whhou_dem_21) + ') \\\\[-0.5mm]')
print('            & $N$=' + str(n_nis_gdp_all_dem_20) + ' & $N$=' +
      str(n_nis_gdp_whsen_dem_20) + ' & $N$=' + str(n_nis_gdp_whhou_dem_20) +
      ' & $N$=' + str(n_nis_gdp_all_dem_21) + ' & $N$=' +
      str(n_nis_gdp_whsen_dem_21) + ' & $N$=' + str(n_nis_gdp_whhou_dem_21) +
      ' \\\\')
print('Split control & ' + "{:.1f}".format(avg_nis_gdp_all_spl_20) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whsen_spl_20) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whhou_spl_20) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_all_spl_21) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whsen_spl_21) + ' & ' +
      "{:.1f}".format(avg_nis_gdp_whhou_spl_21) + ' \\\\[-0.5mm]')
print('            & (' + "{:.1f}".format(std_nis_gdp_all_spl_20) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whsen_spl_20) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whhou_spl_20) + ') & (' +
      "{:.1f}".format(std_nis_gdp_all_spl_21) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whsen_spl_21) + ') & (' +
      "{:.1f}".format(std_nis_gdp_whhou_spl_21) + ') \\\\[-0.5mm]')
print('            & $N$=' + str(n_nis_gdp_all_spl_20) + ' & $N$=' +
      str(n_nis_gdp_whsen_spl_20) + ' & $N$=' + str(n_nis_gdp_whhou_spl_20) +
      ' & $N$=' + str(n_nis_gdp_all_spl_21) + ' & $N$=' +
      str(n_nis_gdp_whsen_spl_21) + ' & $N$=' + str(n_nis_gdp_whhou_spl_21) +
      ' \\\\')

print('')
print('Avg. receipts-to-GDP by party control table output: 1947-2020 and ' +
      '1947-2021')
print('Republican control & ' + "{:.1f}".format(avg_rev_gdp_all_rep_20) +
      ' & ' + "{:.1f}".format(avg_rev_gdp_whsen_rep_20) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whhou_rep_20) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_all_rep_21) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whsen_rep_21) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whhou_rep_21) + ' \\\\[-0.5mm]')
print('            & (' + "{:.1f}".format(std_rev_gdp_all_rep_20) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whsen_rep_20) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whhou_rep_20) + ') & (' +
      "{:.1f}".format(std_rev_gdp_all_rep_21) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whsen_rep_21) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whhou_rep_21) + ') \\\\[-0.5mm]')
print('            & $N$=' + str(n_rev_gdp_all_rep_20) + ' & $N$=' +
      str(n_rev_gdp_whsen_rep_20) + ' & $N$=' + str(n_rev_gdp_whhou_rep_20) +
      ' & $N$=' + str(n_rev_gdp_all_rep_21) + ' & $N$=' +
      str(n_rev_gdp_whsen_rep_21) + ' & $N$=' + str(n_rev_gdp_whhou_rep_21) +
      ' \\\\')
print('Democrat control & ' + "{:.1f}".format(avg_rev_gdp_all_dem_20) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whsen_dem_20) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whhou_dem_20) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_all_dem_21) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whsen_dem_21) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whhou_dem_21) + ' \\\\[-0.5mm]')
print('            & (' + "{:.1f}".format(std_rev_gdp_all_dem_20) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whsen_dem_20) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whhou_dem_20) + ') & (' +
      "{:.1f}".format(std_rev_gdp_all_dem_21) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whsen_dem_21) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whhou_dem_21) + ') \\\\[-0.5mm]')
print('            & $N$=' + str(n_rev_gdp_all_dem_20) + ' & $N$=' +
      str(n_rev_gdp_whsen_dem_20) + ' & $N$=' + str(n_rev_gdp_whhou_dem_20) +
      ' & $N$=' + str(n_rev_gdp_all_dem_21) + ' & $N$=' +
      str(n_rev_gdp_whsen_dem_21) + ' & $N$=' + str(n_rev_gdp_whhou_dem_21) +
      ' \\\\')
print('Split control & ' + "{:.1f}".format(avg_rev_gdp_all_spl_20) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whsen_spl_20) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whhou_spl_20) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_all_spl_21) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whsen_spl_21) + ' & ' +
      "{:.1f}".format(avg_rev_gdp_whhou_spl_21) + ' \\\\[-0.5mm]')
print('            & (' + "{:.1f}".format(std_rev_gdp_all_spl_20) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whsen_spl_20) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whhou_spl_20) + ') & (' +
      "{:.1f}".format(std_rev_gdp_all_spl_21) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whsen_spl_21) + ') & (' +
      "{:.1f}".format(std_rev_gdp_whhou_spl_21) + ') \\\\[-0.5mm]')
print('            & $N$=' + str(n_rev_gdp_all_spl_20) + ' & $N$=' +
      str(n_rev_gdp_whsen_spl_20) + ' & $N$=' + str(n_rev_gdp_whhou_spl_20) +
      ' & $N$=' + str(n_rev_gdp_all_spl_21) + ' & $N$=' +
      str(n_rev_gdp_whsen_spl_21) + ' & $N$=' + str(n_rev_gdp_whhou_spl_21) +
      ' \\\\')

'''
-------------------------------------------------------------------------------
Print p-values from t-tests
-------------------------------------------------------------------------------
'''
print('')
print('Deficit: Column 5 (WH + Sen with forecast): Pr: split control = ' +
      'Rep control (using split control)')
df1 = n_def_gdp_whsen_spl_21 - 1
t_test_stat1 = ((avg_def_gdp_whsen_spl_21 - avg_def_gdp_whsen_rep_21) /
                std_def_gdp_whsen_spl_21)
p_value1 = 1 - tdist.cdf(abs(t_test_stat1), df1)
print('t-test stat with df = ' + str(df1) + ':', "{:.3f}".format(t_test_stat1))
print('One-sided p-value of t-stat with df = ' + str(df1) + ':',
      "{:.3f}".format(p_value1))

# print('')
# print('Deficit: Column 5 (WH + Sen with forecast): Pr: split control = ' +
#       'Rep control (using Rep control)')
# df2 = n_def_gdp_whsen_rep_21 - 1
# t_test_stat2 = ((avg_def_gdp_whsen_rep_21 - avg_def_gdp_whsen_spl_21) /
#                 std_def_gdp_whsen_rep_21)
# p_value2 = 1 - tdist.cdf(abs(t_test_stat2), df2)
# print('t-test stat with df = ' + str(df2) + ':', "{:.3f}".format(t_test_stat2))
# print('One-sided p-value of t-stat with df = ' + str(df2) + ':',
#       "{:.3f}".format(p_value2))

print('')
print('Deficit: Column 5 (WH + Sen with forecast): Pr: split control = ' +
      'Dem control (using split control)')
df3 = n_def_gdp_whsen_spl_21 - 1
t_test_stat3 = ((avg_def_gdp_whsen_spl_21 - avg_def_gdp_whsen_dem_21) /
                std_def_gdp_whsen_spl_21)
p_value3 = 1 - tdist.cdf(abs(t_test_stat3), df3)
print('t-test stat with df = ' + str(df3) + ':', "{:.3f}".format(t_test_stat3))
print('One-sided p-value of t-stat with df = ' + str(df3) + ':',
      "{:.3f}".format(p_value3))

# print('')
# print('Deficit: Column 5 (WH + Sen with forecast): Pr: split control = ' +
#       'Dem control (using Dem control)')
# df4 = n_def_gdp_whsen_dem_21 - 1
# t_test_stat4 = ((avg_def_gdp_whsen_dem_21 - avg_def_gdp_whsen_spl_21) /
#                 std_def_gdp_whsen_dem_21)
# p_value4 = 1 - tdist.cdf(abs(t_test_stat4), df4)
# print('t-test stat with df = ' + str(df4) + ':', "{:.3f}".format(t_test_stat4))
# print('One-sided p-value of t-stat with df = ' + str(df4) + ':',
#       "{:.3f}".format(p_value4))

# print('')
# print('Deficit: Column 5 (WH + Sen with forecast): Pr: Rep control = ' +
#       'Dem control (using Dem control)')
# df5 = n_def_gdp_whsen_dem_21 - 1
# t_test_stat5 = ((avg_def_gdp_whsen_rep_21 - avg_def_gdp_whsen_dem_21) /
#                 std_def_gdp_whsen_dem_21)
# p_value5 = 1 - tdist.cdf(abs(t_test_stat5), df5)
# print('t-test stat with df = ' + str(df5) + ':', "{:.3f}".format(t_test_stat5))
# print('One-sided p-value of t-stat with df = ' + str(df5) + ':',
#       "{:.3f}".format(p_value5))

print('')
print('Deficit: Column 5 (WH + Sen with forecast): Pr: Rep control = ' +
      'Dem control (using Rep control)')
df6 = n_def_gdp_whsen_rep_21 - 1
t_test_stat6 = ((avg_def_gdp_whsen_rep_21 - avg_def_gdp_whsen_dem_21) /
                std_def_gdp_whsen_rep_21)
p_value6 = 1 - tdist.cdf(abs(t_test_stat6), df6)
print('t-test stat with df = ' + str(df6) + ':', "{:.3f}".format(t_test_stat6))
print('One-sided p-value of t-stat with df = ' + str(df6) + ':',
      "{:.3f}".format(p_value6))

print('')
print('Spending: Column 5 (WH + Sen with forecast): Pr: split control = ' +
      'Rep control (using split control)')
df7 = n_nis_gdp_whsen_spl_21 - 1
t_test_stat7 = ((avg_nis_gdp_whsen_rep_21 - avg_nis_gdp_whsen_spl_21) /
                std_nis_gdp_whsen_spl_21)
p_value7 = 1 - tdist.cdf(abs(t_test_stat7), df7)
print('t-test stat with df = ' + str(df7) + ':', "{:.3f}".format(t_test_stat7))
print('One-sided p-value of t-stat with df = ' + str(df7) + ':',
      "{:.3f}".format(p_value7))

# print('')
# print('Spending: Column 5 (WH + Sen with forecast): Pr: split control = ' +
#       'Rep control (using Rep control)')
# df8 = n_nis_gdp_whsen_rep_21 - 1
# t_test_stat8 = ((avg_nis_gdp_whsen_rep_21 - avg_nis_gdp_whsen_spl_21) /
#                 std_nis_gdp_whsen_rep_21)
# p_value8 = 1 - tdist.cdf(abs(t_test_stat8), df8)
# print('t-test stat with df = ' + str(df8) + ':', "{:.3f}".format(t_test_stat8))
# print('One-sided p-value of t-stat with df = ' + str(df8) + ':',
#       "{:.3f}".format(p_value8))

print('')
print('Spending: Column 5 (WH + Sen with forecast): Pr: split control = ' +
      'Dem control (using split control)')
df9 = n_nis_gdp_whsen_spl_21 - 1
t_test_stat9 = ((avg_nis_gdp_whsen_dem_21 - avg_nis_gdp_whsen_spl_21) /
                std_nis_gdp_whsen_spl_21)
p_value9 = 1 - tdist.cdf(abs(t_test_stat9), df9)
print('t-test stat with df = ' + str(df9) + ':', "{:.3f}".format(t_test_stat9))
print('One-sided p-value of t-stat with df = ' + str(df9) + ':',
      "{:.3f}".format(p_value9))

# print('')
# print('Spending: Column 5 (WH + Sen with forecast): Pr: split control = ' +
#       'Dem control (using Dem control)')
# df10 = n_nis_gdp_whsen_dem_21 - 1
# t_test_stat10 = ((avg_nis_gdp_whsen_dem_21 - avg_nis_gdp_whsen_spl_21) /
#                  std_nis_gdp_whsen_dem_21)
# p_value10 = 1 - tdist.cdf(abs(t_test_stat10), df10)
# print('t-test stat with df = ' + str(df10) + ':',
#       "{:.3f}".format(t_test_stat10))
# print('One-sided p-value of t-stat with df = ' + str(df10) + ':',
#       "{:.3f}".format(p_value10))

'''
-------------------------------------------------------------------------------
Run regressions on Republican and Democrat control scatter data
-------------------------------------------------------------------------------
'''
df1 = cntrl_whsen_rep_20_df
df1['const'] = 1
reg1a = sm.OLS(endog=df1['deficit_gdp'], exog=df1[['const', 'dem_senateseats']],
              missing='drop')
res1a = reg1a.fit()
print('')
print('Regression results for def/GDP by Dem Senate seats, ' +
      'Republican Control (WH + Sen) 1947-2020')
print(res1a.summary())
reg1b = sm.OLS(endog=df1['deficit_gdp'], exog=df1[['const', 'dem_houseseats']],
              missing='drop')
res1b = reg1b.fit()
print('')
print('Regression results for def/GDP by Dem House seats, ' +
      'Republican Control (WH + Sen) 1947-2020')
print(res1b.summary())


df2 = cntrl_whsen_dem_20_df
df2['const'] = 1
reg2a = sm.OLS(endog=df2['deficit_gdp'], exog=df2[['const', 'dem_senateseats']],
              missing='drop')
res2a = reg2a.fit()
print('')
print('Regression results for def/GDP by Dem Senate seats, ' +
      'Democrat Control (WH + Sen) 1947-2020')
print(res2a.summary())
reg2b = sm.OLS(endog=df2['deficit_gdp'], exog=df2[['const', 'dem_houseseats']],
              missing='drop')
res2b = reg2b.fit()
print('')
print('Regression results for def/GDP by Dem House seats, ' +
      'Democrat Control (WH + Sen) 1947-2020')
print(res2b.summary())

df3 = cntrl_whsen_dem_21_df
df3['const'] = 1
reg3a = sm.OLS(endog=df3['deficit_gdp'], exog=df3[['const', 'dem_senateseats']],
              missing='drop')
res3a = reg3a.fit()
print('')
print('Regression results for def/GDP by Dem Senate seats, ' +
      'Democrat Control (WH + Sen) 1947-2021')
print(res3a.summary())
reg3b = sm.OLS(endog=df3['deficit_gdp'], exog=df3[['const', 'dem_houseseats']],
              missing='drop')
res3b = reg3b.fit()
print('')
print('Regression results for def/GDP by Dem House seats, ' +
      'Democrat Control (WH + Sen) 1947-2021')
print(res3b.summary())
