import random
import string
from datetime import date
import random
import string
from datetime import date


html_main ="""
<!doctype html>
<html lang="en">
  <head>
	<meta charset="utf-8">
	<title>C Documentation generator</title>
  </head>
  <body>
	%s
  </body>
</html>
"""

class Directory:
	def __init__(self, name, link):
		self.name = name
		self.link = link
		self.files = list()

class File:
	def __init__(self, name, link):
		self.name = name
		self.link = link

def checkExtension(filename):
	extensions=('.h', '.c')
	return filename.endswith(extensions)

def generateDirPage(directory, files, md):
	body = makeFilesList(directory, files)
	m = """	    %s
		  		<h4>%s</h4>
	"""

	t=html_main % m
	return t % (body, md.replace("\n", "<br />"))

def makeFilesList(directory, files):
	content = "\n".join([createLinkDirFile(directory, file) for file in files])
	return """
	<ul>
	  %s
	</ul>
	""" % content


def createLinkDirFile(directory, file):
	isFile = checkExtension(file)
	folderAdd = "" if isFile else " (folder)"
	return '<li><a href="%s">%s</a></li>' % ((directory + "/" + file + ".html"), file + folderAdd)

class Directory:
	def __init__(self, name, link):
		self.name = name
		self.link = link
		self.files = list()

class File:
	def __init__(self, name, link):
		self.name = name
		self.link = link

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def generateIndex(projectName, rootPage, directory):
	referencesContent = makeDirectoryHierachy(directory) if isinstance(directory, Directory) else createReferenceLink(directory)
	html="""
	  	<h1>%s</h1>
	  	<p>C documentation generator</p>
	  	<p style="font-size: 0.75em">Generation date: %s</p>
	  	<h3><a href="%s">Project Documentation</a></h3>
	  	<h3><a href="references.html">Objects References</a></h3>

	    %s

	"""
	t= html_main % html
	return t % (projectName, date.today(), rootPage, referencesContent)

def makeDirectoryHierachy(directory):
	directoryContent = "\n".join([makeDirectoryHierachy(file) if isinstance(file, Directory) else createLinkedItem(file) for file in directory.files])
	idHead = randomString()
	idCollapse = randomString()
	return """
	<div>
         <div id="%s">
            <h5>
              	<button type="button" data-toggle="collapse" data-target="#%s" aria-expanded="true" aria-controls="%s">
                	%s
              	</button> <a href="%s#%s">(link here)</a>
            </h5>
        </div>
		<div id="%s" aria-labelledby="%s">
            <div>
              		%s
            </div>
         </div>
    </div>
	""" % (idHead, idCollapse, idCollapse, directory.name, directory.link, idHead, idCollapse, idHead, directoryContent)

def createLinkedItem(file):
	idHead = randomString()
	return """
	<div>
         <div id="%s">
            <h5>
              	<a href="%s#%s">%s</a>
            </h5>
        </div>
    </div>
	""" % (idHead, file.link, idHead, file.name)

class C_Object:
	name = ""
	comment = ""
	declarations = list()
	functions = list()

	def __init__(self, name, comment, declarations, functions):
		self.name = name
		self.comment = comment
		self.declarations = declarations
		self.functions = functions


class Declaration:
	comment = ""
	name = ""

	def __init__(self, name, comment):
		self.name = name
		self.comment = comment

def generateFilePage(fileComment, objects):
	body = "\n".join([objectToHtml(object) + "\n" for object in objects])
	html = """
	  	<h5>%s</h5>
	    %s

	"""
	return html_main % html % (fileComment.replace('//', '<br>'), body)

def objectToHtml(object):
	content = listFunctions(object.functions)
	declarations = makeDeclarations(object.declarations)
	return """
	<div>
	  <div> %s</div>
	  <div> %s </div>
	  <div>
	  	%s
	    %s
	  </div>
	</div>
	""" % (object.comment.replace(' /// ', '<br> /').replace(' // ', '<br> /'), object.name, declarations, content)

def makeDeclarations(declarations):
	content = "\n".join([createItem(declaration) for declaration in declarations])
	return """
	<div>
	  <ul>
	    %s
	  </ul>
	</div>
	""" % content

def createItem(text):
	return '<li>%s</li>' % (text.replace('<', '&lt'))

def listFunctions(functions):
	text = "\n".join([function_to_html(func) + "\n" for func in functions])
	return """
	  %s
	""" % text

def function_to_html(function):
	return """
 		<p>
        	<button type="button" data-toggle="collapse" data-target="#%s" aria-expanded="false" aria-controls="%s">%s</button>
      	</p>
      	<div>
    		<div>
      			%s
    		</div>
      	</div>

	""" % (id, id, function.name.replace('<', '&lt'), function.comment.replace('///', '<br>').replace('//', '<br>'))

def generateReferences(references):
	referencesContent = makeReferencesList(references)
	html=	"""
			<h1>Objects references:</h1>

			%s
	"""
	return html_main % html % (referencesContent)

def makeReferencesList(references):
	content = "\n".join([createReferenceLink(reference) for reference in references])
	return """
	<ul>
	  %s
	</ul>
	""" % content

def createReferenceLink(reference):
	return '<li><a href="%s">%s</a></li>' % (reference[1], reference[0])
