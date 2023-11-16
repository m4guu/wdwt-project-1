import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
df = pd.read_csv('data/data.csv')

# Replace non-numeric values with NaN
df = df.apply(pd.to_numeric, errors='coerce')

# Forward/Backward fill NaN values (fill NaN with the previous/next non-NaN value in the column)
df = df.ffill()
df = df.bfill()

# MEDIAN
median_temp = df[df<40].median()
# Replace values greater than 40 with the median for each column
df[df > 40] = median_temp.iloc[3]

# 1. Wartość średnia arytmetyczna
mean_values = df.mean()

# 2. Rozstęp
range_values = df.max() - df.min()

# 3. Wartość modalna (dominanta)
mode_values = df.mode().iloc[0]

# 4. Mediana
median_values = df.median()

# 5. Skośność
skewness_values = df.skew()

# 6. Szczytowość (kurtoza)
kurtosis_values = df.kurtosis()

# 7. Odchylenie standardowe
std_dev_values = df.std()

# Wydrukuj wyniki
print("1. Wartość średnia arytmetyczna:")
print(mean_values)

print("\n2. Rozstęp:")
print(range_values)

print("\n3. Wartość modalna (dominanta):")
print(mode_values)

print("\n4. Mediana:")
print(median_values)

print("\n5. Skośność:")
print(skewness_values)

print("\n6. Szczytowość (kurtoza):")
print(kurtosis_values)

print("\n7. Odchylenie standardowe:")
print(std_dev_values)

# Select columns for histograms
columns_to_plot = [['TC1S1', 'TC2S1'], ['TC1S2', 'TC2S2'], ['TC1S3', 'TC2S3']]

# Plot histograms using a loop
fig, axs = plt.subplots(1, len(columns_to_plot), figsize=(15, 5), sharey=True)

for i, columns in enumerate(columns_to_plot):
    df_series = df[columns]
    df_series.plot(kind='hist', bins=40, edgecolor='black', linewidth=1.2, alpha=0.7, ax=axs[i])
    axs[i].set_title(f'Histogram for series {i+1}')
    axs[i].set_xlabel('Temperature [°C]')
    axs[i].set_ylabel('Frequency')

# Adjust layout
plt.tight_layout()
plt.savefig('images/histogramy_temperatur.png')

df[['TC1S1', 'TC1S2', 'TC1S3']].plot(kind='hist', bins=40, edgecolor='black', linewidth=1.2, alpha=0.7)
plt.xlabel('Temperature [°C]')
plt.title('Histogram for TC1 in 3 series')
plt.savefig('images/histogramy_temperatur_2.png')
