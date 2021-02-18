def HTMLTree(HTMLTreeID,Tree):
	# return "$(function(){ $(\"#HTMLTree"+str(HTMLTreeID)+"\").fancytree({ checkbox: true, selectMode: 2, icon: false, source: ["+ Tree +"], init: function(event, data) { data.tree.visit(function(n) { n.key = n.title.split(\" \")[0]; }); }, select: function(event, data) { var selNodes = data.tree.getSelectedNodes(); var selKeys = $.map(selNodes, function(node){ return \"[\" + node.key + \"]: \'\" + node.title + \"\'\"; }); $(\"#echoSelection"+str(HTMLTreeID)+"\").text(selKeys.join(\", \")); }, cookieId: \"fancytree-Cb2\", idPrefix: \"fancytree-Cb2-\" }); });"
	return "$(function(){ $(\"#HTMLTree"+str(HTMLTreeID)+"\").fancytree({ checkbox: false, selectMode: 2, icon: false, source: ["+ Tree +"], init: function(event, data) { data.tree.visit(function(n) { n.key = n.title.split(\" \")[0]; }); }, select: function(event, data) { var selNodes = data.tree.getSelectedNodes(); var selKeys = $.map(selNodes, function(node){ return \"\" + node.title + \"\"; }); $(\"#echoSelection"+str(HTMLTreeID)+"\").text(selKeys.join(\", \")); }, cookieId: \"fancytree-Cb2\", idPrefix: \"fancytree-Cb2-\" }); });"

def TreeAccordionConnector():
	Script = "function SendSelected(HTMLTreeID,CollapseIDToShow) { "
	Script += "var AllDivsToHide = document.getElementsByClassName('SpecialClassToHide'.concat(HTMLTreeID)); "
	Script += "var NbAllDivsToHide = AllDivsToHide.length; "
	Script += "for (i = 0; i < NbAllDivsToHide; i++) { "
	Script += "AllDivsToHide[i].style.display = 'none';} "
	Script += "L = CollapseIDToShow.length; "
	Script += "for (i = 0; i < L; i++) { "
	Script += "document.getElementById('heading'.concat(CollapseIDToShow[i].refKey)).style.display = 'block';} }"
	return Script

def Replicator():
	Script = "function SendToReplicate(HTMLTreeID,IDToShow) { "
	Script += "var AllPropertyDivsToHide = document.getElementsByClassName('SpecialPropertyClassToHide'.concat(HTMLTreeID)); "
	Script += "var NbAllPropertyDivsToHide = AllPropertyDivsToHide.length; "
	Script += "for (i = 0; i < NbAllPropertyDivsToHide; i++) { "
	Script += "AllPropertyDivsToHide[i].style.display = 'none';} "
	Script += "L = IDToShow.length; "
	Script += "for (i = 0; i < L; i++) { "
	Script += "document.getElementById('PropertyDiv'.concat(IDToShow[i].refKey)).style.display = 'block';} }"
	return Script

def CheckboxAccordionConnector():
	Script = "function AccordionSelectForCheckBox(CheckboxID) { "
	Script += "Checked = document.getElementById('checkbox'.concat(CheckboxID)).checked;"
	Script += "if (Checked == true) {"
	Script += "document.getElementById('heading'.concat(CheckboxID)).style.display = 'block'; }"
	Script += "else {"
	Script += "document.getElementById('heading'.concat(CheckboxID)).style.display = 'none'; }"
	Script += "}"
	return Script