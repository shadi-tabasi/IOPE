#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Queries
import unicodedata,random, json
import UtilityFunctions, HTMLGenerators, JSGenerators
import random

class OntoQuery:
	def __init__(self, QueryText, Param, MyGraph, Namespace):
		self.QueryText = QueryText 
		self.Param = Param
		self.Graph = MyGraph
		self.Namespace = Namespace
	def __repr__(self):
		return repr((self.QueryText, self.Param))
	def RunQuery(self):
		ParamQueryText = self.QueryText.replace("!p",self.Param)
		QueryResults = self.Graph.query(ParamQueryText, initNs=self.Namespace)
		print("*")
		return QueryResults

class HasValueConstraintClass:
	def __init__(self):
		self.PropertyLabel = ""
		self.ValueLabel = ""
		self.ValueURI = ""
		self.ValueClassLabel = ""
		self.ParentPropertyLabel = ""
		self.PropertyID = ""
		self.ValueLink = ""
	def Fill(self,ResultRow):
		Counter = 0
		for TextEntity in ResultRow:
			try:
				TextEntityStr = TextEntity.encode('utf-8').strip()
			except:
				TextEntityStr = ""
			TextEntityStr = str(TextEntityStr)
			if Counter == 0: self.PropertyLabel = TextEntityStr
			if Counter == 1: self.ValueURI = TextEntityStr
			if Counter == 2:
				self.ValueLabel = TextEntityStr
				if TextEntityStr == "": self.ValueLabel = self.ValueURI
			if Counter == 3: self.ValueClassLabel = TextEntityStr
			if Counter == 4:
				self.ParentPropertyLabel = TextEntityStr
				if TextEntityStr == "": self.ParentPropertyLabel = self.PropertyLabel
			if Counter == 5: self.PropertyID = TextEntityStr
			if Counter == 6: self.ValueLink = TextEntityStr
			Counter += 1

class CardinalityConstraintClass:
	def __init__(self, CardinalityType):
		self.ClassID = ""
		self.PropertyLabel = ""
		self.ClassLabel = ""
		self.CardinalityNumber = 0
		self.ParentPropertyLabel = ""
		self.PropertyID = ""
		self.CardinalityType = CardinalityType
	def Fill(self,ResultRow):
		Counter = 0
		for TextEntity in ResultRow:
			try:
				TextEntityStr = TextEntity.encode('utf-8').strip()
			except:
				TextEntityStr = ""
			TextEntityStr = str(TextEntityStr)
			if Counter == 0: self.PropertyLabel = TextEntityStr
			if Counter == 1:
				self.ClassLabel = TextEntityStr
				if self.ClassLabel == "": self.ClassLabel = "BLANK"
			if Counter == 2: self.CardinalityNumber = TextEntityStr
			if Counter == 3:
				self.ParentPropertyLabel = TextEntityStr
				if TextEntityStr == "": self.ParentPropertyLabel = self.PropertyLabel
			if Counter == 4: self.ClassID = TextEntityStr
			if Counter == 5: self.PropertyID = TextEntityStr
			Counter += 1
class AlternativeConstraintClass:
	def __init__(self):
		self.PropertyLabel = ""
		self.AlterInstanceLabel = ""
		self.AlterInstanceURI = ""
		self.PropertyID = ""
		self.ParentPropertyLabel = ""
	def Fill(self,ResultRow):
		Counter = 0
		for TextEntity in ResultRow:
			try:
				TextEntityStr = TextEntity.encode('utf-8').strip()
			except:
				TextEntityStr = ""
			TextEntityStr = str(TextEntityStr)
			if Counter == 0: self.PropertyID = TextEntityStr
			if Counter == 1: self.PropertyLabel = TextEntityStr
			if Counter == 2: self.AlterInstanceURI = TextEntityStr
			if Counter == 3: self.AlterInstanceLabel = TextEntityStr
			if Counter == 4: 
				self.ParentPropertyLabel = TextEntityStr
				if TextEntityStr == "": self.ParentPropertyLabel = self.PropertyLabel
			Counter += 1
