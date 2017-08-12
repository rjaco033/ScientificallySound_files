import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create simulated data for control group
random.seed(1)
control = [random.randrange(0,50) for i in range(80)]
# Create simulated data for treatment group
random.seed(2)
treatment = [random.randrange(15,65) for i in range(80)]
# Create dataframe and reshape to use with Seaborn
data = pd.DataFrame({'control': control, 'treatment': treatment})
data_long = pd.melt(data,  value_vars=['control','treatment'])

# Plot using stripplot for subject data, no jitter or dodge
sns.set(font_scale=1.5)
sns.set_style("ticks")
fig = plt.figure(figsize=(20,14))
ax1 = fig.add_subplot(131)
sns.stripplot(x="variable", y="value", data=data_long, dodge=False, jitter=False, alpha=1, zorder=1, size=8)
sns.pointplot(x='variable', y='value', ci='sd', data=data_long, join=False, scale=1.5, zorder=100, color='black')
ax1.set_xlabel('')
ax1.set_ylabel('weight (g)')
sns.despine(offset=10, trim=True)
# Plot using stripplot for subject data with jitter and dodge
sns.set(font_scale=1.5)
sns.set_style("ticks")
ax1 = fig.add_subplot(132)
sns.stripplot(x="variable", y="value", data=data_long, dodge=True, jitter=True, alpha=.40, zorder=1, size=8)
sns.pointplot(x='variable', y='value', ci='sd', data=data_long, join=False, scale=1.5, zorder=100, color='black')
ax1.set_xlabel('')
ax1.set_ylabel('weight (g)')
sns.despine(offset=10, trim=True)
#Plot using swarmplot for subject data
ax2 = fig.add_subplot(133)
sns.swarmplot(x='variable', y="value", data=data_long, alpha=0.40, zorder=1, size=8)
sns.pointplot(x='variable', y='value', ci='sd', data=data_long, join=False, scale=1.5, zorder=100, color='black')
ax2.set_xlabel('')
ax2.set_ylabel('weight (g)')
sns.despine(offset=10, trim=True)

