# Trying out some general pathfinding

edges = [
    ('a', 'b', 4),
    ('a', 'c', 8),
    ('b', 'c', 11),
    ('b', 'd', 2),
    ('b', 'e', 6),
    ('c', 'd', 4),
    ('c', 'f', 5),
    ('d', 'e', 3),
    ('d', 'f', 2),
    ('e', 'g', 7),
    ('f', 'g', 4)
]
edges = [
    (0, 1, 4),
    (0, 7, 8),
    (1, 2, 8),
    (1, 7, 11),
    (2, 3, 7),
    (2, 5, 4),
    (2, 8, 2),
    (3, 4, 9),
    (3, 5, 14),
    (4, 5, 10),
    (5, 6, 2),
    (6, 7, 1),
    (6, 8, 6),
    (7, 8, 7),
]

# nodes = set(i for i, j, d in edges).union(set(j for i, j, d in edges))

def calc_shorts(edges, start):
    dist = {start: 0}
    # Look at neighbors
    new = list(dist.keys())
    while len(new) > 0:
        cur = new.pop()
        opts = [(i, j, d) for i, j, d in edges if i == cur] + [(j, i, d) for i, j, d in edges if j == cur]
        for i, j, d in opts:
            if j not in dist:
                dist[j] = dist[cur] + d
                new.append(j)
            elif dist[j] > dist[cur] + d:
                dist[j] = dist[cur] + d
                new.append(j)
    return dist

mins = calc_shorts(edges, (15, 1, '>'))
mins[(1, 15, '>')]
mins[(1, 15, '^')]
