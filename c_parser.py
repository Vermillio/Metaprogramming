import re
import os
from html_converter import *

# function remove all bodies from functions and inner objects
def removeBody(text):
	newText = ""
	prevText = ""
	level = 0
	isComment=False
	isCommentMultiline=False
	isDefine=False

	for i in range(0, len(text)):
		char=text[i]
#		prevText += char
		if text[i:i+1]=='//':
			isComment=True
		if char=='\n':
			isComment=False
		if text[i:i+1]=='/*':
			isCommentMultiline=True
		if text[i:i+6]=="#ifdef" or text[i:i+7]=="#ifndef":
			isDefine=True

		if char=='*' and text[i+1]=='/':
			isCommentMultiline=False
		if text[i:i+6]=="#endif":
			isDefine=False

		if char == '{' and not isDefine and not isComment and not isCommentMultiline:
			level += 1
		if level <= 0:
			newText += char
		if char == '}':
			level-=1
			if level<=0:
				toDelete = False

	return newText


# get name of object from declaration line
def getObjectName(objName):
	return objName.partition(":")[0].partition("<")[0].split()[-1]

commentPattern=r"(?:\/\/([^\n]+\n))+"
commentMultilinePattern=r"\/\*([\S\s]+?)\*\/"

funcPattern=r"\A[\t ]*(?:(?:static|const)[\t ]+)*([A-Za-z_]+[\t ]+\(?\*?[A-Za-z_]+\)?\([A-Za-z_ *()]+\))"
objPattern=r"\A[\t ]*(?:(?:typedef|const)[\t ]+)*((?:struct|enum)[\t ]+([A-Za-z_]+)?[^\n=;]+);?"

def getObjects(text):
	objects=[]
	C_Object = C_Object("Global", "", list(), list())
	objects.append(C_Object)
	multilineComments=re.finditer(commentMultilinePattern, text, flags=re.MULTILINE)
	startComment = re.search("\A\s*("+commentMultilinePattern+")", text, flags=re.MULTILINE)
	endComment=re.search("\A\s*("+commentMultilinePattern+")", text[::-1], flags=re.MULTILINE)
	if endComment:
		endComment=endComment[::-1]
	textWithoutMultilineComments = []

	lastPos=0
	comments=""
	count = 0
	for comm in multilineComments:
		count += 1
		m=comm.span()
		currentText = text[m[1]:].replace('\n', '')
		if lastPos != 0:
			textWithoutMultilineComments.append(text[lastPos:m[0]-1])
			lastPos = m[1]

		functionMatch = re.search(funcPattern, currentText )
		if functionMatch:
			next = Declaration(functionMatch.group(), comm.groups()[0] if len(comm.groups()[0]) > 0  else "No comment")
			C_Object.functions.append(next)
		else:
			objectMatch = re.search(objPattern, currentText)
			if objectMatch:
				next = C_Object(objectMatch.group(), comm.groups()[0] if len(comm.groups()[0]) > 0 else "No comment", list(), list())
				objects.append(next)
				C_Object.declarations.append(objectMatch.groups()[0])
			else:
				comments = '\n'.join([comments, comm.groups()[0]])

	# search comments and use it as file description
	comments='\n'.join(re.findall(commentPattern, ''.join(textWithoutMultilineComments)))
	C_Object.comment = '\n'.join([startComment.groups()[0] if startComment is not None else '', comments, startComment.groups()[0] if endComment is not None else ''])

	return comments, objects

def parse_file(prefix, path, workingDirectory, name):
	filename = '%s%s' % (prefix + path, name)
	print("Parsing file %s" % filename)
	file = open(filename, mode='r')
	text = file.read()
	file.close()
	(fileComment, objects) = getObjects(removeBody(text))

	text = generateFilePage(fileComment, objects)
	pageName = '%s/%s%s.html' % (workingDirectory, path, name)
	page = open(pageName, mode='w')
	page.write(text)
	page.close()
	# add objects to references if it is not global
	classReference = list(filter(lambda o: not o.name.find("Global") != -1, objects))
	processedReferences = { getObjectName(o.name): pageName for o in classReference }
	return dict(processedReferences)
