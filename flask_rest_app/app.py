from __future__ import division
from flask import Flask, jsonify, request, abort, render_template


counter = 0

app = Flask(__name__)

urls = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/all')
def all():
	return jsonify({'urls': urls})

# Get long url by id 
@app.route('/<string:url_id>', methods=['GET'])
def get_url(url_id):
	id_ = [url for url in urls if url['id'] == url_id]
	url_ = [url for url in urls if url['url'] == url_id]
	if len(id_) != 0: return jsonify({'url': id_[0]['url']}), 301
	if len(url_) != 0: return jsonify({'id': url_[0]['id']}), 200
	return jsonify({'error': 'Not found'}), 404


# posts new urls with id
@app.route('/', methods=['POST'])
def post_or_delete():
	print request.form
	if request.form.get('newurl') != '':
		create_new()
		return jsonify({'urls': urls}), 201

	elif request.form.get('delurl') != '':
		del_url()
		return jsonify({'urls': urls}), 204
	return jsonify({'error': 'no url or id inserted'}), 400


def create_new():
	global counter

	url = {
		'id': encode_id(counter),
		'url': request.form.get('newurl')
	}
	urls.append(url)
	counter = counter + 1

# del url with button
def del_url():
	url_id = request.form.get('delurl')
	for i in range(len(urls)):
		if urls[i]['url'] == url_id:
			print urls[i]
			urls.pop(i)
			break
		if urls[i]['id'] == url_id:
			urls.pop(i)
			break

@app.route('/', methods=['DELETE'])
def delete_url():
	if not request.json:
		return jsonify({'error': 'No url found'}), 400
	if 'id' in request.json: x = 'id'
	if 'url' in request.json: x = 'url'
	print x
	for i in range(len(urls)):
		if urls[i][x] == request.json[x]:
			print urls[i][x]
			urls.pop(i)
			return jsonify({'urls': urls}), 204
	return jsonify({'error': 'No url found'}), 400

@app.route('/', methods=['PUT'])
def put_url():
	if not request.json:
		return jsonify({'error': 'Not found'}), 400
	if 'id' in request.json and 'url' in request.json:
		for i in range(len(urls)):
			if urls[i]['id'] == request.json['id']:
				urls[i]['url'] = request.json['url']
				return jsonify({'urls': urls}), 200
	return jsonify({'error': 'Not found'}), 404

def encode_id(num):
	base_list = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
	if num == 0:
		return '0'
	l = len(base_list)
	unique_id = ''
	while num != 0:
		unique_id = base_list[int(num % l)] + unique_id
		num = int(num / l)
	return unique_id

if __name__ == '__main__':
    app.run(debug=True)
