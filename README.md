# Data-visualization-Wikipedia

On wikipedia page are link to each other by link (reference to other wikipedia pages). Here I use these links to draw the graph network of wikipedia pages related to the artificial inteligence field. I also use this graph to find pages communities.

## Extracting data from the wikipedia API

### Find all the nodes of selected categories

```python
import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('en')

Nodes = []

# list of pages in each category
def catmembers(categorymembers,level,max_level):
        for c in categorymembers.values():
            if 'Category:' not in c.title:
                Nodes.append(c.title)
            if 'Category:' in c.title and level < max_level:
                catmembers(c.categorymembers, level = level+1, max_level = max_level)             

#  Selected category 
cat_ml = wiki_wiki.page("Category:Machine learning")
cat_dm = wiki_wiki.page("Category:data mining")
cat_ai = wiki_wiki.page("Category:artificial intelligence")
cat_dt = wiki_wiki.page("Category:decision theory")
cat_sc = wiki_wiki.page("Category:Statistical classification")
cat_da = wiki_wiki.page("Category:Data analysis")

print("Category members: Category:Machine learning")
catmembers({**cat_ml.categorymembers, 
            **cat_dm.categorymembers,
            **cat_ai.categorymembers,
            **cat_dt.categorymembers,
            **cat_sc.categorymembers,
            **cat_da.categorymembers},level = 0, max_level = 1)

Nodes = list(set(Nodes)) # delate any duplicate
```

### Find all links between pages of previously selected pages

```python
edge = [] #list of edges in the graph
for page in Nodes :
    Links = wiki_wiki.page(page).links
    for link in Links :
        if link in Nodes : #only select links between nodes selected before
            edge.append((page,link)) 
```

### Save data

```python
import pandas as pd

df_edge = pd.DataFrame(edge)
df_edge.columns = ['from','to']

df_vertex = pd.DataFrame(Nodes)
df_vertex.columns = ['vertex']

df_edge.to_csv('edge.csv',index = False, header = False)
df_vertex.to_csv('vertex.csv',index = False, header = False)
```
## Plot the network of pages between pages related tho AI

By uploading the edges and nodes data in [Gephi](https://gephi.org/) the following plot can be obtained.

![Wikipedia AI related pages network](https://github.com/QuentinMas/Data-visualization-Wikipedia/blob/main/AI_wiki_page_network.png)

< *Spatialisation algorithm : Force Atlas* >


The different color represent communities. These [communities](https://en.wikipedia.org/wiki/Community_structure) represent group of pages that have a lot of link to each others. Here they can also represent page categories.

![Wikipedia AI related pages network with communities names](https://github.com/QuentinMas/Data-visualization-Wikipedia/blob/main/AI_wiki_page_network_communities.png)

The center of the graph is the page [Artificial Inteligence](https://en.wikipedia.org/wiki/Artificial_intelligence) and the farest we go from the center the less the pages are about artificial inteligence. For instance the farest pages from the center (top-left) are about [botnets](https://en.wikipedia.org/wiki/Botnet) which are not realy linked to artificial inteligence. But from the page [botnets](https://en.wikipedia.org/wiki/Botnet) you can find a link to the page [robot](https://en.wikipedia.org/wiki/Robot) which gives you a link to the page [artificial inteligence](https://en.wikipedia.org/wiki/Artificial_intelligence).
