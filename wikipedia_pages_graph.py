import wikipediaapi
import pandas as pd
from tqdm import tqdm

wiki_wiki = wikipediaapi.Wikipedia('en')

Nodes = []

# find all the pages in a category
def catmembers(categorymembers,level,max_level):
        for c in categorymembers.values():
            if 'Category:' not in c.title:
                Nodes.append(c.title)
            if 'Category:' in c.title and level < max_level:
                catmembers(c.categorymembers, level = level+1, max_level = max_level)
                
cat_ml = wiki_wiki.page("Category:Machine learning")
cat_dm = wiki_wiki.page("Category:data mining")
cat_ai = wiki_wiki.page("Category:artificial intelligence")
cat_dt = wiki_wiki.page("Category:decision theory")
cat_sc = wiki_wiki.page("Category:Statistical classification")
cat_da = wiki_wiki.page("Category:Data analysis")

catmembers({**cat_ml.categorymembers, 
            **cat_dm.categorymembers,
            **cat_ai.categorymembers,
            **cat_dt.categorymembers,
            **cat_sc.categorymembers,
            **cat_da.categorymembers},level = 0, max_level = 1)

Nodes = list(set(Nodes)) # delate any duplicate 

edge = []
for page in tqdm(Nodes) :
    Links = wiki_wiki.page(page).links
    for link in Links :
        if link in Nodes : 
            edge.append((page,link))           
                   
df_edge = pd.DataFrame(edge)
df_edge.columns = ['from','to']

df_vertex = pd.DataFrame(Nodes)
df_vertex.columns = ['vertex']

# write dataframe in a .csv to use it in Gephi
df_edge.to_csv('edge.csv',index = False, header = False)
df_vertex.to_csv('vertex.csv',index = False, header = False)