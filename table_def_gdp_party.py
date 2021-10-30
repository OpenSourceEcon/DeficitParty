'''
This script creates the table output for average deficits, noninterest
spending, and revenues as a percent of GDP by party control.
'''

# Import packages
import numpy as np
import pandas as pd
import os

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
