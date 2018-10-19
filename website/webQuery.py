from flask import Flask, url_for, render_template, request, redirect
import sys
sys.path.append('../')
import retrival
sys.path.append('website')
import time
import urllib

app = Flask(__name__)

links = []

@app.route('/<nextQ>', methods=['POST', 'GET'])
def homeRedirect(nextQ):
	error = None
	if request.method == 'GET':
		pastTime = time.time()
		text = nextQ
		linkObj = retrival.Retrival()
		linkObj.searchRequest(str(text))
		links = linkObj.flink

		for link in links:
			links[links.index(link)] = urllib.parse.unquote(link)

		dym = linkObj.dym
		if dym != [None]:
			dym	= ' '.join(dym)

		t = str(time.time() - pastTime)

		if links != []:
			return render_template('index.html', name=links, timming=t)
		elif links == []:
			if dym == [None] or dym == []:
				return render_template('index.html', error='Search Not Found!', timming=t)
			elif dym != [None]:
				return render_template('index.html', instead=dym, timming=t)

		error = 'Invalid'

	elif request.method == 'POST':
		return redirect("", code=303)

	return render_template('index.html', error=error)



@app.route('/', methods=['POST', 'GET'])
def home():
	error = None
	if request.method == 'POST':
		if request.form['query']:
			pastTime = time.time()
			text = request.form['query']
			linkObj = retrival.Retrival()
			linkObj.searchRequest(str(text))
			links = linkObj.flink
			dym = linkObj.dym
			if dym != [None]:
				dym	= ' '.join(dym)

			for link in links:
				links[links.index(link)] = urllib.parse.unquote(link)

			t = str(time.time() - pastTime)

			if links != []:
				return render_template('index.html', name=links, timming=t)
			elif links == []:
				if dym == [None] or dym == []:
					return render_template('index.html', error='Search Not Found!', timming=t)
				elif dym != [None]:
					return render_template('index.html', instead=dym, timming=t)
			error = 'Invalid'
	return render_template('index.html', error=error)

if __name__ == '__main__':
	app.run()