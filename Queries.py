HasValueParamQuery = """
SELECT  ?prop_name_label ?value ?value_label ?value_type_label ?parent_name_label ?prop_id ?link
WHERE {  !p  rdfs:subClassOf _:R .
_:R rdf:type  owl:Restriction .
_:R owl:onProperty ?prop_id .
_:R owl:hasValue ?value . 
?prop_id rdfs:label ?prop_name_label .
OPTIONAL{?value rdfs:label ?value_label. FILTER langMatches( lang(?value_label ), "FR"  )}
OPTIONAL{ ?prop_id rdfs:subPropertyOf ?parent. ?parent rdfs:label ?parent_name_label .  FILTER langMatches( lang(?parent_name_label ), "FR"  )}
OPTIONAL{ ?value rdf:type ?value_type. ?value_type rdfs:label ?value_type_label. FILTER langMatches( lang(?value_type_label), "FR"  ) }
OPTIONAL{ ?value rdfs:seeAlso ?link}
FILTER langMatches( lang(?prop_name_label ), "FR"  )
}
"""


CardinalityMaxParamQuery = """
SELECT  ?prop_name_label ?value_label_max ?maxnumber ?parent_name_label ?class_name ?prop_id
WHERE {
VALUES ?quantifierType { owl:maxQualifiedCardinality  owl:maxCardinality}
!p rdfs:subClassOf ?B .
?B rdf:type  owl:Restriction .
?B owl:onProperty ?prop_id .
?prop_id rdfs:label ?prop_name_label .
?B ?quantifierType ?maxnumber 
OPTIONAL{?B owl:onClass ?class_name .
?class_name rdfs:label ?value_label_max. FILTER langMatches( lang(?value_label_max ), "FR"  )}
OPTIONAL{?prop_id rdfs:subPropertyOf ?parent .
?parent rdfs:label ?parent_name_label . FILTER langMatches( lang(?parent_name_label ), "FR"  )}
FILTER langMatches( lang(?prop_name_label ), "FR"  )
}
 """

CardinalityMinParamQuery = """
SELECT  ?prop_name_label ?value_label_min ?minnumber ?parent_name_label ?class_name ?prop_id
WHERE {
VALUES ?quantifierType { owl:minQualifiedCardinality  owl:minCardinality}
!p rdfs:subClassOf ?B .
?B rdf:type  owl:Restriction .
?B owl:onProperty ?prop_id .
?prop_id rdfs:label ?prop_name_label .
?B ?quantifierType ?minnumber 
OPTIONAL{?B owl:onClass ?class_name .
?class_name rdfs:label ?value_label_min. filter langMatches( lang(?value_label_min ), "FR"  )}
OPTIONAL{?prop_id rdfs:subPropertyOf ?parent .
?parent rdfs:label ?parent_name_label . filter langMatches( lang(?parent_name_label ), "FR"  )}
FILTER langMatches( lang(?prop_name_label ), "FR"  )
FILTER isBlank(?B)
} 
 """

AlternativeParamQuery = """
SELECT ?prop_id  ?prop_label ?instance ?instance_label  ?parent_name_label
WHERE {!p ?prop_id ?B.
?B rdf:type rdf:Alt .
?B ?num ?instance .
?instance rdfs:label ?instance_label .
?prop_id rdfs:label ?prop_label
OPTIONAL{?prop_id rdfs:subPropertyOf ?parent .
?parent rdfs:label ?parent_name_label . 
FILTER langMatches( lang(?parent_name_label ), "FR"  )}
FILTER langMatches( lang(?prop_label ), "FR"  )
FILTER (?num != rdf:type)
FILTER langMatches( lang(?instance_label), "FR"  )
}ORDER BY ASC(?instance_label)
"""


GetSubPropertyQuery = """
SELECT  ?sub_property ?sub_property_label ?property
WHERE { ?sub_property rdfs:subPropertyOf ?property.
?property rdfs:label \"!p\"@fr .
?sub_property rdfs:label ?sub_property_label 
FILTER langMatches( lang(?sub_property_label ), "FR"  )
}
"""
# SELECT  ?sub_class ?subclass_label
# WHERE { ?sub_class rdfs:subClassOf <!p>  .
# ?sub_class rdfs:label ?subclass_label
# FILTER langMatches( lang(?subclass_label ), "FR"  )
# }

GetSubClassQuery = """ 
SELECT  ?sub_class ?subclass_label ?class_label
WHERE { ?sub_class rdfs:subClassOf <!p> .
<!p> rdfs:label ?class_label .
?sub_class rdfs:label ?subclass_label
FILTER langMatches( lang(?subclass_label ), "FR"  )
FILTER langMatches( lang(?class_label ), "FR"  )
} 
 """



GetInstanceQuery = """
SELECT  ?instance_label ?instance ?link 
WHERE { ?instance rdf:type <!p>  .
?instance samsei:affichable true .
?instance rdfs:label ?instance_label .
OPTIONAL{ ?instance rdfs:seeAlso ?link}
FILTER langMatches( lang(?instance_label ), "FR"  )
}
"""
GetFocusLabelQuery = """
SELECT ?label
WHERE {
<!p> rdfs:label ?label
FILTER langMatches( lang(?label ), "FR"  )
} """

GetFocusIDQuery = """
SELECT ?url
WHERE {
?url rdfs:label "!p"@fr
}
"""

GetFunctionalProperty = """
SELECT   ?property
WHERE {  
?property rdf:type  owl:FunctionalProperty .
}
"""

GetQuantifiableClass = """
SELECT  ?class 
WHERE { ?class samsei:quantifiable true .
?class rdfs:label "!p"@fr
}
"""
GetDataPropertyType = """
SELECT  ?P 
WHERE { ?P rdfs:label "!p"@fr .
  ?P rdf:type owl:DatatypeProperty .
}
"""

GetAtelierListQuery = """
SELECT  distinct ?Atelier  ?AtelierLabel  
WHERE { ?Atelier rdfs:subClassOf* samsei:UAPS .
?Atelier  rdfs:subClassOf ?B .
?B rdf:type  owl:Restriction .
?Atelier rdfs:label ?AtelierLabel.
FILTER langMatches( lang(?AtelierLabel ), "FR"  )
FILTER(?Atelier != samsei:UAPS)
}ORDER BY ASC(?Atelier)
"""

GetLabelOfID = """
SELECT ?uri  ?label 
WHERE {?uri rdfs:label ?label .
FILTER langMatches( lang(?label ), "FR"  )
}"""

# GetFocusIDQuery = """
# SELECT ?url
# WHERE {
# ?url rdfs:label "!p"@fr
# }
# """