"""
Script to convert from InPhO data model to RDF triple store.
"""
import rdflib
from rdflib import Literal, Namespace
from rdflib.graph import ConjunctiveGraph as Graph

from inpho.model import *

g = Graph()

# add namespaces
inpho = Namespace("http://inpho.cogs.indiana.edu/")
g.bind("inpho", "http://inpho.cogs.indiana.edu/")

t = Namespace("http://inpho.cogs.indiana.edu/thinker/")
g.bind("thinker", "http://inpho.cogs.indiana.edu/thinker/")

foaf = Namespace("http://xmlns.com/foaf/0.1/")
g.bind("foaf", "http://xmlns.com/foaf/0.1/")

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
g.bind("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")

rdfs = Namespace("http://www.w3.org/TR/rdf-schema/#")
g.bind("rdfs", "http://www.w3.org/TR/rdf-schema/#")

owl = Namespace("http://www.w3.org/2002/07/owl#")
g.bind("owl", "http://www.w3.org/2002/07/owl#")

skos = Namespace("http://www.w3.org/2004/02/skos/core#")
g.bind("skos", "http://www.w3.org/2004/02/skos/core#")

dc = Namespace("http://purl.org/dc/elements/1.1/")
g.bind ("dc", "http://purl.org/dc/elements/1.1/")

# Select all Thinkers
thinkers = Session.query(Thinker).all()
g.add((inpho['thinker'], rdf['type'], foaf['person']))
g.add((inpho['thinker'], rdfs['subClassOf'], inpho['entity']))
for thinker in thinkers:
    g.add((t['t' + str(thinker.ID)], rdf['type'], inpho['thinker']))
    g.add((t['t' + str(thinker.ID)], foaf['name'], Literal(thinker.label)))

with open("out.rdf", "w") as f:
    f.write(g.serialize(format="n3"))