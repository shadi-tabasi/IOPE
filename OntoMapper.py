#!/usr/bin/python
# -*- coding: UTF-8 -*-


from rdflib.graph import Graph
from rdflib import URIRef
import Queries, OntoConcepts, UtilityFunctions
import unicodedata, os, time, sys
import random

def OntoMapper(AtelierURI, AtelierLabel):
    StartTime = time.time()

    # input parameters
    OntoFileName = "onto.nt"
    # QueryParameter = "samsei:PriseEnChargeUnArretCardioRespiratoire"
    QueryParameter = AtelierURI
    QueryParameterLabel = AtelierLabel
    # QueryParameterLabel = "Prise en charge d'un arret cardio respiratoire"

    print("Mapping ontlogy for "+QueryParameter+" ...")

    QueryParameterWithoutDots = QueryParameter.replace(":","")
    DirName = "static/HTMLPages/Atelier_"+QueryParameterWithoutDots
 
    try: os.mkdir(DirName)
    except: pass

    MyGraph = Graph()
    MyGraph.parse(OntoFileName, format="nt")

    Namespace = dict(owl="http://www.w3.org/2002/07/owl#",samsei="http://my.ontology.fr/sgm#")

    HasValueConstraints = OntoConcepts.OntoQuery(Queries.HasValueParamQuery, QueryParameter, MyGraph, Namespace)
    HasValueConstraintsResults = HasValueConstraints.RunQuery()

    CardinalityMaxConstraints = OntoConcepts.OntoQuery(Queries.CardinalityMaxParamQuery, QueryParameter, MyGraph, Namespace)
    CardinalityMaxResults = CardinalityMaxConstraints.RunQuery()

    CardinalityConstraints = OntoConcepts.OntoQuery(Queries.CardinalityMinParamQuery, QueryParameter, MyGraph, Namespace)
    CardinalityMinResults = CardinalityConstraints.RunQuery()

    AlternativeValueConstraints = OntoConcepts.OntoQuery(Queries.AlternativeParamQuery, QueryParameter, MyGraph, Namespace)
    AlternativeValueConstraintsResults = AlternativeValueConstraints.RunQuery()

    OntoGlobal = OntoConcepts.OntoGlobalClass()

    for ResultRow in HasValueConstraintsResults:
        HasValueConstraint = OntoConcepts.HasValueConstraintClass()
        HasValueConstraint.Fill(ResultRow)
        OntoGlobal.Update(HasValueConstraint, "HasValue")

    for ResultRow in CardinalityMaxResults:
        CardinalityMaxConstraint = OntoConcepts.CardinalityConstraintClass("Max")
        CardinalityMaxConstraint.Fill(ResultRow)
        OntoGlobal.Update(CardinalityMaxConstraint, "Max")
        OntoGlobal.UpdateMinMax(CardinalityMaxConstraint, MyGraph, Namespace)

    for ResultRow in CardinalityMinResults:
        CardinalityMinConstraint = OntoConcepts.CardinalityConstraintClass("Min")
        CardinalityMinConstraint.Fill(ResultRow)
        OntoGlobal.Update(CardinalityMinConstraint, "Min")
        OntoGlobal.UpdateMinMax(CardinalityMinConstraint, MyGraph, Namespace)

    for ResultRow in AlternativeValueConstraintsResults:
        AlternativeConstraint = OntoConcepts.AlternativeConstraintClass()
        AlternativeConstraint.Fill(ResultRow)
        OntoGlobal.Update(AlternativeConstraint, "Alter")
        OntoGlobal.UpdateAlter(AlternativeConstraint, "Alter")

    # AtelierIndexPage = open(DirName+"/AtelierIndex.html","w")
    # AtelierIndexPage.write("<html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1'><link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'><script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js'></script><style>body {padding: 20px;} a {cursor: pointer;}</style></head><body><div class='container'><div class='jumbotron'><h2>Pages du formulaire décrivant l'atelier \""+ AtelierLabel + "\":</h2></div><div class='card'><h4 class='card-header'>Accéder à chaque page pour compléter et valider les différentes sections</h4><div class='card-body'><p><b>Pages vues jusqu'à présent: </b>{{ cookie_content }}</p>")
    # AtelierIndexPage.write("{{ session_name }} <br>\n")
    # HTML generation
    count_pages = 0
    for Parent in OntoGlobal.Parents:
        count_pages += 1
        print("page",count_pages)
        SeenProperties = []
        HTMLFile = OntoConcepts.HTMLFileClass(Parent,DirName,AtelierURI)
        HTMLFile.Initialize(AtelierLabel)
        ChildrenOfParent = OntoGlobal.GetParentAssociation(Parent)
        for Child in ChildrenOfParent:
            if UtilityFunctions.Is_Child_Valid(Child, SeenProperties) == False: continue
            SeenProperties.append(Child)
            HTMLElement = OntoConcepts.HTMLElementClass(Child, Parent, MyGraph, Namespace)
            SubChildFlatRelations = HTMLElement.GetSubChildFlatRelations(Child, MyGraph, Namespace)
            HTMLTreeID = random.randint(1,1000)
            PropertyTree = UtilityFunctions.GetTreeStructure("Property",SubChildFlatRelations,Child,HTMLTreeID)
            ChildMinNumber = OntoGlobal.GetMinNumber(Child)       
            HTMLElement.Initialize(PropertyTree,SubChildFlatRelations,ChildMinNumber)
            if OntoGlobal.PropMarker[Child].find("HasValue") != -1:
                ChildValueClassLabel = OntoGlobal.GetValueClassLabel(Child)
                ChildValueLabel = OntoGlobal.GetValueLabel(Child)
                HTMLElement.AddHasValue(ChildValueClassLabel,ChildValueLabel)
            if OntoGlobal.PropMarker[Child].find("Max") != -1:
                ChildValueLabelMax = OntoGlobal.GetValueLabelMax(Child)
                ChildMaxNumber = OntoGlobal.GetMaxNumber(Child)
                HTMLElement.MaxVisited(ChildValueLabelMax)
                HTMLElement.AddMax(ChildValueLabelMax,ChildMaxNumber)
            if OntoGlobal.PropMarker[Child].find("Min") != -1: 
                ChildValueLabelMin = OntoGlobal.GetValueLabelMin(Child)
                if OntoGlobal.PropMarker[Child].find("Alter") != -1:
                    ChildValueAlterLabel = OntoGlobal.GetValueAlternative(Child)
                    if ChildValueAlterLabel != -1:
                        HTMLElement.AddAlternativeValue(ChildValueAlterLabel, Child, MyGraph, Namespace)
                # ChildMinNumber = OntoGlobal.GetMinNumber(Child)
                # HTMLElement.PropertyAsterisk(Child, ChildMinNumber)
                HTMLElement.AddMin(ChildValueLabelMin,ChildMinNumber,HTMLFile.ConstraintCount,Child,MyGraph,Namespace)
            HTMLElement.AddOrphanMax(Child,HTMLFile.ConstraintCount,MyGraph, Namespace)
            HTMLElement.OtherTextBox(Child, MyGraph, Namespace)
            HTMLFile.AddJS(HTMLElement.GetJSScript())
            HTMLFile.AddHTMLTreeJS(HTMLElement.GetHTMLTreeJS())
            HTMLFile.IncreaseConstraintCount()
            if HTMLElement.HasContent():
                HTMLFile.AddHTMLElement(HTMLElement) # attach HTMLElement to HTMLPage
        ParentFileName = Parent.replace(" ","_")
        ParentFileName = ParentFileName.decode("utf-8")
        FileName = "Page_"+ParentFileName+".php"
        # AtelierIndexPage.write("<a href=\"static/"+FileName.encode('ascii', 'xmlcharrefreplace')+"?session_name={{ session_name }}\">"+Parent+"</a><br>\n")
        # AtelierIndexPage.write("<span style='color:green'>$$</span><a href=\"/SelectPage?page="+FileName.encode('ascii', 'xmlcharrefreplace')+"&session_name={{ session_name }}&atelier_URI={{ atelier_URI }}\">"+Parent+"</a><br>\n")
        # AtelierIndexPage.write("<a href=\"/SelectPage?page="+FileName.encode('ascii', 'xmlcharrefreplace')+"&session_name={{ session_name }}&atelier_URI={{ atelier_URI }}\">"+Parent+"</a><br>\n")

        HTMLFile.Finalize()
        HTMLFile.WriteToFile()
    # AtelierIndexPage.write("</div></div>")  
    # AtelierIndexPage.close()

    EndTime = time.time()
    Duration = round(EndTime - StartTime, 2)
    print "Generated HTML pages in "+str(Duration)+" seconds."
    print(count_pages)
