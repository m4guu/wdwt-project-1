import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# Load the CSV file into a DataFrame
df = pd.read_csv('data/data.csv')  
# Replace non-numeric values with NaN
df = df.apply(pd.to_numeric, errors='coerce')       

labels = ['TC1S1', 'TC2S1', 'TC1S2', 'TC2S2', 'TC1S3', 'TC2S3']

fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 10))
axes = axes.flatten()

for i, label in enumerate(labels):
    df[[label]].plot(ax=axes[i])
    axes[i].set_xlabel('Samples')
    axes[i].set_ylabel('Temperature [°C]')
    axes[i].set_title(f'Chart for {label}')

plt.tight_layout()
plt.savefig('images/fig_1.png')

### Filtering TC2S3
## 1st method
# Replace values greater than 40 with the median for each column
median_temp = df[df<40].median()
df[df > 40] = median_temp.iloc[3]
df[['TC2S3']].plot()
plt.xlabel('Samples')
plt.ylabel('Temperature [°C]')
plt.title('TC2 in series 3 after processing using 1st method')
plt.savefig('images/after_data_processing_1.png')
## 2nd method
# Standard deviation
std_TC2S3 = df[['TC2S3']].std().iloc[0]
# Iterating through columns and eliminating errors
for column in df.columns:
    for i in range(1, len(df)):
        diff = abs((df[column][i] - df[column][i-1]))
        if diff >= std_TC2S3 * 2:
            df.at[i, column] = df.at[i-1, column]

df[['TC2S3']].plot()
plt.xlabel('Samples')
plt.ylabel('Temperature [°C]')
plt.title('TC2 in series 3 after processing using 1st method')
plt.savefig('images/after_data_processing_2.png')
### Fill NaN values
# Count the number of NaN values in each column
nan_count = df.isna().sum()
# Calculate the procentage of missing values for TC1S1 and TC2S2
percentage_missing_TC1S1 = df[['TC1S1']].isna().mean() * 100
percentage_missing_TC2S2 = df[['TC2S2']].isna().mean() * 100
# Forward/Backward fill NaN values (fill NaN with the previous/next non-NaN value in the column)
df = df.ffill()
df = df.bfill()

### STATISTICAL INDICATORS
mean_values = df.mean()             # Wartość średnia arytmetyczna
range_values = df.max() - df.min()  # Rozstęp
mode_values = df.mode().iloc[0]     # Wartość modalna (dominanta)
median_values = df.median()         # Mediana
skewness_values = df.skew()         # Skośność
kurtosis_values = df.kurtosis()     # Szczytowość (kurtoza)

### FREQUENCY ANALYSIS
std_dev_values = df.std()           # standard deviation
# Select columns for histograms
columns_to_plot = [['TC1S1', 'TC2S1'], ['TC1S2', 'TC2S2'], ['TC1S3', 'TC2S3']]

# Plot histograms using a loop
fig, axs = plt.subplots(1, len(columns_to_plot), figsize=(15, 5), sharey=True)

for i, columns in enumerate(columns_to_plot):
    df_series = df[columns]
    df_series.plot(kind='hist', bins=41, edgecolor='black', linewidth=1.2, alpha=0.7, ax=axs[i])
    axs[i].set_title(f'Histogram for series {i+1}')
    axs[i].set_xlabel('Temperature [°C]')
    axs[i].set_ylabel('Samples')

# Adjust layout
plt.tight_layout()
plt.savefig('images/histogramy_temperatur.png')

# Fit normal distribution to the data
mu, std = norm.fit(df[['TC1S1']])
# Create a histogram of the data
df[['TC1S1']].plot(kind='hist', bins=41, density=True, alpha=0.7, color='#1f77b4', edgecolor='black', linewidth=1.2)
# Plot the fitted normal distribution
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, color='#ff7f0e', linewidth=2)
# Add labels and title
plt.xlabel('Temperature [°C]')
plt.ylabel('Density')
plt.title('Histogram with Fitted Normal Distribution (TC1S1)')
# Save the plot
plt.savefig('images/fit.png')
