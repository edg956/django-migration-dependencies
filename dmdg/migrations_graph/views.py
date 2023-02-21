from django.apps import apps
from django.db.migrations.loader import MigrationLoader
from django.shortcuts import render


def index(request):
    include = request.GET.get('include', None)
    exclude = request.GET.get('exclude', "")

    loader = MigrationLoader(None)

    if include:
        include = include.split(',')
    else:
        include = [app.label for app in apps.get_app_configs()]

    nodes = [
        loader.graph.node_map[(app_label, migration)]
        for app in include
        for app_label, migration in loader.graph.root_nodes(app)
        if app not in exclude
    ]

    node_and_child = []
    final_nodes = set()
    for node in nodes:
        for parent in node.parents:
            node_tuple = parent, node
            if node_tuple not in node_and_child:
                node_and_child.append(node_tuple)

        for child in node.children:
            node_tuple = node, child
            if node_tuple not in node_and_child:
                node_and_child.append(node_tuple)

            nodes.append(child)
        final_nodes.add(node)

    nodes = [
        dict(id=str(node.key[0]), name=str(node.key[0]), type="app")
        for node in nodes
    ] + [ # noqa
        dict(id=f"{node.key[0]}-{node.key[1]}", name=str(node.key[1]), parent=str(node.key[0]), type="migration")
        for node in final_nodes
    ]

    edges = [
        dict(id=f"{n1.key[0]}-{n1.key[1]}__{n2.key[0]}-{n2.key[1]}", source=f"{n1.key[0]}-{n1.key[1]}", target=f"{n2.key[0]}-{n2.key[1]}")
        for n1, n2 in node_and_child
    ]

    return render(request, 'migrations_graph/index.html', {"nodes": nodes, "edges": edges})
