import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import pearsonr, kruskal, shapiro, f_oneway
from sklearn.metrics import auc


def calculate_pearson(df, column1, column2):
    """
    calculate pearson's correlation between two columns of a df'
    :param df:
    :return:
    """
    output = pearsonr(df[column1].astype(float), df[column2].astype(float))
    return output


def flatten(xss):
    return [x for xs in xss for x in xs]


g50071 = pd.read_excel('../pythonProject/data_summary.xlsx', sheet_name='50071')
g50071 = g50071.drop(0)
Pa3 = pd.read_excel('../pythonProject/data_summary.xlsx', sheet_name='Pa3')
Pa3 = Pa3.drop(0)
Pa4 = pd.read_excel('../pythonProject/data_summary.xlsx', sheet_name='Pa4')
Pa4 = Pa4.drop(0)
Pa8 = pd.read_excel('../pythonProject/data_summary.xlsx', sheet_name='Pa8')
Pa8 = Pa8.drop(0)
Pa13 = pd.read_excel('../pythonProject/data_summary.xlsx', sheet_name='Pa13')
Pa13 = Pa13.drop(0)

## AUC calculation for MOI 10
time = [g50071['Time(min)']]
time = flatten(time)

# Convert time strings to seconds for plotting
time_data = [int(t.split(":")[0]) * 60 + int(t.split(":")[1]) + (int(t.split(":")[0]) / 60) for t in time]
time_data_hours = [t / 60 for t in time_data]

KE1 = [g50071['KE MOI 1'], Pa3['KE MOI 1'], Pa4['KE MOI 1'], Pa8['KE MOI 1'], Pa13['KE MOI 1']]
KE10 = [g50071['KE MOI 10'], Pa3['KE MOI 10'], Pa4['KE MOI 10'], Pa8['KE MOI 10'], Pa13['KE MOI 10']]
KE50 = [g50071['KE MOI 50'], Pa3['KE MOI 50'], Pa4['KE MOI 50'], Pa8['KE MOI 50'], Pa13['KE MOI 50']]
KE100 = [g50071['KE MOI 100'], Pa3['KE MOI 100'], Pa4['KE MOI 100'], Pa8['KE MOI 100'], Pa13['KE MOI 100']]

auc_list_1 = [auc(time_data_hours, KE1[i]) for i in range(len(KE1))]
auc_list_10 = [auc(time_data_hours, KE10[i]) for i in range(len(KE10))]
auc_list_50 = [auc(time_data_hours, KE50[i]) for i in range(len(KE50))]
auc_list_100 = [auc(time_data_hours, KE100[i]) for i in range(len(KE100))]

# Correlation calculation
strain = ['50071', 'Pa3', 'Pa4', 'Pa8', 'Pa13']
latency_period = [10, 10, 30, 10, 10]
burst_size = [1.17, 1.14, None, 1.54, 1.07]
adsorption_rate = [9.29E-11, 3.46E-10, 1.61E-10, 3.28E-10, 2.44E-10]
# latency period is NOT normally distributed
print(f'Latency period: {shapiro(latency_period)}, Burst size: {shapiro(burst_size)}, '
      f'Adsorption rate: {shapiro(adsorption_rate)}')
data_for_corr = {'strain': strain, 'KE AUC': auc_list_10, 'latency_period': latency_period,
                 'burst_size': burst_size, 'adsorption_rate': adsorption_rate}
df_corr = pd.DataFrame(data_for_corr, columns=['KE AUC', 'latency_period', 'burst_size', 'adsorption_rate'],
                       index=strain)
corr_matrix = df_corr.corr(method='kendall')
# https://statisticseasily.com/kendall-tau-b-vs-spearman/
mask = np.triu(np.ones(corr_matrix.shape), k=1).astype('bool')
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrix, mask=mask, annot=True, ax=ax2, cmap='RdBu',
            cbar_kws={'label': 'Kendall rank correlation coefficient'},
            xticklabels=['KE AUC', 'Latency period', 'Burst size', 'Adsorption rate'],
            yticklabels=['KE AUC', 'Latency period', 'Burst size', 'Adsorption rate'])
plt.title('Correlation matrix MOI 10')
plt.tight_layout()
plt.savefig('../pythonProject/correlation_matrix.png', dpi=600)
plt.cla()
plt.clf()

# ANOVA on MOIs
print(f'Shapiro AUC MOI 1: {shapiro(auc_list_1)}, Shapiro AUC MOI 10: {shapiro(auc_list_10)}, '
      f'Shapiro AUC MOI 50: {shapiro(auc_list_50)}, Shapiro AUC MOI 100: {shapiro(auc_list_100)}')
kruskal_results_auc_all_mois = kruskal(auc_list_1, auc_list_10, auc_list_50, auc_list_100)
print(f'Kruskal results: {kruskal_results_auc_all_mois}')
anova_results_auc_all_mois = f_oneway(auc_list_1, auc_list_10, auc_list_50, auc_list_100)
print(f'ANOVA results: {anova_results_auc_all_mois}')

hue_anova = [['1'] * 5, ['10'] * 5, ['50'] * 5, ['100'] * 5]
hue_anova = flatten(hue_anova)
ke_auc_for_anova_combinded = [auc_list_1, auc_list_10, auc_list_50, auc_list_100]
ke_auc_for_anova_combinded = flatten(ke_auc_for_anova_combinded)
data_for_anova = {'KE AUC': ke_auc_for_anova_combinded, 'Hue': hue_anova}
df_for_anova = pd.DataFrame(data_for_anova, columns=['KE AUC', 'Hue'])

fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_for_anova, x='Hue', y='KE AUC', palette='RdBu', hue='Hue', ax=ax4)
plt.ylabel('KE AUC')
plt.title('KE AUC across all strains for each MOI')
plt.text(x=2, y=610, bbox=dict(facecolor='darkred', alpha=0.5), 
         s=f'Does the MOI have an influence on KE?\nANOVA results -> F-value: {anova_results_auc_all_mois[0]:.2f}; P-value: {anova_results_auc_all_mois[1]:.2f}')
#plt.ylim(-60, 110)
plt.xlabel('MOI')
plt.tight_layout()
plt.savefig('../pythonProject/boxplot_ke_moi.png', dpi=600)
plt.cla()
plt.clf()

#regression plot
data_for_reg = {'KE AUC': auc_list_10, 'Latency period': latency_period}
df_for_reg = pd.DataFrame(data_for_reg, columns=['KE AUC', 'Latency period'])

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.regplot(data=df_for_reg, x='KE AUC', y='Latency period', ax=ax3, ci=None, marker='x', color='.3',
            line_kws=dict(color='b'))
plt.title('Regression plot KE AUC vs Latency period')
plt.xlabel('KE AUC')
plt.ylabel('Latency period')
plt.xlim(750, 1350)
plt.ylim(5, 35)
plt.tight_layout()
plt.savefig('../pythonProject/regplot_ke_auc_latency.png', dpi=600)
