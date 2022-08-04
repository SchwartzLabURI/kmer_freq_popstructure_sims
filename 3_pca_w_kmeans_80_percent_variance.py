import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from os import listdir
from os.path import isfile, join
import pickle

'''
Modules used:
module load matplotlib/3.3.3-intel-2020b
module load SciPy-bundle/2020.11-intel-2020b
module load scikit-learn/0.23.2-intel-2020b
'''

def get_num_pcs(expl_var):
    list_of_var_vals = list(expl_var)
    cum_val = 0.0
    num_PCs = 0
    for i in list_of_var_vals:
            percnt = float(i) * 100
            cum_val += percnt
            if(cum_val >= 80.0):
                num_PCs = int(list_of_var_vals.index(i)) + 1
                break;
    return (cum_val, num_PCs)

############## Setup

pickled_dictionary_path = sys.argv[1]
pickled_dictionary_filtered = pickled_dictionary_path + '/filterdict.pkl' 
kmer_frequencies_dictionary = pickle.load( open( pickled_dictionary_filtered, "rb" ) )


df = pd.DataFrame(kmer_frequencies_dictionary)

#population = ['P1_1', 'P1_2', 'P1_3', 'P1_4', 'P1_5', 'P1_6', 
#	      'P2_1', 'P2_2', 'P2_3', 'P2_4', 'P2_5', 'P2_6']

#get sorted fastas and trim ends of names to get sample labels
sortedfiles = listdir(pickled_dictionary_path)
fa_sorted = [f for f in sortedfiles if f.endswith('_mers_sorted.fa')]
samples = [s.split('_') for s in fa_sorted]
population = ['_'.join(s[:-3]) for s in samples]
population.sort()

#get just population names (targets in PCA)
targets = list(set(['_'.join(s[:-4]) for s in samples])) #uniques
targets.sort()

df['Population'] = population

features = df.columns.tolist()[0:-1] #['AAAAAAAAAAAAAAAAAAAAA', ... , 'TTTTTTTTTTCAAAAAAAAAA']

x = df.loc[:, features].values
y = df.loc[:,['Population']].values
std_x = StandardScaler().fit_transform(x)


#################

pca = PCA(n_components = len(population)) #use num samples
principalComponents = pca.fit_transform(std_x)

cum_val, num_PCs = get_num_pcs(pca.explained_variance_ratio_) #this tells us how many PCs are needed for >= 80% of the variance
print(cum_val, num_PCs) #double check that its about 80% and 21 PCs

list_of_column_headers = [] #for dataframe

for i in range(1, pca.n_components_+1, 1):
    col_label = 'principal component ' + str(i)
    list_of_column_headers.append(col_label)

principalDf = pd.DataFrame(data = principalComponents, columns = list_of_column_headers) #['principal component 1', 'principal component 2', 'principal component 3', 'principal component 4', 'principal component 5']

finalDf = pd.concat([principalDf, df[['Population']]], axis = 1) #add a column with populations


#Visualize 2D Projection 80%
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
plt.xlabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[0]*100), fontsize = 11)
plt.ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100), fontsize = 11)

#targets = ['P1', 'P2'] #, 'EAS_JPT', 'EUR_TSI', 'SAS_ITU'] #make sure they are listed in the correct order
colors = ['m', 'r', 'g', 'b', 'y', 'c', 'k', 'w']
colors = colors[:len(targets)]
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['Population'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()
plt.savefig(pickled_dictionary_path+"/2D_PCA_80_prcn_variance.pdf")
plt.clf() #clear the plt variable so the plots don't overlap

#TRYING TO MAKE PLOT WORK
import numpy as np
n = len(population)/len(targets) #assumes equal sample per population
c2 = list(np.repeat(colors, n))

plt.scatter(finalDf['principal component 1'], finalDf['principal component 2'], c=c2) 
plt.xlabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[0]*100), fontsize = 11)
plt.ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100), fontsize = 11)
plt.savefig(pickled_dictionary_path+"/2PC_pop_plot_80percent.pdf")
plt.clf() #clear the plt variable so the plots don't overlap

#just 2 pcs NOT 80%
#PCA Projection to 2D
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(std_x)

principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
finalDf = pd.concat([principalDf, df[['Population']]], axis = 1) #add a column with populations

plt.scatter(finalDf['principal component 1'], finalDf['principal component 2'], c=c2)
plt.xlabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[0]*100), fontsize = 11)
plt.ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100), fontsize = 11)
plt.savefig(pickled_dictionary_path+"/2PC_pop_plot.pdf")
plt.clf() #clear the plt variable so the plots don't overlap

#Clustering with K-means
inertias = []
ks = range(1, 10)
# Creating 10 K-Mean models while varying the number of clusters (k)
for k in range(1,10):
    model = KMeans(n_clusters=k)

    # Fit model to samples
    model.fit(finalDf.iloc[:,:2]) #2 pcs

    # Append the inertia to the list of inertias
    inertias.append(model.inertia_)

plt.plot(range(1,10), inertias, '-p', color='gold')
plt.xlabel('number of clusters, k')
plt.ylabel('inertia')
plt.xticks(ks)
plt.savefig(pickled_dictionary_path+"/elbow_method_plot_2pcs.pdf")
plt.clf() #clear the plt variable so the plots don't overlap

model = KMeans(n_clusters=3)#double check that it actually is three from the elbow plot

model.fit(finalDf.iloc[:,:2]) #build a model from 2pcs      #the number of PCs that hold 80% of the variance

labels = model.predict(finalDf.iloc[:,:2])

plt.scatter(finalDf['principal component 1'], finalDf['principal component 2'], c=labels) #from the model trained on plot the first 2PCs
plt.xlabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[0]*100), fontsize = 11)
plt.ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100), fontsize = 11)
plt.savefig(pickled_dictionary_path+"/k_means_clustering_2PC.pdf")
plt.clf() #clear the plt variable so the plots don't overlap
