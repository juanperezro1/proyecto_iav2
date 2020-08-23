

"""
a=[1,2,3]
b=[4,5,6] 
c = [a, b] 
with open("list1.txt", "w") as file:
    for x in zip(*c):
        file.write("{0}\t{1}\n".format(*x))
"""

"""
DFS with children visited in sorted order.
Nodes must be sortable.
Basic algorithms for depth-first searching.
Based on http://www.ics.uci.edu/~eppstein/PADS/DFS.py
by D. Eppstein, July 2004.
"""



def dfs_predecessors(G, source=None):
    """Return dictionary of predecessors in depth-first-search from source."""
    return dict((t,s) for s,t in dfs_edges(G,source=source))


def dfs_successors(G, source=None):
    """Return dictionary of successors in depth-first-search from source."""
    d=defaultdict(list)
    for s,t in dfs_edges(G,source=source):
        d[s].append(t)
    return dict(d)


def dfs_postorder_nodes(G,source=None):
    """Produce nodes in a depth-first-search post-ordering starting 
    from source.
    """
    post=(v for u,v,d in dfs_labeled_edges(G,source=source)
          if d['dir']=='reverse')
    # chain source to end of pre-ordering
#    return chain(post,[source])
    return post


def dfs_preorder_nodes(G,source=None):
    """Produce nodes in a depth-first-search pre-ordering starting at source."""
    pre=(v for u,v,d in dfs_labeled_edges(G,source=source) 
         if d['dir']=='forward')
    # chain source to beginning of pre-ordering
#    return chain([source],pre)
    return pre


def dfs_labeled_edges(G,source=None):
    """Produce edges in a depth-first-search starting at source and
    labeled by direction type (forward, reverse, nontree).
    """
    # Based on http://www.ics.uci.edu/~eppstein/PADS/DFS.py
    # by D. Eppstein, July 2004.
    if source is None:
        # produce edges for all components
        nodes=G
    else:
        # produce edges for components with source
        nodes=[source]
    visited=set()
    for start in nodes:
        if start in visited:
            continue
        yield start,start,{'dir':'forward'}
        visited.add(start)
        stack = [(start,iter(sorted(G[start])))]
        while stack:
            parent,children = stack[-1]
            try:
                child = next(children)
                if child in visited:
                    yield parent,child,{'dir':'nontree'}
                else:
                    yield parent,child,{'dir':'forward'}
                    visited.add(child)
                    stack.append((child,iter(sorted(G[child]))))
            except StopIteration:
                stack.pop()
                if stack:
                    yield stack[-1][0],parent,{'dir':'reverse'}
        yield start,start,{'dir':'reverse'}

if __name__ == '__main__':
    print("dfs")
    G = nx.Graph()
    G.add_edge('start','apple')
    G.add_edge('start','banana')
    G.add_edge('start','cherry')
    G.add_edge('banana','split')
    G.add_edge('banana','pie')
    print(list(nx.dfs_labeled_edges(G,'start')))
    print(list(dfs_labeled_edges(G,'start')))
    print(list(nx.dfs_preorder_nodes(G,'start')))
    print(list(dfs_preorder_nodes(G,'start')))
