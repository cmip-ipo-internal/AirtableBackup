'''
Convert the schema for each base into a node link format outlining substituted tables
'''

import json

with open('schema.json') as f:
    data = json.load(f)

nodes = set()
links = set() 
link_types = {}

for table in data:
    nodes.add(table['id'])
    
    for field in table['fields']:
        if field['type'] == 'multipleRecordLinks':
            link_name = field['name']
            linked_table = field['options']['linkedTableId']
            
            links.add((table['id'], linked_table))
            link_types[(table['id'], linked_table)] = link_name
            
print("Nodes:")
for node in nodes:
    print("-", node)
    
print("\nLinks:")
for link in links: 
    print("-", link[0], "(", link[1], ")")
    
print("\nLink Types:")   
for link, link_type in link_types.items():
    print("-", link[0], "(", link[1], "):", link_type)
