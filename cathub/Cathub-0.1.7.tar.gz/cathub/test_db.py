from cathub.cathubsql import *
from pandas import read_pickle, read_csv
db = CathubSQL()#'tests/aayush/MontoyaChallenge2015.db')


#print(db.get_atoms_for_publication('PengRole2020'))

dataframe = db.get_dataframe(pub_id='PengRole2020',
                             include_atoms=True, ##'PengRole2020.db',
                             reactants=['COgas'],
                             products=['COstar'],
                             elements=['Cu', 'Al'],
                             #surface_composition='Cu',
                             facet = '100'
    
)

#print(dataframe)

#dataframe.to_pickle('Peng.pickle')

df = read_pickle('Peng.pickle')
#df = read_csv('Peng')
print(df)

from ase.visualize import view
view(df['atoms'][0])
#print(dataframe['atoms'][0][0])

#print(dataframe[['equation']].values)

