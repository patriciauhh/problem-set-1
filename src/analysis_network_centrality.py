'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Guild a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class 
'''
import json
import pandas as pd
import networkx as nx
import requests
from datetime import datetime
import matplotlib.pyplot as plt 

# url to the json file 
url = 'https://raw.githubusercontent.com/cbuntain/umd.inst414/main/data/imdb_movies_2000to2022.prolific.json'

# fetching json data from url 
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# debugging, just to ensure fetching data from url works 
print("First few lines of the response text:")
print(response.text[:100])


def build_graph(g, response): 
    '''
    builds graph from the json response. each actor is created as a node. 
    each edge is the relationship between each actor based on movie. 
    '''
    for line in response.iter_lines(decode_unicode=True):
        if line:
            this_movie = json.loads(line)
            actors = this_movie.get('actors', []) 
        # Create a node for every actor
            if actors: 
                for actor_id, actor_name in actors:
                    g.add_node(actor_name)
        # add the actor to the graph    
        # Iterate through the list of actors, generating all pairs
        ## Starting with the first actor in the list, generate pairs with all subsequent actors
        ## then continue to second actor in the list and repeat
                for i, (left_actor_id,left_actor_name) in enumerate(actors):
                    for right_actor_id,right_actor_name in actors[i+1:]:
                        if g.has_edge(left_actor_name, right_actor_name):
                            g[left_actor_name][right_actor_name]['weight'] += 1
                        else: 
                             g.add_edge(left_actor_name, right_actor_name, weight=1)
    return g
 
# build graph using networkx library
g = nx.Graph()
g = build_graph(g, response)   

# Check the number of nodes 
print("Number of Nodes:", len(g.nodes))

# Verify the first few nodes
print("First 10 nodes:", list(g.nodes)[:10])

# create df for edges 
edge_dict = {edge: g.edges[edge] for edge in g.edges()}
edge_df = pd.DataFrame.from_dict(edge_dict, orient='index').reset_index()
edge_df.columns = ['left_actor_name', 'right_actor_name','weight']
print(edge_df.head())

# creates a csv file from the edge dataframe that was created 

current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'edges_df{current_datetime}.csv'
edge_dict.to_csv(f'/data/{filename}', index=False)

# calculating centrality metrics 
degree_centrality = nx.degree_centrality(g)
betweenness_centrality = nx.betweenness_centrality(g)
closeness_centrality = nx.closeness_centrality(g)

# creating a dataframe from the centrality metrics of the nodes 
node_data = {
    'actor_name': list(g.nodes),
    'degree_centrality': [degree_centrality[node] for node in g.nodes],
    'betweenness_centrality': [betweenness_centrality[node] for node in g.nodes],
    'closeness_centrality': [closeness_centrality[node] for node in g.nodes]
}
node_df = pd.DataFrame(node_data)
print(node_df.head())

# creating a csv file for the centrality dataframe, 
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'network_centrality{current_datetime}.csv'
node_df.to_csv(f'/data/{filename}', index=False)

# printing the top 10 nodes based off the degree centrality 
top_10_nodes = node_df.nlargest(10, 'degree_centrality')
print("Top 10 nodes based on degree centrality:")
print(top_10_nodes)

# visualizing graph using matplot
plt.figure(figsize=(12,8))
pos = nx.spring_layout(g)
nx.draw(g, pos, with_labels=True, node_size=50, font_size=8)
plt.title("IMBD Actors")
plt.show


# calculating centrality metrics 

# notes: centrality 
# high centrality = more connections betweeness = how often it acts as a bridge 
# closeness = how close a node is to other nodes 
# (i do not know if this is functional)