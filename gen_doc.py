from os import listdir, mkdir, walk
from os.path import *
import sys
from c_parser import *
import argparse
from html_converter import *

def lookupMD(path, files):
	for file in files:
		fullname = (path + "/" + file)
		if isfile(fullname) and (fullname).endswith(".md"):
			readme = open(fullname, mode="r")
			text = readme.read()
			readme.close()
			return text
	return "No readme file"

def getFilesAndDirs(path):
	res = []
	for root, dirs, files in os.walk(path):
		for d in dirs:
			res.append(d)
		for f in files:
			if checkExtension(f):
				res.append(f)
	return res

def parse_dir(prefix, path, workingDirectory):
	references = dict()
	allPath = prefix + path
	md = ""
	if isfile(allPath) and checkExtension(allPath):
		name = basename(path)
		path = dirname(path) + "/"
		references.update(parse_file(prefix, path + "/", workingDirectory, name))
		return references, File(basename(allPath),'%s/%s%s.html' % (workingDirectory, path, name))
	elif isdir(allPath):
		directory = Directory(basename(allPath), workingDirectory + "/" + path + ".html")
		if not exists(workingDirectory + "/" + path):
			mkdir(workingDirectory + "/" + path)
		files = listdir(allPath + "/")
		file = open(workingDirectory + "/" + path + ".html", mode="w")
		md = lookupMD(allPath, files)
		file.write(generateDirPage(basename(path), getFilesAndDirs(allPath), md))
		file.close()
		for file in files:
			filereferences, fileObj = parse_dir(prefix, path + "/" + file, workingDirectory)
			references.update(filereferences)
			if fileObj is not None:
				directory.files.append(fileObj)
		return references, directory
	else:
		return  dict(), None


def parse_project(projectPath, outputPath):
	projectName = basename(projectPath)
	if not exists(outputPath):
		mkdir(outputPath)

	prefix = dirname(projectPath) + "/" if len(dirname(projectPath)) > 0 else ""

	if isfile(projectPath) and checkExtension(projectPath):
		path = "/" if len(dirname(projectPath)) > 0 else ""
		references = parse_file(dirname(projectPath), path, outputPath, basename(projectPath))
		rootDirectory = File(basename(projectPath),'%s.html' % (outputPath + '/' + basename(projectPath)))
		rootProject = outputPath + "/" + projectName + ".html"
	else:
		references, rootDirectory = parse_dir(prefix, projectName, outputPath)
		rootProject = outputPath + "/" + projectName + ".html"
	sorted_references = sorted(references.items(), key=lambda kv: kv[0])
	index = generateIndex(projectName, rootProject, rootDirectory)
	page = open("index.html", mode='w')
	page.write(index)
	page.close()
	refFile = open("references.html", mode='w')
	refFile.write(generateReferences(sorted_references))
	refFile.close()


parser = argparse.ArgumentParser()
parser.add_argument("--src", help="Path to generate C documentation from", required=True)
parser.add_argument("--dest", help="Path to save result", required=True)
args = parser.parse_args()
parse_project(args.src, args.dest)
exit()
