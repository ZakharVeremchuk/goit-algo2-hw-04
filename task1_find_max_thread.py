import networkx as nx
from collections import deque

# 1. Створення графа
G = nx.DiGraph()
edges = [
    ('Термінал 1', 'Cклад 1', 25), ('Термінал 1', 'Cклад 2', 20), ('Термінал 1', 'Cклад 3', 15),
    ('Термінал 2', 'Cклад 3', 15), ('Термінал 2', 'Cклад 4', 30), ('Термінал 2', 'Cклад 2', 10),
    ('Cклад 1', 'Магазин 1', 15), ('Cклад 1', 'Магазин 2', 10), ('Cклад 1', 'Магазин 3', 20),
    ('Cклад 2', 'Магазин 4', 15), ('Cклад 2', 'Магазин 5', 10), ('Cклад 2', 'Магазин 6', 25),
    ('Cклад 3', 'Магазин 7', 20), ('Cклад 3', 'Магазин 8', 15), ('Cклад 3', 'Магазин 9', 10),
    ('Cклад 4', 'Магазин 10', 20), ('Cклад 4', 'Магазин 11', 10), ('Cклад 4', 'Магазин 12', 15),
    ('Cклад 4', 'Магазин 13', 5), ('Cклад 4', 'Магазин 14', 10)
]
G.add_weighted_edges_from(edges)

# 2. Додаємо Суперджерело та Суперстік
terminals = ['Термінал 1', 'Термінал 2']
shops = [n for n in G.nodes if 'Магазин' in n]

for t in terminals:
    G.add_edge('S-Source', t, weight=float('inf'))
for s in shops:
    G.add_edge(s, 'S-Sink', weight=float('inf'))

# 3. Перетворення назв вузлів у індекси для алгоритму
nodes = list(G.nodes())
node_to_idx = {node: i for i, node in enumerate(nodes)}
idx_to_node = {i: node for i, node in enumerate(nodes)}
num_nodes = len(nodes)

# Автоматичне створення матриці пропускної здатності
capacity_matrix = [[0] * num_nodes for _ in range(num_nodes)]
for u, v, d in G.edges(data=True):
    capacity_matrix[node_to_idx[u]][node_to_idx[v]] = d['weight']

def bfs(capacity, flow, source, sink, parent):
    visited = [False] * len(capacity)
    queue = deque([source])
    visited[source] = True
    while queue:
        u = queue.popleft()
        for v in range(len(capacity)):
            if not visited[v] and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                visited[v] = True
                if v == sink: return True
                queue.append(v)
    return False

def edmonds_karp(capacity, source, sink):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    max_f = 0
    parent = [-1] * n
    while bfs(capacity, flow, source, sink, parent):
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, capacity[parent[s]][s] - flow[parent[s]][s])
            s = parent[s]
        max_f += path_flow
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = parent[v]
    return max_f

# Виконання
source_idx = node_to_idx['S-Source']
sink_idx = node_to_idx['S-Sink']

if __name__ == "__main__":
    max_flow_value = edmonds_karp(capacity_matrix, source_idx, sink_idx)
    print(f"Загальний максимальний потік у мережі: {max_flow_value}")