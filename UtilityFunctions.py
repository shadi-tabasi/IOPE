#!/usr/bin/python
# -*- coding: UTF-8 -*-
from hashlib import md5 
import time
import json 

def Is_Child_Valid(Child, SeenProperties):
	if Child in SeenProperties or Child == "": return False
	return True

def TreeAccordionKeyGenerator(Element1, Element2, Type="NonAutre"):


	Element1 = Element1.strip()
	Key = ""
	Count = 0
	Half = ord(Element1[len(Element1)/2])
	if Type == "Autre": Key = str(ord(Element1[0])) + str(ord(Element1[1])) + str(ord(Element1[2])) + str(ord(Element1[-1])) + str(ord(Element1[-2])) + str(Element2)
	else: 
		A = Element1[ : :1]
		for i in A:
			Count+=ord(i)
		Key = str(Count) + str(Element2)
		# Key = str(ord(Element1[0])) + str(ord(Element1[1])) + str(ord(Element1[2])) + str(Half) + str(ord(Element1[-1])) + str(ord(Element1[-2])) + str(Element2)
	return Key


def MakeTreeRecursively(TreeType,Node,Dictionary,Mapping,HTMLTreeID):
	try: Children = Mapping[Node]
	except: return False
	if len(Children) == 0: 
		Key = TreeAccordionKeyGenerator(Node,HTMLTreeID)
		return {"title": Node, "refKey": str(Key), "checkbox":True}
	for Child in Children:
	    NewDic = {"title": Child, "children": []}
	    Dictionary["children"].append(MakeTreeRecursively(TreeType,Child,NewDic,Mapping,HTMLTreeID))
	AutreKey = TreeAccordionKeyGenerator(Node,HTMLTreeID,"Autre")
	if TreeType == "Class":
		Dictionary["children"].append({"title": "Autre "+Node.lower(), "refKey": str(AutreKey), "checkbox":True})
	return Dictionary

import json
def GetTreeStructure(TreeType,SubChildFlatRelations,Child,HTMLTreeID):
	if len(SubChildFlatRelations) == 0: return False
	TreeRoots = set()
	TreeMapping = {}
	for SubProperty, Property in SubChildFlatRelations.iteritems():
		TreeSubPropertyItem = TreeMapping.get(SubProperty,None)
		if TreeSubPropertyItem is None:
			TreeSubPropertyItem =  {}
			TreeMapping[SubProperty] = TreeSubPropertyItem
		else:
			TreeRoots.discard(SubProperty)
		TreeParentItem = TreeMapping.get(Property,None)
		if TreeParentItem is None:
			TreeMapping[Property] = {SubProperty:TreeSubPropertyItem}
			TreeRoots.add(Property)
		else: TreeParentItem[SubProperty] = TreeSubPropertyItem
	Key = TreeAccordionKeyGenerator(Child,HTMLTreeID)
	InitialDic = {"title": Child, "children": []} if TreeType == "Class" else {"title": Child,  "children": []}
	Tree = MakeTreeRecursively(TreeType,Child,InitialDic,TreeMapping,HTMLTreeID)
	TreeDumps = json.dumps(Tree)
	if TreeDumps == "false":
		return False
	return TreeDumps

import Queries, OntoConcepts
def GetCollapseInstances(ID,myGraph,Namespace):
	Output = []
	InstancesQuery = OntoConcepts.OntoQuery(Queries.GetInstanceQuery, str(ID), myGraph, Namespace)
	InstancesQueryResults = InstancesQuery.RunQuery()
	for Element in InstancesQueryResults:
		InstanceLabel = Element[0].encode('utf-8').strip()
		InstanceName = Element[1].encode('utf-8').strip()
		InstanceLink = Element[2]
		Output.append(InstanceLabel)
	return Output

import Queries, OntoConcepts
def GetQuantifiableValue(Label,MyGraph,Namespace):
	QuantifiableValueQuery = OntoConcepts.OntoQuery(Queries.GetQuantifiableClass, Label, MyGraph, Namespace)
	QuantifiableValueQueryResults = QuantifiableValueQuery.RunQuery()
	if len(QuantifiableValueQueryResults) == 0: return False
	else: return True

def GetDataPropertyType(Child,MyGraph,Namespace):
	DataPropertyTypeQuery = OntoConcepts.OntoQuery(Queries.GetDataPropertyType, Child, MyGraph, Namespace)
	DataPropertyTypeQueryResults = DataPropertyTypeQuery.RunQuery()
	if len(DataPropertyTypeQueryResults) == 0: return False
	else: return True

