import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

def flatten(xss):
    return [x for xs in xss for x in xs]

g50071 = pd.read_excel('data_summary.xlsx', sheet_name='50071')
g50071 = g50071.drop(0)
Pa3 = pd.read_excel('data_summary.xlsx', sheet_name='Pa3')
Pa3 = Pa3.drop(0)
Pa4 = pd.read_excel('data_summary.xlsx', sheet_name='Pa4')
Pa4 = Pa4.drop(0)
Pa8 = pd.read_excel('data_summary.xlsx', sheet_name='Pa8')
Pa8 = Pa8.drop(0)
Pa13 = pd.read_excel('data_summary.xlsx', sheet_name='Pa13')
Pa13 = Pa13.drop(0)

time = [g50071['Time(min)']]
time = time * 5
time = flatten(time)

# Convert time strings to seconds for plotting
time_data = [int(t.split(":")[0]) * 60 + int(t.split(":")[1]) + (int(t.split(":")[0]) / 60) for t in time]
time_data_hours = [t / 60 for t in time_data]

KE = [g50071['KE MOI 1'], g50071['KE MOI 10'], g50071['KE MOI 50'], g50071['KE MOI 100'],
      Pa3['KE MOI 1'], Pa3['KE MOI 10'], Pa3['KE MOI 50'], Pa3['KE MOI 100'],
      Pa4['KE MOI 1'], Pa4['KE MOI 10'], Pa4['KE MOI 50'], Pa4['KE MOI 100'],
      Pa8['KE MOI 1'], Pa8['KE MOI 10'], Pa8['KE MOI 50'], Pa8['KE MOI 100'],
      Pa13['KE MOI 1'], Pa13['KE MOI 10'], Pa13['KE MOI 50'], Pa13['KE MOI 100']]
KE10 = [g50071['KE MOI 10'], Pa3['KE MOI 10'], Pa4['KE MOI 10'], Pa8['KE MOI 10'], Pa13['KE MOI 10']]
KE10 = flatten(KE10)
hue = [['50071 MOI 1'] * len(g50071), ['50071 MOI 10'] * len(g50071), ['50071 MOI 50'] * len(g50071),
       ['50071 MOI 100'] * len(g50071),
       ['Pa3 MOI 1 '] * len(g50071), ['Pa3 MOI 10'] * len(g50071), ['Pa3 MOI 50'] * len(g50071),
       ['Pa3 MOI 100'] * len(g50071),
       ['Pa4 MOI 1'] * len(g50071), ['Pa4 MOI 10'] * len(g50071), ['Pa4 MOI 50'] * len(g50071),
       ['Pa4 MOI 100'] * len(g50071),
       ['Pa8 MOI 1'] * len(g50071), ['Pa8 MOI 10'] * len(g50071), ['Pa8 MOI 50'] * len(g50071),
       ['Pa8 MOI 100'] * len(g50071),
       ['Pa13 MOI 1'] * len(g50071), ['Pa13 MOI 10'] * len(g50071), ['Pa13 MOI 50'] * len(g50071),
       ['Pa13 MOI 100'] * len(g50071)]
hue10 = [['50071'] * len(g50071), ['Pa3'] * len(g50071), ['Pa4'] * len(g50071),
         ['Pa8'] * len(g50071), ['Pa13'] * len(g50071),]
hue10 = flatten(hue10)
data_for_df = {'Time(h)': time_data_hours, 'KE': KE10, 'Hue': hue10}
df = pd.DataFrame(data=data_for_df, columns=['Time(h)', 'KE', 'Hue'])
marker = itertools.cycle(['o', '^', '*', '8', 's', 'p', 'd', 'v'])
markers = [next(marker) for i in df["Hue"].unique()]
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df, x='Time(h)', y='KE', hue='Hue', ax=ax, markers=markers, palette='RdBu', linewidth=3)
ax.set_ylim(-20, 100)
ax.set_xlim(0, 25)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
ax.set_ylabel('Phage Killing Efficiency (%)', fontsize=16)

ax.set_xlabel('Time (h)', fontsize=16)

ax.legend(bbox_to_anchor=(0.79, 0.99), loc='upper left', fontsize=16, title_fontsize=16, title='MOI 10')
plt.tight_layout()
plt.savefig('plot_kinetics.png', dpi=600)
plt.clf()
plt.cla()
