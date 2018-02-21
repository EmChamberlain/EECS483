def toposort(edges):
    # edge[0] depends on edge[1]    edge[0] <---- edge[1]
    vertices = set([])

    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])

    S = []

    for vertex in vertices:
        incoming_edge = False
        for edge in edges:
            if edge[0] == vertex:
                incoming_edge = True
                break
        if not incoming_edge:
            S.append(vertex)

    if len(S) == 0:
        return S, False

    L = []
    while len(S) > 0:
        S.sort(reverse=True) # this should handle the ascii sort but it is not very performant
        n = S.pop()
        L.append(n)
        x = 0
        while x < len(edges):
            edge = edges[x]
            x += 1
            if edge[1] == n:
                m = edge[0]
                edges.remove(edge)
                x -= 1
                incoming_edge = False
                for edge in edges:
                    if edge[0] == m:
                        incoming_edge = True
                        break
                if not incoming_edge:
                    S.append(m)

    if len(edges) != 0:
        return edges, False
    return L, True
