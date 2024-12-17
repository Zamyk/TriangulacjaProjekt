class Vertex:
    def __init__(self, x, y):
        self.x = x  # Współrzędna x wierzchołka
        self.y = y  # Współrzędna y wierzchołka
        self.outgoingEdge = None  # Wskaźnik na jedną z wychodzących krawędzi (HalfEdge)

    def __repr__(self):
        return f"Vertex({self.x}, {self.y})"


class HalfEdge:
    def __init__(self):
        self.origin = None  # Wskaźnik na początkowy wierzchołek (Vertex)
        self.twin = None  # Wskaźnik na drugą połowę tej samej krawędzi (HalfEdge)
        self.next = None  # Wskaźnik na następną krawędź w tej samej ścianie (HalfEdge)
        self.prev = None  # Wskaźnik na poprzednią krawędź w tej samej ścianie (HalfEdge)
        self.face = None  # Wskaźnik na ścianę, do której należy krawędź (Face)

    def __repr__(self):
        return f"HalfEdge(origin={self.origin})"


class Face:
    def __init__(self):
        self.outerEdge = None  # Wskaźnik na jedną z otaczających krawędzi (HalfEdge)

    def __repr__(self):
        return f"Face(outer_edge={self.outerEdge})"


class HalfEdgeMesh:
    def __init__(self, vertices = [], faces = [], edges = []):
        self.vertices = vertices  # Lista wszystkich wierzchołków
        self.edges = edges  # Lista wszystkich krawędzi (HalfEdge)
        self.faces = faces  # Lista wszystkich ścian (Face)

    def addVertex(self, x, y):
        vertex = Vertex(x, y)
        self.vertices.append(vertex)
        return vertex

    def addEdge(self, v1, v2):
        """
        Dodaje krawędź między wierzchołkami v1 i v2.
        Tworzy dwie HalfEdge: jedną dla kierunku v1 -> v2 i drugą dla v2 -> v1.
        """
        edge1 = HalfEdge()
        edge2 = HalfEdge()

        # Powiązanie krawędzi z wierzchołkami
        edge1.origin = v1
        edge2.origin = v2
        v1.outgoingEdge = edge1
        v2.outgoingEdge = edge2

        # Powiązanie krawędzi jako twin
        edge1.twin = edge2
        edge2.twin = edge1

        # Dodanie krawędzi do listy
        self.edges.append(edge1)
        self.edges.append(edge2)

        return edge1, edge2

    def addFace(self, edgeCycle):
        """
        Tworzy ścianę (Face) otoczoną przez cykl krawędzi edge_cycle.
        edge_cycle: lista obiektów HalfEdge tworzących zamknięty obwód.
        """
        face = Face()
        self.faces.append(face)

        # Powiązanie krawędzi z nową ścianą
        for i, edge in enumerate(edgeCycle):
            edge.face = face
            edge.next = edgeCycle[(i + 1) % len(edgeCycle)]  # Następna krawędź w cyklu
            edge.prev = edgeCycle[(i - 1) % len(edgeCycle)]  # Poprzednia krawędź w cyklu

        # Powiązanie ściany z jedną z jej krawędzi
        face.outerEdge = edgeCycle[0]

        return face

    def __repr__(self):
        return f"HalfEdgeMesh(vertices={len(self.vertices)}, edges={len(self.edges)}, faces={len(self.faces)})"


# Przykład użycia
if __name__ == "__main__":
    # Tworzymy siatkę
    mesh = HalfEdgeMesh()

    # Dodajemy wierzchołki
    v1 = mesh.addVertex(0, 0)
    v2 = mesh.addVertex(1, 0)
    v3 = mesh.addVertex(1, 1)
    v4 = mesh.addVertex(0, 1)

    # Dodajemy krawędzie
    e1, e2 = mesh.addEdge(v1, v2)
    e3, e4 = mesh.addEdge(v2, v3)
    e5, e6 = mesh.addEdge(v3, v4)
    e7, e8 = mesh.addEdge(v4, v1)

    # Tworzymy ścianę (Face)
    face = mesh.addFace([e1, e3, e5, e7])

    print(mesh)
    print("Vertices:", mesh.vertices)
    print("Edges:", mesh.edges)
    print("Faces:", mesh.faces)