class OntoGlobalClass:
	def __init__(self):
		self.Properties = []
		self.Parents = []
		self.PropertiesID = []
		self.ParentAssociation = {} 		# key: parent, 		value: children (properties)
		self.PropertiesType ={}
		self.HasValueValueLabels = {} 		# key: property, 	value: children (value labels)
		self.ValueLinks = {}				# key: ???
		self.HasValueValueClassLabels = {}	# key: property,	value: children (class labels)
		self.ValueLabelsMax = {}			# key: property,	value: children (value labels max)
		self.ValueLabelsMin = {}			# key: property,	value: children (value labels min)
		self.ValueLabelsAlter = {}
		self.ValueIDsAlter = {}
		self.MaxNumbers = {}				# key: property,	value: value class label max
		self.MinNumbers = {}				# key: property,	value: value class label min
		self.Instances = {}					# key: ???
		self.InstanceLinks = {}				# key: ???
		self.InstanceLabels = {}			# key: ???
		self.PropMarker = {}				# key: property 	value: type of property (hasvalue, min, max)
	def GetValueClassLabel(self, Child):
		ChildValueClassLabelStr = self.HasValueValueClassLabels[Child]
		ChildValueClassLabel = ChildValueClassLabelStr.split(",")
		return ChildValueClassLabel
	def GetValueLabel(self, Child):
		ChildValueLabelStr = self.HasValueValueLabels[Child]
		ChildValueLabel = ChildValueLabelStr.split(",")
		return ChildValueLabel
	def GetParentAssociation(self, Parent):
		ChildrenOfParentStr = self.ParentAssociation[Parent]
		ChildrenOfParent = ChildrenOfParentStr.split(",")
		return ChildrenOfParent
	def GetValueLabelMax(self,Child):
		ChildValueLabelMaxStr = self.ValueLabelsMax[Child]
		ChildValueLabelMax = ChildValueLabelMaxStr.split(",")
		return ChildValueLabelMax
	def GetMaxNumber(self,Child):
		ChildMaxNumberStr = self.MaxNumbers[Child]
		ChildMaxNumber = ChildMaxNumberStr.split(",")
		return ChildMaxNumber
	def GetValueLabelMin(self,Child):
		ChildValueLabelMinStr = self.ValueLabelsMin[Child]
		ChildValueLabelMin = ChildValueLabelMinStr.split(",")
		return ChildValueLabelMin
	def GetMinNumber(self,Child):
		ChildMinNumberStr = self.MinNumbers[Child]
		ChildMinNumber = ChildMinNumberStr.split(",")
		return ChildMinNumber
	def GetValueAlternative(self,Child):
		ChildValueLabelAlterStr = self.ValueLabelsAlter[Child]
		ChildValueLabelAlter = ChildValueLabelAlterStr.split(",")
		return ChildValueLabelAlter
	def Update(self, Constraint, ConstraintType):
		if Constraint.ParentPropertyLabel not in self.Parents:
			self.Parents.append(Constraint.ParentPropertyLabel)
			self.ParentAssociation[Constraint.ParentPropertyLabel] = "" # initialization
		if Constraint.PropertyLabel not in self.Properties:
			self.Properties.append(Constraint.PropertyLabel)
			self.PropertiesID.append(Constraint.PropertyID)
			self.MinNumbers[Constraint.PropertyLabel] = "" 
			self.ValueLabelsMin[Constraint.PropertyLabel] = ""
			self.MaxNumbers[Constraint.PropertyLabel] = "" 
			self.ValueLabelsMax[Constraint.PropertyLabel] = ""
			self.ValueLabelsAlter[Constraint.PropertyLabel] = ""
			self.ValueIDsAlter[Constraint.PropertyLabel] = ""
			if ConstraintType == "HasValue":
				self.HasValueValueLabels[Constraint.PropertyLabel] = Constraint.ValueLabel
				self.HasValueValueClassLabels[Constraint.PropertyLabel] = Constraint.ValueClassLabel
		else:
			if ConstraintType == "HasValue":
				self.HasValueValueLabels[Constraint.PropertyLabel] += "," + Constraint.ValueLabel
				self.HasValueValueClassLabels[Constraint.PropertyLabel] += "," + Constraint.ValueClassLabel
		self.ParentAssociation[Constraint.ParentPropertyLabel] += Constraint.PropertyLabel + ","
		if Constraint.PropertyLabel in self.PropMarker: self.PropMarker[Constraint.PropertyLabel] += ConstraintType
		else: self.PropMarker[Constraint.PropertyLabel] = ConstraintType
	def UpdateMinMax(self, CardinalityConstraint, MyGraph, Namespace):
		if CardinalityConstraint.CardinalityType == "Max":
			self.ValueLabelsMax[CardinalityConstraint.PropertyLabel] += CardinalityConstraint.ClassLabel + ","
			self.MaxNumbers[CardinalityConstraint.PropertyLabel] += CardinalityConstraint.CardinalityNumber + ","
		elif CardinalityConstraint.CardinalityType == "Min":
			self.ValueLabelsMin[CardinalityConstraint.PropertyLabel] += CardinalityConstraint.ClassLabel + ","
			self.MinNumbers[CardinalityConstraint.PropertyLabel] += CardinalityConstraint.CardinalityNumber + ","
	def UpdateAlter(self, Constraint, ConstraintType):
		if ConstraintType == "Alter":
			self.ValueLabelsAlter[Constraint.PropertyLabel] += "," + Constraint.AlterInstanceLabel
			self.ValueIDsAlter[Constraint.PropertyLabel] += "," + Constraint.AlterInstanceURI
