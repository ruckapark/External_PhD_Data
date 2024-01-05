# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:57:39 2024

Code for analysis of RSDE data in 2021 INERIS report

@author: Admin
"""

import pandas as pd

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path, index_col=None)
        self.concentration_columns = [col for col in self.data.columns if 'concentration' in col.lower()]
        self.group_columns = [col for col in self.data.columns if col not in self.concentration_columns]
        self.replace_nan_lq()
        self.INF,self.EFF = self.separate_dataframes()
        
    def replace_nan_lq(self):
        ql_column = [col for col in self.data.columns if col.startswith('QL')][0]
        for col in self.concentration_columns:
            self.data[col] = pd.to_numeric(self.data[col], errors = 'coerce')
            
            #use mask to replace nans with data from ql
            nan_mask = self.data[col].isna()
            self.data[col].loc[nan_mask] = self.data[ql_column].loc[nan_mask].values

    def separate_dataframes(self):
        inf_columns = self.group_columns + [col for col in self.data.columns if 'INF' in col]
        eff_columns = self.group_columns + [col for col in self.data.columns if 'EFF' in col]
        INF_df = self.data[inf_columns].copy()
        EFF_df = self.data[eff_columns].copy()
        return INF_df,EFF_df

# Usage (data in current directory)
file_path = 'RSDE_table1314data.csv'
RSDE = DataProcessor(file_path)