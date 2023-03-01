# Django Migration Dependency Graph
This is an app that helps developers understand how their migrations are interconnected across their apps, serving as a tool to identify possible circular dependencies when squashing them.

## Installation

    pip install django-migration-dependencies

## Quick start

1. Add "migrations-graph" to your INSTALLED_APPS setting like this:


    INSTALLED_APPS = [
        ...
        'migrations_graph',
    ]


2. Include the polls URLconf in your project urls.py like this::


    import migrations_graph.urls
    path('migrations-graph/', include('migrations_graph.urls')),


3. Start the development server.

4. Visit http://127.0.0.1:8000/migrations_graph/ to see the graph.
<img width="689" alt="image" src="https://user-images.githubusercontent.com/36116126/220771061-ecf9812b-afe8-459b-927b-58025225dfd8.png">

## Features
- Shows migrations that run special operations (i.e: `RunPython`s or `SeparateDatabaseAndState`) with Python's logo
- Filter by app passing the query params `include` or `exclude`.
- Change `cytoscape`s layout with query param `layout`. Takes `dagre` (default) and `breadthfirst`.

## Caveats
- Sometimes you won't get a graph for some reason and find an error in the browser's console `Cannot set property 'order' of undefined...`. Change the layout by passing the query param `?layout=breadthfirst`. For more info see https://github.com/dagrejs/dagre/issues/234
- Sometimes the graph for an app wont be complete. Select it with `include` query param to have the full graph. I don't think I'll fix this any time soon :p.

# Disclaimer
This is a real quick hack to help a one-time need (for now). You won't find tests here (...that is, for now).
