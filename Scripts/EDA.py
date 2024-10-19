import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipaddress


# Set up plotting aesthetics
plt.style.use('ggplot')
sns.set_palette('Set2')

# Univariate analysis for each column
def univariate_analysis(df, column):
    plt.figure(figsize=(10, 6))
    
    # If the column is numerical
    if df[column].dtype in ['int64', 'float64']:
        sns.histplot(df[column], kde=True, bins=30)
        plt.title(f'Distribution of {column}')
    
    # If the column is categorical
    else:
        sns.countplot(y=df[column], order=df[column].value_counts().index)
        plt.title(f'Countplot of {column}')
    
    plt.show()



# Function to convert IP address to integer, handling invalid cases
def ipAddress_conversion(df, column):
    valid_ips = []
    invalid_ips = []
    
    # Iterate through each row in the IP address column
    for ip in df[column]:
        try:
            # Try converting the IP address to integer using IPv4 conversion
            valid_ips.append(int(ipaddress.IPv4Address(ip)))
        except ValueError:
            # If there is a malformed IP, append None or handle as needed
            invalid_ips.append(ip)
            valid_ips.append(None)  # Handle invalid IPs (e.g., set to None)
    
    # Add converted IP addresses to the dataframe
    df[f'{column}_int'] = invalid_ips
    
    # Return the modified dataframe, and the list of invalid IPs
    return df, invalid_ips, valid_ips

