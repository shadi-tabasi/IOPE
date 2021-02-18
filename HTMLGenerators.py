#!/usr/bin/python
# -*- coding: UTF-8 -*-
def OpenDiv(Type=""):
	if Type == "ClassTree": return "<br><div class='form-row card-text'>"
	return "<div class='form-group row'>"

def CloseDiv():
	return "</div>\n"

def CheckBox(CheckBoxID):
	# return "<input type='checkbox'>"
	return "<input class='form-check-input' type='checkbox' value='' id='checkbox"+str(CheckBoxID)+"' onclick='AccordionSelectForCheckBox("+str(CheckBoxID)+")';>"

def InBold(TextToShowInBold,CheckBoxID):
	# return "<p style='margin-left: 46px;'>"+TextToShowInBold+": "
	return "<label class='form-check-label' for='checkbox"+str(CheckBoxID)+"'>"+TextToShowInBold+"</label>"
  

def ShowAsterisk(Value):
	AsteriskLabel = "( ""<span style='color:red'>*</span> "")</p>"
	if Value == "0": AsteriskLabel = ""
	return AsteriskLabel

def Header():
	return """
		<head><meta charset='UTF-8'>
    	<meta name="viewport" content="width=device-width, initial-scale=1">
  		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.0/css/bootstrap.min.css">
		</head>
		"""

def BodyOpen():
	return """
		<body>
		<div class='container'>
		"""

def BodyHTMLClose():
	return """
		</div>
		</body>
		</html>
	"""


def HTMLTree(HTMLTreeID):
	FinalID = str(HTMLTreeID)
	return "<div id='HTMLTree"+FinalID+"' class='col-auto mr-auto' onclick=\"SendSelected("+FinalID+",$('#HTMLTree"+FinalID+"').fancytree('getTree').getSelectedNodes())\"></div>"
	# <label><span id='echoSelection"+str(HTMLTreeID)+"'></span></label>

def TextBox(ChildID):
	return "<input type='text' style= 'width:auto; margin-left:30px;' name='R6$" + ChildID.encode('utf-8') + "' class='form-control' id='userdataentry' placeholder='Donner une valeur'>"

def CollapseHeader(ID,ChildName, HTMLTreeID):
	# try:
	# 	ChildName = ChildName.encode('utf-8')
	# except:
	# 	ChildName = "MMM"
	return "<div class='card'><div class='card-header collapseclass SpecialClassToHide"+str(HTMLTreeID)+"' id='heading"+str(ID)+"' style='display:none;'><h2 class='mb-0'><button class='btn btn-link collapsed' type='button' data-toggle='collapse' data-target='#collapse"+str(ID)+"' aria-expanded='false' aria-controls='collapse"+str(ID)+"'>"+ChildName+"</button></h2></div>"

def CollapseBody(ID,HTMLTreeID,Content):
	Body = "<div id='collapse"+str(ID)+"' class='collapse' aria-labelledby='heading"+str(ID)+"' data-parent='#Accordion"+str(HTMLTreeID)+"'><div class='card-body'>"+Content.decode('utf-8')+"</div></div></div>"
	# Body = Body.decode('latin-1')
	return Body

def HTMLAccordion(HTMLTreeID,AccordionContent):
	return "<div class='accordion col-sm-4 ml-auto' id='Accordion"+str(HTMLTreeID)+"'>"+ AccordionContent.encode('utf-8')+"</div>"

def CollapseContent(Items,Quantifiable, ChildID, ChildNameID, ID):
	Output = ""
	if len(Items) != 0:
		Output = "<label for=''>Selectionner ou saisir une nouvelle entreé: </label><select multiple='multiple' class='form-control'  style='overflow-x: auto; white-space: nowrap;' name='R3$" + ChildID.encode('utf-8') + '$' + ChildNameID.encode('utf-8') + '$' + str(ID)+"[]'>"
		for Item in Items: Output += "<option>"+Item+"</option>"
		Output += "</select>"
	if Quantifiable == True: 
		Output += "<br><input class='form-control' data-role='tagsinput' type='text' name='R2$" + ChildID.encode('utf-8') + '$' + ChildNameID.encode('utf-8') + '$' + str(ID)+ " ' placeholder='Preciser le nombre requis'>"
	else: 
		Output += "<br><input class='form-control' data-role='tagsinput' type='text' name='R1$" + ChildID.encode('utf-8') + '$' + ChildNameID.encode('utf-8') + '$' + str(ID)+ " ' placeholder='Donner un nom ou une URL.'>"
	return Output

def PHPInitializers():
	Output = ""
	Output += "<?php session_start();\n"
	Output += "include '../../db_connection.php';\n"
	Output += "$_SESSION['CurrentProperty'] = $_GET['PropertyID'];\n"
	Output += "$ExpertID = $_SESSION['SessionID'];\n"
	Output += "$PropertyID = $_SESSION['CurrentProperty'];\n"
	Output += "$QueryStatus = \"INSERT INTO `ExpertFillingStatus` (`StatusID`, `ExpertID`, `PropertyID`, `Status`) VALUES (NULL, '$ExpertID', '$PropertyID', '0');\";\n"
	Output += "$Conn->query($QueryStatus) or die(mysqli_error($Conn));\n?>\n"
	return Output

def Footnote():
	Output = ""
	Output += "<footer class='pt-4 my-md-5 pt-md-5 border-top'>\n"
	Output += "<div class='row'>\n"
	Output += "<div class='col-12 col-md'>\n"
	Output += "<p><b>OntoSamsei</b></p> <small class='d-block mb-3 text-muted'>&copy; 2019-2020</small></div>\n</div>\n</footer>\n"
	return Output

