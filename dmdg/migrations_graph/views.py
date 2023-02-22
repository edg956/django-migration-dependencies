from collections import namedtuple

from django.apps import apps
from django.db.migrations.graph import Node
from django.db.migrations.loader import MigrationLoader
from django.shortcuts import render


Migration = namedtuple("Migration", ("id", "name", "parent"))
App = namedtuple("App", ("id", "name"))
Edge = namedtuple("Edge", ("id", "source", "target"))


def make_migration(node: Node) -> Migration:
    return Migration(
        id=f"{node.key[0]}-{node.key[1]}",
        name=node.key[1],
        parent=node.key[0]
    )


def make_app(node: Node) -> App:
    return App(id=node.key[0], name=node.key[0])


def make_edge(migration_a: Migration, migration_b: Migration) -> Edge:
    edge = Edge(
        id=f"{migration_a.id}-{migration_b.id}",
        source=migration_a.id,
        target=migration_b.id
    )
    print(f"------ created edge: {edge.id}")
    return edge


def index(request):
    include = request.GET.get('include', None)
    exclude = request.GET.get('exclude', "")

    loader = MigrationLoader(None)

    if include:
        include = include.split(',')
    else:
        include = [app.label for app in apps.get_app_configs()]

    root_keys = [
        root_keys
        for app in include if app not in exclude
        for root_keys in loader.graph.root_nodes(app)
    ]

    visited = set()
    apps_set = set()
    migrations = set()
    edges = set()
    for root_key in root_keys:
        root_node = loader.graph.node_map[root_key]

        nodes_to_visit = [root_node]
        while nodes_to_visit:
            node = nodes_to_visit.pop(0)

            if node in visited:
                continue

            migration = make_migration(node)

            visited.add(node)
            migrations.add(migration)
            apps_set.add(make_app(node))

            for parent in node.parents:

                parent_migration = make_migration(parent)

                migrations.add(parent_migration)
                apps_set.add(make_app(parent))
                edges.add(make_edge(parent_migration, migration))

            if root_node.key[0] != node.key[0]:
                # It's coming from a different app, we won't look into their downstream tree
                continue

            for child in node.children:
                if child not in nodes_to_visit and child not in visited:
                    nodes_to_visit.append(child)

    nodes = [
        dict(id=app.id, name=app.name, type="app")
        for app in apps_set
    ] + [ # noqa
        dict(id=migration.id, name=migration.name, parent=migration.parent, type="migration")
        for migration in migrations
    ]

    edges = [
        dict(id=edge.id, source=edge.source, target=edge.target)
        for edge in edges
    ]

    return render(request, 'migrations_graph/index.html', {"nodes": nodes, "edges": edges})
