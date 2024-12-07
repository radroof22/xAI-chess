import chess
import networkx as nx
import matplotlib.pyplot as plt

def get_pos_obj(board_position: str) -> "chess-like-object":
    mapping = {
    'a1': chess.A1, 
    'a2': chess.A2, 
    'a3': chess.A3, 
    'a4': chess.A4, 
    'a5': chess.A5, 
    'a6': chess.A6, 
    'a7': chess.A7, 
    'a8': chess.A8,
    'b1': chess.B1, 
    'b2': chess.B2, 
    'b3': chess.B3, 
    'b4': chess.B4, 
    'b5': chess.B5, 
    'b6': chess.B6, 
    'b7': chess.B7, 
    'b8': chess.B8,
    'c1': chess.C1, 
    'c2': chess.C2, 
    'c3': chess.C3, 
    'c4': chess.C4, 
    'c5': chess.C5, 
    'c6': chess.C6, 
    'c7': chess.C7, 
    'c8': chess.C8,
    'd1': chess.D1, 
    'd2': chess.D2, 
    'd3': chess.D3, 
    'd4': chess.D4, 
    'd5': chess.D5, 
    'd6': chess.D6, 
    'd7': chess.D7, 
    'd8': chess.D8,
    'e1': chess.E1, 
    'e2': chess.E2, 
    'e3': chess.E3, 
    'e4': chess.E4, 
    'e5': chess.E5, 
    'e6': chess.E6, 
    'e7': chess.E7, 
    'e8': chess.E8,
    'f1': chess.F1, 
    'f2': chess.F2, 
    'f3': chess.F3, 
    'f4': chess.F4, 
    'f5': chess.F5, 
    'f6': chess.F6, 
    'f7': chess.F7, 
    'f8': chess.F8,
    'g1': chess.G1, 
    'g2': chess.G2, 
    'g3': chess.G3, 
    'g4': chess.G4, 
    'g5': chess.G5, 
    'g6': chess.G6, 
    'g7': chess.G7, 
    'g8': chess.G8,
    'h1': chess.H1, 
    'h2': chess.H2, 
    'h3': chess.H3, 
    'h4': chess.H4, 
    'h5': chess.H5, 
    'h6': chess.H6, 
    'h7': chess.H7, 
    'h8': chess.H8
    }
    return mapping[board_position]

def get_all_pos():
    return ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']

def pos_to_index_mapping(pos):
    rows = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
    cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    return (rows[pos[1]], cols[pos[0]])

def dfs(curr_node, graph, visited_set):
    visited_set.add(curr_node)
    if (curr_node in graph):
        for neighbor in graph[curr_node]:
            if (neighbor not in visited_set):
                dfs(neighbor, graph, visited_set)
    return


def visualize_directed_graph(graph):
    """
    Visualize a directed graph
    """

    G = nx.DiGraph()
    
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    
    plt.figure(figsize=(4, 4))
    pos = nx.spring_layout(G) 
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=75, font_size=6, font_weight='bold', edge_color='gray', arrows=True)

    edge_labels = {edge: '' for edge in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title("Directed Graph Visualization")
    plt.show()


def read_fens(file_path):
    """
    Return list of FENs stored in file
    """
    with open(file_path, 'r') as file:
        fens = [line.strip() for line in file if line.strip()]
    return fens 