import HTMLGenerators
def GetAccordionContent(AssignedIDsForSubClassLabels,IDsForSubClassLabels,DoesSubClassHaveNoChild,HTMLTreeID,MyGraph,Namespace,Child):
	AccordionContent = ""
	for Key in AssignedIDsForSubClassLabels:
		ChildName = AssignedIDsForSubClassLabels[Key]
		ChildIDQuery = OntoConcepts.OntoQuery(Queries.GetFocusIDQuery, Child, MyGraph, Namespace)
		ChildIDQueryResults = ChildIDQuery.RunQuery()
		for Element in ChildIDQueryResults: ChildID = Element[0]
		ChildNameQuery = OntoConcepts.OntoQuery(Queries.GetFocusIDQuery, ChildName, MyGraph, Namespace)
		ChildNameQueryResults = ChildNameQuery.RunQuery()
		for Element in ChildNameQueryResults: ChildNameID = Element[0]
		if DoesSubClassHaveNoChild[ChildName] == False : 
			AssignedID = TreeAccordionKeyGenerator(ChildName,HTMLTreeID)
			CollapseHeader = HTMLGenerators.CollapseHeader(AssignedID,ChildName,HTMLTreeID)
			CollapseInstances = GetCollapseInstances(IDsForSubClassLabels[ChildName],MyGraph,Namespace)
			Quantifiable = GetQuantifiableValue(ChildName,MyGraph,Namespace)
			CollapseContent = HTMLGenerators.CollapseContent(CollapseInstances,Quantifiable, ChildID, ChildNameID, AssignedID)
			CollapseBody = HTMLGenerators.CollapseBody(AssignedID,HTMLTreeID,CollapseContent)
			AccordionContent += CollapseHeader + "\n" + CollapseBody
		elif DoesSubClassHaveNoChild[ChildName] == True: 
			AssignedID = TreeAccordionKeyGenerator(ChildName,HTMLTreeID,"Autre")
			AutreChildName = "Autre "+ChildName 
			CollapseHeader = HTMLGenerators.CollapseHeader(AssignedID,AutreChildName,HTMLTreeID)
			Quantifiable = GetQuantifiableValue(AutreChildName,MyGraph,Namespace)
			CollapseInstances = ""
			# if AutreChildName in locals():
			# 	print "****"+IDsForSubClassLabels[AutreChildName]
			CollapseContent = "<br><input class='form-control' data-role='tagsinput' type='text' name='R4$" + ChildID.encode('utf-8') + "$" + ChildNameID.encode('utf-8') + "$" + AssignedID + "' placeholder='Donner le(s) libellé(s).'>"
			# print CollapseContent
			CollapseBody = HTMLGenerators.CollapseBody(AssignedID,HTMLTreeID,CollapseContent)
			AccordionContent += CollapseHeader + "\n" + CollapseBody
	return AccordionContent

import random, Queries
def GetCheckBoxAccordionContent(CheckBoxLabels, MyGraph, Namespace, Child):
	AccordionContent = ""
	for CheckBoxLabel in CheckBoxLabels:
		ChildIDQuery = OntoConcepts.OntoQuery(Queries.GetFocusIDQuery, Child, MyGraph, Namespace)
		ChildIDQueryResults = ChildIDQuery.RunQuery()
		for Element in ChildIDQueryResults: ChildID = Element[0]
		CheckBoxID = CheckBoxLabel
		Label = CheckBoxLabels[CheckBoxLabel]
		CollapseHeader = HTMLGenerators.CollapseHeader(CheckBoxID,Label,"12345")
		LabelIDQuery = OntoConcepts.OntoQuery(Queries.GetFocusIDQuery, Label, MyGraph, Namespace)
		LabelIDQueryResults = LabelIDQuery.RunQuery()
		LabelID = ""
		for Element in LabelIDQueryResults: LabelID = Element[0]
		CollapseInstances = GetCollapseInstances(LabelID,MyGraph,Namespace)
		Quantifiable = GetQuantifiableValue(Label,MyGraph,Namespace)
		CollapseContent = HTMLGenerators.CollapseContent(CollapseInstances,Quantifiable, ChildID, LabelID, CheckBoxID)
		CollapseBody =  "<div id='collapse"+str(CheckBoxID)+"' class='collapse' aria-labelledby='heading"+str(CheckBoxID)+"' data-parent='#Accordion12345'><div class='card-body'>"+CollapseContent+"</div></div></div>"
		AccordionContent += CollapseHeader + "\n" + CollapseBody
	return AccordionContent
import sys
def MakePropertyDivs(Tree,TreeID,Content):
	Output = ""
	if Tree == "": return -1
	TreeLoaded = json.loads(str(Tree))
	Properties = TreeLoaded["children"]
	for Property in Properties: 
		PropertyLabel = Property["title"]
		RefKey = Property["refKey"]
		Output += "<div class='card-text SpecialPropertyClassToHide"+str(TreeID)+"' id='PropertyDiv"+RefKey.encode("utf-8")+"' style='display:none'><h6 style='margin-bottom: 25px; margin-top: 25px;'>"+PropertyLabel.encode("utf-8")+"</h6>"+Content+"</div>"
	return Output
			