class HTMLFileClass:
	def __init__(self, Parent,DirName,AtelierURI):
		self.Parent = Parent
		self.DirName = DirName
		self.Output = ""
		self.ConstraintCount = 0
		self.JSScript = ""
		self.AtelierURI = AtelierURI
	def Initialize(self,QueryParameterLabel):
		self.Output += HTMLGenerators.PHPInitializers()
		self.Output += HTMLGenerators.Header()
		self.Output += HTMLGenerators.BodyOpen()
		self.Output += "<div class='jumbotron' style= 'background-color:rgb(248, 248, 248);'><h2>L'atelier \""+QueryParameterLabel+"\"</h2></div>"
		self.Output += HTMLGenerators.RecapBox()
		self.Output += "<div class='card'><h4 class='card-header'>"+self.Parent+"</h4>"
		self.Output += "<div class='card-body'><form action='../../GetElements.php' method='post'>"

	def Finalize(self):
		self.Output += "</div></div><hr>"
		self.Output += "<p><em><b>Attention!</b> Vous devez cliquer sur \"Enregistrer\" pour mémoriser les informations saisies dans cette page.</em></p>\n"
		self.Output += "<a class='btn btn-primary float-right btn-lg' role='button' href='../../AtelierIndex.php'>Revenir à la liste des pages</a> <button type='submit' class='btn btn-success float-right btn-lg' style='margin-right: 20px;'>Enregistrer</button><br><br>\n"
		self.Output += HTMLGenerators.Footnote()
		self.Output += "</div></form>"
		self.Output += "<script src='https://code.jquery.com/jquery-1.12.4.js'></script>\n"
		self.Output += "<script src='https://code.jquery.com/ui/1.12.1/jquery-ui.js'></script>\n"
		self.Output += "<script src='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js'></script><script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js'></script>\n"
		self.Output += "<link href='https://cdnjs.cloudflare.com/ajax/libs/jquery.fancytree/2.32.0/skin-lion/ui.fancytree.min.css' rel='stylesheet'>\n"
		self.Output += "<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery.fancytree/2.32.0/jquery.fancytree.min.js'></script>\n"
		self.Output += "<script type='text/javascript'>"
		self.Output += JSGenerators.TreeAccordionConnector()
		self.Output += JSGenerators.CheckboxAccordionConnector()
		self.Output += JSGenerators.Replicator()
		self.Output += self.JSScript
		self.Output += "</script>"
		self.Output += HTMLGenerators.BodyHTMLClose()
	def AddJS(self, JSContent): self.JSScript += JSContent
	def AddHTMLTreeJS(self, HTMLTreeJS): self.JSScript += HTMLTreeJS
	def WriteToFile(self):
		ParentFileName = self.Parent.replace(" ","_")
		ParentFileName = ParentFileName.decode("utf-8")
		FileName = self.DirName+"/Page_"+ParentFileName+".php"
		File = open(FileName, "w")
		File.write(self.Output)
		File.close()
		return FileName
	def IncreaseConstraintCount(self): self.ConstraintCount += 100
	def AddHTMLElement(self,Element): self.Output += Element.Output
		
