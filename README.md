# Django Migration Dependency Graph
This is an app that helps developers understand how their migrations are interconnected across their apps, serving as a tool to identify possible circular dependencies when squashing them.

## Quick start

1. Add "migrations-graph" to your INSTALLED_APPS setting like this:


    INSTALLED_APPS = [
        ...
        'migrations-graph',
    ]


2. Include the polls URLconf in your project urls.py like this::


    path('migrations-graph/', include('migrations_graph.urls')),


3. Start the development server.

4. Visit http://127.0.0.1:8000/migrations_graph/ to see the graph.
