import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Importing data
med_data = pd.read_csv('Medical Data Visualizer\medical_examination.csv')
# Adding 'Overweight' column

med_data['overweight'] = (med_data['weight'] / (med_data['height']/100)**2).apply(lambda x: 1 if x > 25 else 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

med_data['cholesterol'] = np.where(med_data['cholesterol']>1,1,0)
med_data['gluc'] = np.where(med_data['gluc']>1,1,0)


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(med_data,value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active','overweight'],id_vars=['cardio'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat['total'] = 0
    df_cat = df_cat.groupby(['cardio','variable','value'],as_index=False).count()
    print(df_cat)

    # Draw the catplot with 'sns.catplot()'
    plt_data = sns.catplot(data=df_cat,x="variable",y="total",col='cardio',kind='bar',errorbar=None,hue='value')
    plt.show()
    # # Get the figure for the output
    fig = plt.figure()


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = med_data[(med_data['ap_lo'] <= med_data['ap_hi'])&(med_data['height'] >= med_data['height'].quantile(0.025))&(med_data['height'] <= med_data['height'].quantile(0.975))&(med_data['weight'] >= med_data['weight'].quantile(0.025))&(med_data['weight'] <= med_data['weight'].quantile(0.975))]

    # # Calculate the correlation matrix
    corr = df_heat.corr()
    # corr.iloc[13]*=-1
    # # Generate a mask for the upper triangle
    mask = np.triu(corr)

    maskdf = pd.DataFrame(mask)


    # # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(7,5))

    # # Draw the heatmap with 'sns.heatmap()'

    corr_heatmap = sns.heatmap(data=corr,annot=True,mask=mask,fmt=".1f",cbar_kws = {'shrink':0.5},vmax=.3,linewidths=.5,center=0)
    plt.show()

    # # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

    print(maskdf)

draw_heat_map()