class HTMLElementClass:
	def __init__(self, Child, Parent, MyGraph, Namespace):
		self.Child = Child
		self.Parent = Parent
		self.InfoCount = 0 # counter of added information to this HTML element
		self.Output = ""
		self.SubPropertyLabels = {} # subproperty flat dictionary
		self.SubClassLabels = {} 	# subclass flat dictionary
		self.AssignedIDsForSubClassLabels = {}
		self.IDsForSubClassLabels = {}
		self.DoesSubClassHaveNoChild = {}
		self.MaxOutput = {}
		self.SeenMinMax = []
		self.SeenMax = []
		self.JSScript = ""
		self.HTMLTreeJS = ""
		self.SelectedProp = ""
		self.EntityCount = 0
		self.MyGraph = MyGraph
		self.Namespace = Namespace
		self.Tree = ""
		self.NOfTree = ""
	def Initialize(self, Tree, SubChildFlatRelations, ChildMinNumber):
		if self.Parent == self.Child: 
			self.Output += ""
			if '1' in ChildMinNumber: 
				self.Output += "(<span style='color:red'>*</span>)"
			else:
				self.Output += ""
		elif len(SubChildFlatRelations) == 0:
			self.Output += "<div class='form-group row'> <div class='card-title'>"
			self.Output += "<h5 style='margin-left: 24px;'>"+self.Child+":"+"</h5>" 
			self.Output += HTMLGenerators.CloseDiv()
			if '1' in ChildMinNumber:
				self.Output += "(<span style='color:red'>*</span>)"
			else:
				self.Output += ""
			self.Output += HTMLGenerators.CloseDiv()
		elif len(SubChildFlatRelations) != 0:
			N = random.randint(1,1000)
			self.NOfTree = N
			self.Tree = Tree
			self.Output += HTMLGenerators.OpenDiv()
			self.Output += "<div class='card-title' id='HTMLTree"+str(N)+"' onclick=\"SendToReplicate("+str(N)+",$('#HTMLTree"+str(N)+"').fancytree('getTree').getSelectedNodes())\"></div>"
			if '1' in ChildMinNumber:
				self.Output += "(<span style='color:red'>*</span>)"
			else:
				self.Output += ""
			self.Output += "</div>"
			# self.SelectedProp += "<div class='col-auto'><label><span class='font-weight-bold' id='echoSelection"+str(N)+"'></span></label></div>"
			# self.Output += "<div class='form-row card-text'><div class='col-auto'><label><span class='font-weight-bold' id='echoSelection"+str(N)+"'></span></label>"
			# self.Output += HTMLGenerators.CloseDiv()
			self.HTMLTreeJS += "$(function(){ $(\"#HTMLTree"+str(N)+"\").fancytree({ checkbox: false, selectMode: 2, icon: false, source: ["+ Tree +"], init: function(event, data) { data.tree.visit(function(n) { n.key = n.title.split(\" \")[0]; }); },select: function(event, data) { var selNodes = data.tree.getSelectedNodes(); var selKeys = $.map(selNodes, function(node){ return \"\" + node.title + \"\"; }); $(\"#echoSelection"+str(N)+"\").text(selKeys.join(\", \")); }, cookieId: \"fancytree-Cb2\", idPrefix: \"fancytree-Cb2-\" }); });"
	def GetSubChildFlatRelations(self, Child, MyGraph, Namespace):
		Stack = []
		Stack.append(Child)
		while len(Stack) != 0:
			FocusProperty = Stack.pop()
			SubPropertyQuery = OntoQuery(Queries.GetSubPropertyQuery, FocusProperty, MyGraph, Namespace)
			SubPropertyQueryResults = SubPropertyQuery.RunQuery()
			if len(SubPropertyQueryResults) == 0: pass # reaching a leaf
			for SubPropertyQueryResult in SubPropertyQueryResults:
				Stack.append(SubPropertyQueryResult[1])
				self.SubPropertyLabels[SubPropertyQueryResult[1]] = FocusProperty
		return self.SubPropertyLabels
	def GetSubClassFlatRelations(self, ClassLabel, MyGraph, Namespace):
		Stack = []
		Stack.append(ClassLabel)
		DecodedClassLabel = ClassLabel.decode("utf-8")
		self.AssignedIDsForSubClassLabels[0] = DecodedClassLabel
		self.DoesSubClassHaveNoChild[DecodedClassLabel] = True
		self.IDsForSubClassLabels[DecodedClassLabel] = -1
		CounterForSubClassLabels = 1
		while len(Stack) != 0:
			FocusClassLabel = Stack.pop()
			FocusIDQuery = OntoQuery(Queries.GetFocusIDQuery, FocusClassLabel, MyGraph, Namespace)
			FocusID = "" # will be defined in the next for loop
			FocusIDQueryResults = FocusIDQuery.RunQuery()
			for FocusIDQueryResult in FocusIDQueryResults: FocusID = FocusIDQueryResult[0]
			SubClassQuery = OntoQuery(Queries.GetSubClassQuery, FocusID, MyGraph, Namespace)
			SubClassQueryResults = SubClassQuery.RunQuery()
			if len(SubClassQueryResults) == 0: 
				self.DoesSubClassHaveNoChild[FocusClassLabel] = False
				pass # reaching a leaf
			for SubClassQueryResult in SubClassQueryResults:
				Stack.append(SubClassQueryResult[1])
				self.SubClassLabels[SubClassQueryResult[1]] = FocusClassLabel
				# print "**", SubClassQueryResult[1], "->", FocusClassLabel
				self.AssignedIDsForSubClassLabels[CounterForSubClassLabels] = SubClassQueryResult[1]
				self.IDsForSubClassLabels[SubClassQueryResult[1]] = SubClassQueryResult[0]
				self.DoesSubClassHaveNoChild[SubClassQueryResult[1]] = True
				CounterForSubClassLabels += 1
		return self.SubClassLabels
	def MaxVisited(self,ChildValueLabelMax):
		for Label in ChildValueLabelMax: self.SeenMax.append(Label)
	def GetMaxOutput(self): return self.MaxOutput
	def HasContent(self): 
		if self.InfoCount > 0: return True
	def AddHasValue(self, ChildValueClassLabel, ChildValueLabel):
		for Counter in range(0,len(ChildValueClassLabel)):
			if ChildValueClassLabel[Counter] == "": 
				self.Output += "<p style='margin-left: 30px;'><b>"+ChildValueLabel[Counter]+ "</b> " + "(<span style='color:red'>*</span>)"+"</p>\n"
				self.InfoCount += 1
			else:
				self.Output += "<p style='margin-left: 30px;'><b>"+ChildValueLabel[Counter]+ "</b> " + "(" +ChildValueClassLabel[Counter]+ ") " + "<b><span style='color:red'>*</span></b> "+"</p>\n"
				self.InfoCount += 1
	def AddAlternativeValue(self, ChildValueAlterLabel, Child, MyGraph, Namespace):
		ChildIDQuery = OntoQuery(Queries.GetFocusIDQuery, Child, MyGraph, Namespace)
		ChildIDQueryResults = ChildIDQuery.RunQuery()
		for Element in ChildIDQueryResults: ChildID = Element[0]
		self.Output += "<fieldset style='border:1px solid rgba(0, 0, 0, 0.24); margin-bottom:25px;'>"
		for Counter in range(0,len(ChildValueAlterLabel)): 
			ValueNameID = ""
			CheckBoxID = random.randint(1,1000)
			self.Output += "<div class='col-auto mr-auto'><div class='form-check'>"
			ChildValueAlterIDQuery = OntoQuery(Queries.GetFocusIDQuery, ChildValueAlterLabel[Counter], MyGraph, Namespace)
			ChildValueAlterIDQueryResults = ChildValueAlterIDQuery.RunQuery()
			for Element in ChildValueAlterIDQueryResults: 
				ValueNameID = Element[0]
			self.Output += "<input class='form-check-input' name='R6$" + ChildID.encode("utf-8") + '$' + ValueNameID.encode('ascii', 'xmlcharrefreplace') + "' type='checkbox' >"
			# self.Output += "<p style='margin-left: 30px;'><b>"+ChildValueAlterLabel[Counter]+ "</b></p>\n"
			self.Output += HTMLGenerators.InBold(ChildValueAlterLabel[Counter],CheckBoxID)
			self.Output += "</div></div>"
			self.InfoCount += 1
		self.Output += "</fieldset>"

	def AddMax(self,ChildValueLabelMax,ChildMaxNumber):
		for Counter in range(0,len(ChildValueLabelMax)):
			if ChildValueLabelMax[Counter] != "":
				self.MaxOutput[ChildValueLabelMax[Counter]] = ChildMaxNumber[Counter]
	def AddOrphanMax(self,Child,ConstraintCount, MyGraph, Namespace):
		# !!! need to add class tree
		for Label in self.SeenMax: # Children with Max but not Min
			if Label == "": continue
			TreeStructure = TreeStructureClass(Label, ConstraintCount+self.EntityCount, ValueLabels, MyGraph, Namespace)
			TreeStructureOutput = TreeStructure.GetSelectStructure()
			self.Output += "<div class='form-group row'><label for='Entrez votre chiffre' class='col-sm-8 col-form-label'>"
			if TreeStructureOutput != "": self.Output += "<a id='ShowDiv"+str(ConstraintCount+self.EntityCount)+"'>&#x25BA</a> "
			if Label != "BLANK": self.Output += "<b>"+Label+"</b>: "
			self.Output += "(maximum: "+self.MaxOutput[Label]+")</label>"
			self.Output += "<div class='col-sm-4'><input type='text' placeholder='Entrez votre chiffre' class='form-control'></div></div>\n"
			self.InfoCount += 1
	def GetJSScript(self): return self.JSScript
	def GetHTMLTreeJS(self): return self.HTMLTreeJS
	def GenerateClassTree(self,ClassTreeID,AsteriskShower,AccordionContent):
		TreeOutput = ""
		TreeOutput += HTMLGenerators.OpenDiv("ClassTree")
		TreeOutput += HTMLGenerators.HTMLTree(ClassTreeID)
		TreeOutput += HTMLGenerators.ShowAsterisk(AsteriskShower)
		TreeOutput += HTMLGenerators.HTMLAccordion(ClassTreeID,AccordionContent)
		TreeOutput += HTMLGenerators.CloseDiv()
		return TreeOutput
	def AddMin(self,ChildValueLabelMin,ChildMinNumber,ConstraintCount, Child, MyGraph,Namespace):
		CheckBoxLabels = {}
		for Counter in range(0,len(ChildValueLabelMin)):
			CurrentClassLabel = ChildValueLabelMin[Counter]
			if CurrentClassLabel == "": continue
			SubClassFlatRelations = self.GetSubClassFlatRelations(CurrentClassLabel, self.MyGraph, self.Namespace)
			if self.Tree != "":
				TreeLoaded = json.loads(str(self.Tree))
				Properties = TreeLoaded["children"]
				for Property in Properties: 
					PropertyLabel = Property["title"]
					RefKey = Property["refKey"]
					self.Output += "<div id='DivForHTMLTree"+str(self.NOfTree)+"' class=''>"
					self.Output += "<div class='card-text SpecialPropertyClassToHide"+str(self.NOfTree)+"' id='PropertyDiv"+RefKey.encode("utf-8")+"' style='display:none'><h6 style='margin-bottom: 25px; margin-top: 25px;'>"+PropertyLabel.encode("utf-8")+"</h6>"
					HTMLTreeID = random.randint(1,1000)
					ClassTree = UtilityFunctions.GetTreeStructure("Class",SubClassFlatRelations,CurrentClassLabel,HTMLTreeID)
					TreeOutput = ""
					TreeOutputJS = ""
					if len(SubClassFlatRelations) and ClassTree:
						AccordionContent = UtilityFunctions.GetAccordionContent(self.AssignedIDsForSubClassLabels,self.IDsForSubClassLabels,self.DoesSubClassHaveNoChild,HTMLTreeID,self.MyGraph,self.Namespace, PropertyLabel)
						self.Output += self.GenerateClassTree(HTMLTreeID,ChildMinNumber[Counter],AccordionContent)
						TreeOutputJS += JSGenerators.HTMLTree(HTMLTreeID,ClassTree)
						self.Output += "</div></div>"
						self.HTMLTreeJS += TreeOutputJS
					else:
						self.Output += "<div id='DivForHTMLTree"+str(self.NOfTree)+"' class=''>"
						self.Output += "<div class='card-text SpecialPropertyClassToHide"+str(self.NOfTree)+"' id='PropertyDiv"+RefKey.encode("utf-8")+"' style='display:none'><h6 style='margin-bottom: 25px; margin-top: 25px;'>"+PropertyLabel.encode("utf-8")+"</h6>"
						self.Output += "<div class='form-group row'>"
						CheckBoxID = random.randint(1,1000)
						if CurrentClassLabel == "BLANK":
							ChildIDQuery = OntoQuery(Queries.GetFocusIDQuery, Child, MyGraph, Namespace)
							ChildIDQueryResults = ChildIDQuery.RunQuery()
							for Element in ChildIDQueryResults: ChildID = Element[0]
							self.Output += HTMLGenerators.TextBox(ChildID)
							self.Output += HTMLGenerators.ShowAsterisk(ChildMinNumber[Counter])
						if CurrentClassLabel != "BLANK": 
							self.Output += "<div class='col-auto mr-auto'>"
							self.Output += "<div class='form-check'>"
							self.Output += HTMLGenerators.CheckBox(CheckBoxID)
							self.Output += HTMLGenerators.InBold(CurrentClassLabel,CheckBoxID) # print label of the class
							CheckBoxLabels[CheckBoxID] = CurrentClassLabel
							self.Output += "</div></div>"
							self.Output += HTMLGenerators.ShowAsterisk(ChildMinNumber[Counter])
							AccordionContent = UtilityFunctions.GetCheckBoxAccordionContent(CheckBoxLabels,self.MyGraph, self.Namespace, Child)
							self.Output += "<div class='accordion col-sm-4 ml-auto' id='Accordion12345'>"+AccordionContent+"</div>"
						self.Output += "</div>"
					self.InfoCount += 1
			if self.Tree == "":
				HTMLTreeID = random.randint(1,1000)
				ClassTree = UtilityFunctions.GetTreeStructure("Class",SubClassFlatRelations,CurrentClassLabel,HTMLTreeID)
				TreeOutput = ""
				TreeOutputJS = ""
				if len(SubClassFlatRelations) != 0 and ClassTree != False:
					AccordionContent = UtilityFunctions.GetAccordionContent(self.AssignedIDsForSubClassLabels,self.IDsForSubClassLabels,self.DoesSubClassHaveNoChild,HTMLTreeID,self.MyGraph,self.Namespace, Child)
					TreeOutput += self.GenerateClassTree(HTMLTreeID,ChildMinNumber[Counter],AccordionContent)
					TreeOutputJS += JSGenerators.HTMLTree(HTMLTreeID,ClassTree)
					PropertyDivs = UtilityFunctions.MakePropertyDivs(self.Tree,self.NOfTree,TreeOutput)
					if PropertyDivs != -1: self.Output += "<div id='DivForHTMLTree"+str(self.NOfTree)+"' class=''>"+PropertyDivs+"</div>"
					else: self.Output += TreeOutput
					self.HTMLTreeJS += TreeOutputJS
				else:
					self.Output += "<br><div class='form-group row'>"
					CheckBoxID = random.randint(1,1000)
					if CurrentClassLabel == "BLANK": 
						ChildIDQuery = OntoQuery(Queries.GetFocusIDQuery, Child, MyGraph, Namespace)
						ChildIDQueryResults = ChildIDQuery.RunQuery()
						for Element in ChildIDQueryResults: ChildID = Element[0]
						self.Output += HTMLGenerators.TextBox(ChildID)
						self.Output += HTMLGenerators.ShowAsterisk(ChildMinNumber[Counter])
					if CurrentClassLabel != "BLANK": 
						self.Output += "<div class='col-auto mr-auto'>"
						self.Output += "<div class='form-check'>"
						self.Output += HTMLGenerators.CheckBox(CheckBoxID)
						self.Output += HTMLGenerators.InBold(CurrentClassLabel,CheckBoxID) # print label of the class
						CheckBoxLabels[CheckBoxID] = CurrentClassLabel
						self.Output += "</div></div>"
						self.Output += HTMLGenerators.ShowAsterisk(ChildMinNumber[Counter])
						AccordionContent = UtilityFunctions.GetCheckBoxAccordionContent(CheckBoxLabels,self.MyGraph, self.Namespace, Child)
						self.Output += "<div class='accordion col-sm-4 ml-auto' id='Accordion12345'>"+AccordionContent+"</div>"
					self.Output += "</div>"
				self.InfoCount += 1
	def OtherTextBox(self, Child, MyGraph,Namespace):
		ChildIDQuery = OntoQuery(Queries.GetFocusIDQuery, Child, MyGraph, Namespace)
		ChildIDQueryResults = ChildIDQuery.RunQuery()
		for Element in ChildIDQueryResults: ChildID = Element[0]
		DataPropertyTypeQuery = OntoQuery(Queries.GetDataPropertyType, Child, MyGraph, Namespace)
		DataPropertyTypeQueryResults = DataPropertyTypeQuery.RunQuery()
		if len(DataPropertyTypeQueryResults) == 0: self.Output += "<br><div class='form-group row' style='margin-left:20px;'><label for='' class='col-sm-1 col-form-label'>Autre : </label><div class='col-sm-7'><input class='form-control' name='R5$" + ChildID.encode('utf-8') + "' type='text' id='' placeholder='Donner le(s) libellé(s) (séparer les libellés avec une virgule).'></div></div>"
		else: return 

		
