'''
#import key_data.txt
key = np.genfromtxt("key_data.txt", unpack=True, skiprows = 1)
#key = ID
print(key)
'''
import pandas as pd
key_data=pd.read_csv("key_data.txt", delim_whitespace=True, skipinitialspace=True)
print(key_data.columns[0])