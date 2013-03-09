# -*- coding: utf-8 -*-
'''
MetMast
-------

A straightforward met mast import class built with the pandas library

'''
from __future__ import print_function
import os
import json
import pandas as pd
from pandas import DataFrame

class MetMast(object): 
    '''Subclass of the pandas dataframe built to import and quickly analyze
       met mast data.'''
       
    def __init__(self, lat=None, lon=None, height=None, time_zone=None):
        '''Data structure with both relevant information about the mast
        itself (coordinates, height, time zone), as well as methods to process
        the met mast data and manipulate it using tools from the pandas
        library. 
        
        Parameters
        ----------
        lat: float, default None
            Latitude of met mast
        long: float, default None
            Longitude of met mast
        height: float or int, default None
            Height of met mast
        time_zone: string
            Please follow the pytz time zone conventions: 
            http://pytz.sourceforge.net/
        '''
        self.lat = lat
        self.lon = lon
        self.height = height
        self.time_zone = time_zone
        
    def wind_import(self, path, columns=None, header_row=None, time_col=None,
                    delimiter=None, parse_cols=True, **kwargs):
        '''Wind data import. This is a very thin wrapper on the pandas read_table 
        method, with the option to pass keyword arguments to pandas read_table 
        if needed. 
    
        Parameters:
        ----------
        path: string
            Path to file to be read
        header_row: int
            Row containing columns headers
        time_col: int
            Column with the timestamps
        delimiter: string
            File delimiter
    
        Returns: 
        --------
        DataFrame with wind data
        '''
        self.data = pd.read_table(path, header=header_row, index_col=time_col, 
                                  parse_dates=True, delimiter=delimiter,
                                  **kwargs)
                                  
        if parse_cols:                         
            '''Smart parse columns for Parameters'''
            data_columns = self.data.columns.tolist()
            data_columns = [x.strip().lower() for x in data_columns]
        
            #Read json from pkg
            pkg_dir, filename = os.path.split(__file__)
            json_path = os.path.join(pkg_dir, 'data', 'data_parse.json')
            with open(json_path, 'r') as f: 
                parse_strings = json.load(f)
        
            #Search dict for parameter match, rename column
            iter_dict = {'Std Dev': 1, 'Wind Speed': 1, 'Wind Direction': 1}
            new_columns = []
            for x, cols in enumerate(data_columns): 
                get_col = parse_strings.get(cols)
                if get_col:
                    new_col = '{0} {1}'.format(get_col, str(iter_dict[get_col]))
                    new_columns.append(new_col)
                    iter_dict[get_col] += 1
                else: 
                    print('Header parser could not parse ', cols)
                    new_columns.append(cols)
            self.data.columns = new_columns
                                       
    def mean_ws(time_period='all'):
        '''
        Averaging of mean wind speed
        '''
        pass 
        
    def sectorwise(sectors=12, **kwargs):
        '''Bin the wind data sectorwise
        '''
        pass
        if not self.data:
            print(("You have not imported any data. Use the 'wind_import'"
                   "method to load data into your object"))
        cuts = 360/sectors
        bins = [0, cuts/2]
        bins.extend(range(cuts, 360, cuts))
        bins.extend([360-cuts/2, 360])
        cats = pd.cut(self.data['Average Direction'], bins, right=False)
        array = pd.value_counts(cats)
        
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  