class InstancesOfSubClassClass:
	def __init__(self, FocusNode, FocusNodeLabel, ValueLabels, myGraph, namespace):
		self.FocusNode = FocusNode
		self.FocusNodeLabel = FocusNodeLabel.encode('utf-8').strip()
		self.myGraph = myGraph
		self.namespace = namespace
		self.HasValueValueLabels = ValueLabels
	def GetInstances(self):
		Output = "<div id='"+str(self.FocusNode)+"' class='form-group row' style='display:None'>\n"
		Output += "<p><b>Instances of \""+str(self.FocusNodeLabel)+"\":</b></p>"
		Output += "<ul>\n"
		InstancesQuery = OntoQuery(Queries.GetInstanceQuery, str(self.FocusNode), self.myGraph, self.namespace)
		InstancesQueryResults = InstancesQuery.RunQuery()
		for Element in InstancesQueryResults:
			InstanceLabel = Element[0].encode('utf-8').strip()
			InstanceName = Element[1].encode('utf-8').strip()
			InstanceLink = Element[2]
			AlreadyChosen = ""
			for n in self.HasValueValueLabels:
				if self.HasValueValueLabels[n] == InstanceLabel:
					AlreadyChosen = " <span style='color:green'><b><em>(deja imposee)</em></b></span>"
			if InstanceLink == None:
				Output += "<li>&#x25A0 <em>"+str(InstanceLabel)+"</em>"+AlreadyChosen+"</li>\n"
			else:
				Output += "<li>&#x25A0 <a href='"+str(InstanceLink)+"'><em>"+str(InstanceLabel)+"</em>"+AlreadyChosen+"</a></li>\n"
		Output += "</ul>"
		Output += "<div class='input-group mb-3'><input type='text' class='form-control' placeholder='Precisez la ressource (peut etre un nom, un titre, une URL, ou autre)' aria-label='' aria-describedby='basic-addon2'><div class='input-group-append'><button class='btn btn-outline-secondary' type='button'>Ajouter</button></div></div>"
		Output += "</div>\n"
		return Output


