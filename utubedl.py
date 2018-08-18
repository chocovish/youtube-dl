from flask import Flask, request, render_template, jsonify
from pytube import YouTube


app = Flask(__name__)


@app.route("/")
def home():
	return render_template('home.html')

@app.route('/download/')
def download():
	url = request.args.get("url",None)
	if url == None: return 'no url given'
	yt = YouTube(url)
	return render_template('download.html',obj = yt, int=int)


@app.route('/api/info/')
def info():
	url = request.args.get('url',None)
	if 'youtu' not in url: return jsonify(error="not an youtube url or no url given")
	yt = YouTube(url)
	yt = convert(yt)
	return jsonify(yt)



def convert(obj):
	data = {'title':obj.title, 'description':obj.description[:260], 'thumbnail_url':obj.thumbnail_url, 'length':"{}min {}sec".format(int(int(obj.length)/60), int(obj.length)%60), 'streams':[], }
	for v in obj.streams.all():
		d = {'mime_type':v.mime_type, 'url':v.url, 'resolution':v.resolution, 'video_only': not v.includes_audio_track, 'size': int(v.filesize/1048576),}
		data['streams'].append(d)
	return data


if __name__=="__main__":
	app.run(debug=True, host='0.0.0.0', port=8080)