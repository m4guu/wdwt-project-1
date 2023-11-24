
df[['TC2S3']].plot()
plt.xlabel('Samples')
plt.ylabel('Temperature [°C]')
plt.title('Histogram for TC2 in series 3 before procssing')
plt.savefig('images/before_data_processing.png')

# Replace non-numeric values with NaN
df = df.apply(pd.to_numeric, errors='coerce')

# Forward/Backward fill NaN values (fill NaN with the previous/next non-NaN value in the column)
df = df.ffill()
df = df.bfill()



# Iteracja po kolumnach i eliminacja błędów
for column in df.columns:
    for i in range(1, len(df)):
        diff = abs((df[column][i] - df[column][i-1]))
        if diff >= 0.2:
            df.at[i, column] = df.at[i-1, column]


df[['TC2S3']].plot()
plt.xlabel('Samples')
plt.ylabel('Temperature [°C]')
plt.title('Histogram for TC2 in series 3 after procssing using 2nd method')
plt.savefig('images/after_data_processing_2.png')

mean_values = df.mean()             # Wartość średnia arytmetyczna
range_values = df.max() - df.min()  # Rozstęp
mode_values = df.mode().iloc[0]     # Wartość modalna (dominanta)
median_values = df.median()         # Mediana
skewness_values = df.skew()         # Skośność
kurtosis_values = df.kurtosis()     # Szczytowość (kurtoza)
std_dev_values = df.std()           # Odchylenie standardowe

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
    df_series.plot(kind='hist', bins=41, edgecolor='black', linewidth=1.2, alpha=0.7, ax=axs[i])
    axs[i].set_title(f'Histogram for series {i+1}')
    axs[i].set_xlabel('Temperature [°C]')
    axs[i].set_ylabel('Samples')

# Adjust layout
plt.tight_layout()
plt.savefig('images/histogramy_temperatur.png')

df[['TC1S1', 'TC1S2', 'TC1S3']].plot(kind='hist', bins=40, edgecolor='black', linewidth=1.2, alpha=0.7)
plt.xlabel('Temperature [°C]')
plt.title('Histogram for TC1 in 3 series')
plt.savefig('images/histogramy_temperatur_2.png')

df[['TC1S1']].plot()
plt.savefig('images/line_chart_TC1S1')
df[['TC2S1']].plot()
plt.savefig('images/line_chart_TC2S1')

window_size = 5
TC2S1_smooth = df[['TC2S1']].rolling(window=window_size).mean()
TC2S1_smooth.plot()
plt.savefig('images/line_chart_TC2S1_smooth')


