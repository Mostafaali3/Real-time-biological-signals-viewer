import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

class wave:
    def __init__(self, dir, sampling_rate, interp_order):
        '''
        args:
            - dir is an array of the directories of the data sheets in csv format
        '''
        self.dir = dir
        self.raw_data = [pd.read_csv(f'{self.dir[i]}.csv') for i in range(len(dir))]  
        self.sampling_rate = sampling_rate
        self.min_time, self.max_time = self.get_time_range(self.raw_data)
        self.time_grid = self.create_time_grid(self.min_time, self.max_time, self.sampling_rate)
        self.interp_order = interp_order
        self.data_samples = self.concatenate_resampled_data(self.raw_data, self.time_grid)
    
    def get_time_range(self, dataframes):
        """
        Find the minimum and maximum time values across all dataframes.
        """
        min_time = min([df['time'].min() for df in dataframes])
        max_time = min([df['time'].max() for df in dataframes])
        return min_time, max_time

    def create_time_grid(self, min_time, max_time, target_sampling_rate):
        """
        Create a common time grid based on the target sampling rate.
        """
        dt = 1.0 / target_sampling_rate  # Time interval between samples
        common_time_grid = np.arange(min_time, max_time, dt)  # Time values for resampling
        return common_time_grid
    
    def resample_single_dataframe(self, df, target_sampling_rate, interp_order):
        """
        Resample a single dataframe using interpolation to fit the common time grid.
        """
        min_time, max_time = self.get_time_range([df])
        common_time_grid = self.create_time_grid(min_time, max_time, target_sampling_rate)
        
        time_values = df['time'].values  # Original time values
        data_values = df.drop(columns='time').values  # Exclude the 'time' column

        resampled_data = {}
        
        # Interpolate each column separately
        for col_idx, col_name in enumerate(df.columns[1:]):  # Skip 'time' column
            # Create interpolation function
            interp_func = interp1d(time_values, data_values[:, col_idx], kind=interp_order, fill_value="extrapolate")
            # Apply interpolation to the common time grid
            resampled_values = interp_func(common_time_grid)
            resampled_data[col_name] = resampled_values
        
        return resampled_data

    def concatenate_resampled_data(self, raw_dataframes, common_time_grid):
        """
        Combine the resampled data from multiple dataframes into a final dataframe.
        """
        resampled_dataframes = []
        for idx ,dataframe in enumerate(raw_dataframes):
            resampled_dataframes.append(self.resample_single_dataframe(dataframe, self.sampling_rate, self.interp_order))
            print(len(resampled_dataframes[idx][f'value{idx+1}']))
          
          # Find the minimum length across all resampled data
        min_length = min([len(df[f'value{idx+1}']) for idx, df in enumerate(resampled_dataframes)])
        print(f"Minimum length of all resampled data: {min_length}")
        
        # Clip all resampled dataframes to the minimum length
        for idx in range(len(resampled_dataframes)):
            for col in resampled_dataframes[idx].keys():
                resampled_dataframes[idx][col] = resampled_dataframes[idx][col][:min_length]  # Clip to min_length
    
                
        resampled_data = {'time': common_time_grid[:min_length]}
        for resampled_df_data in resampled_dataframes:
            resampled_data.update(resampled_df_data)  # Add each resampled dataframe's data
        
        resampled_df = pd.DataFrame(resampled_data)
        return resampled_df