def RecapTime():
	Output = ""
	Output += "$LastFillingTime = -1;\n"
	Output += "$QueryLastTimeOfFilling = \"select max(FillingTime) as 'MaxTime' from Fillings where ExpertID = '$ExpertID' and PropertyID = '$PropertyID'\";\n"
	Output += "$QueryLastTimeOfFillingResults = mysqli_query($Conn, $QueryLastTimeOfFilling);\n"
	Output += "while ($QueryLastTimeOfFillingResult = mysqli_fetch_array($QueryLastTimeOfFillingResults,MYSQLI_BOTH)) {\n"
	Output += "$LastFillingTime = $QueryLastTimeOfFillingResult['MaxTime']; }\n"
	Output += "$FormattedLastFillingTime = date(\"j/m/Y à H\hm\", strtotime($LastFillingTime));\n?>\n"
	return Output

def RecapBox():
	Output = ""
	Output += "<?php $RecapShow = True;\n$Recap = \"\";\n"
	Output += "$QueryRecap = \"select AttributeName, AttributeValue from Fillings where ExpertID = '$ExpertID' and PropertyID = '$PropertyID'\";\n"
	Output += "$Conn->set_charset(\"utf8\");\n"
	Output += "$QueryRecapResults = mysqli_query($Conn, $QueryRecap);\n$QueryRecapNumRows = $QueryRecapResults->num_rows;\n"
	Output += "if ($QueryRecapNumRows == 0) {\n $RecapShow = False; \n }\n"
	Output += "else {\n"
	Output += "while ($QueryRecapResult = mysqli_fetch_array($QueryRecapResults,MYSQLI_BOTH)) {\n"
	Output += "$AttributeName = $QueryRecapResult['AttributeName'];\n"
	Output += "$AttributeNamePieces = explode(\"\$\", $AttributeName);\n"

	Output += "$AttributeNamePiece1 = str_replace(\"_\", \".\", $AttributeNamePieces[1]);\n"
	Output += "$AttributeNamePiece1Label = $AttributeNamePiece1;\n"
	Output += "$AttributeNamePiece2 = \"\";\n"
	Output += "if (count($AttributeNamePieces)>2)\n{\n"
	Output += "$AttributeNamePiece2 = $AttributeNamePieces[2];\n"
	Output += "$SubPieces = explode(\"#\", $AttributeNamePiece2);\n"

	Output += "$SubPiece1 = str_replace(\"_\", \".\",$SubPieces[0]);\n"
	Output += "$AttributeNamePiece2 = $SubPiece1 . \"#\" . $SubPieces[1];\n}\n"
	Output += "$AttributeNamePiece2Label = $AttributeNamePiece2;\n"
	Output += "$QueryAttributeNamePiece1Label = \"select Label from OntologyIdentifiers where Identifier = '$AttributeNamePiece1'\";\n"
	Output += "$QueryAttributeNamePiece1LabelResults = mysqli_query($Conn, $QueryAttributeNamePiece1Label);\n"
	Output += "while ($QueryAttributeNamePiece1LabelResult = mysqli_fetch_array($QueryAttributeNamePiece1LabelResults,MYSQLI_BOTH))\n{\n"
	Output += "$AttributeNamePiece1Label = $QueryAttributeNamePiece1LabelResult[\"Label\"];\n}\n"
	Output += "$QueryAttributeNamePiece2Label = \"select Label from OntologyIdentifiers where Identifier = '$AttributeNamePiece2'\";\n"
	Output += "$QueryAttributeNamePiece2LabelResults = mysqli_query($Conn, $QueryAttributeNamePiece2Label);\n"
	Output += "while ($QueryAttributeNamePiece2LabelResult = mysqli_fetch_array($QueryAttributeNamePiece2LabelResults,MYSQLI_BOTH))\n{\n"
	Output += "$AttributeNamePiece2Label = $QueryAttributeNamePiece2LabelResult[\"Label\"];\n}\n"
	Output += "$AttributeValue = $QueryRecapResult[\"AttributeValue\"];\n"
	Output += "if ($AttributeValue == \"on\") $AttributeValue = \"\";\n"
	# Output += "$Recap = $Recap . \"<p><span style='color:blue'>\".$QueryRecapResult[\"PropertyName\"].\"</span>\";\n"
	# Output += "if ($AttributeNamePiece1Label != $QueryRecapResult[\"PropertyName\"])\n{\n"
	Output += "$Recap = $Recap . \" <p><span style='color:blue'>(\".$AttributeNamePiece1Label.\")</span>\";\n"


	Output += "if ($AttributeNamePiece2Label != \"\")\n{\n"
	Output += "$Recap = $Recap.\" : \".$AttributeValue.\" <span style='color:green'>(\".$AttributeNamePiece2Label.\")</span></p>\";\n}\n"

	# Output += "$Recap = $Recap.\" :  <span style='color:green'>\".$AttributeNamePiece2Label.\"</span>  &#8680; \".$AttributeValue.\"</p>\";\n}\n"
	Output += "else\n{$Recap = $Recap.\" : \".$AttributeValue.\"</p>\";\n}\n"
	Output += "}\n}\n"    		
	Output += RecapTime()
	Output += "<?php if ($RecapShow == True) { ?>\n"
	Output += "<p><a class='btn btn-primary' data-toggle='collapse' href='#CollapseRecap' role='button' aria-expanded='false' aria-controls='CollapseRecap'>Récaptulatif de la saisie des données du <?php echo($FormattedLastFillingTime); ?></a></p>\n"
	Output += "<div class='collapse' id='CollapseRecap'><div class='card card-body'><?php echo($Recap); ?></div></div>\n<br>\n"
	Output += "<?php } // end for ?>\n"
	return Output



      