# class TreeStructureClass:
# 	def __init__(self, Focus, ConstraintCount, myGraph, namespace):
# 		self.SubClassLabels = {}
# 		self.Focus = Focus
# 		self.FocusID = ""
# 		self.myGraph = myGraph
# 		self.namespace = namespace
# 		self.DIVs = ""
# 		FocusIDQ = OntoQuery(Queries.GetFocusIDQuery, self.Focus, myGraph, namespace)
# 		FocusIDResults = FocusIDQ.RunQuery()
# 		for Element in FocusIDResults:
# 			self.FocusID = Element[0]
# 	def GetSelectStructure(self):
# 		TempStack = []
# 		TempStack.append(self.FocusID)
# 		ShowTreeStructure = True
# 		while len(TempStack) != 0:
# 			FocusClass = TempStack.pop()
# 			SubClassQuery = OntoQuery(Queries.GetSubClassQuery, FocusClass, self.myGraph, self.namespace)
# 			SubClassQueryResults = SubClassQuery.RunQuery()
# 			if len(SubClassQueryResults) == 0: pass # reaching a leaf
# 			for SubClassQueryResult in SubClassQueryResults:
# 				TempStack.append(SubClassQueryResult[0])
# 				self.SubClassLabels[SubClassQueryResult[1]] = SubClassQueryResult[2]
# 				# self.SubClassLabels[SubClassQueryResult[1]] = FocusClass
# 		return self.SubClassLabels



               		
		





