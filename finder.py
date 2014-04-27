import MySQLdb
import networkx as nx

class Finder:
    @staticmethod
    def findRoute(src,dest):
        G = nx.Graph()
        db = MySQLdb.connect(host = "localhost", user = "root", passwd = "", db = "project")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM nodes")
        for row in cursor.fetchall():
            G.add_node(int(row[0]))
         
        cursor.execute("SELECT * FROM lanes")
        for row in cursor.fetchall():
            G.add_edge(int(row[1]), int(row[2]))
            G[row[1]][row[2]]['weight'] = row[3]
         
        print G.edges()
        print G.nodes()
         
        #src = raw_input("Enter source: ")
        #dest = raw_input("Enter destination: ")
        query = "SELECT node_id FROM locations WHERE name = '" + src + "' OR name = '" + dest +"'"
        cursor.execute(query)
        try:
            fetch = cursor.fetchall()
            source = fetch[0][0]
            destination = fetch[1][0]
            F = nx.bidirectional_dijkstra(G, source, destination, weight = 'weight')
            print F[1]
         
            A = []
            cursor.execute("SELECT node_id, x, y from nodes")
            results = cursor.fetchall()
            for x in F[1]:
                for row in results:
                    if x == row[0]:
                        A.append((row[1],row[2]))
            return A
            
        except:
            print "Invalid Query"
            return []
            
    @staticmethod
    def findNeighbours(src, dest):
        
        G = nx.Graph()
        db = MySQLdb.connect(host = "localhost", user = "root", passwd = "", db = "project")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM nodes")
        for row in cursor.fetchall():
            G.add_node(int(row[0]))
         
        cursor.execute("SELECT * FROM lanes")
        for row in cursor.fetchall():
            G.add_edge(int(row[1]), int(row[2]))
            G[row[1]][row[2]]['weight'] = row[3]
         
        print G.edges()
        print G.nodes()
        
        query = "SELECT node_id FROM locations WHERE name like '" + src + "'"
        cursor.execute(query)
        try:
            fetch = cursor.fetchall()
            source = fetch[0][0]

            query = "SELECT node_id FROM locations WHERE type = '" + dest + "'"
            print query
            cursor.execute(query)
            results = cursor.fetchall()
            print results
            
            F = []
            for x in results:
                temp = nx.bidirectional_dijkstra(G, source, int(x[0]), weight = 'weight')
                F.append(temp)
            
            maxval = min(F[0:])
            index = []
            for ctr in range(len(F)):
                if F[ctr][0] == maxval[0]:
                    index.append(ctr)

            cursor.execute("SELECT nodes.node_id, nodes.x, nodes.y, name from nodes left join locations on nodes.node_id = locations.node_id")
            results = cursor.fetchall()
            Pathlist = []
            for y in index:
                A = []
                for x in F[y][1]:
                    for row in results:
                        if x == row[0]:
                            A.append((row[1],row[2],row[3]))
                Pathlist.append(A)
                
            return Pathlist
            
        except:
            print "Invalid Query"
            return []
