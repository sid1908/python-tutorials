import os, time
from flask import Flask, render_template, request
import sqlite3 as sql
from werkzeug import secure_filename

app = Flask(__name__)

# Default folder setting for image upload
UPLOAD_FOLDER = os.path.basename('images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def person():
	return render_template('person.html')


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
	if request.method == 'POST':
		try:
			name = request.form['name']
			file = request.files['image']
			f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
			file.save(f)

			with sql.connect("database.db") as con:
				cur = con.cursor()

				cur.execute("INSERT INTO peoples(name, img_path) VALUES (?, ?)", (name, f))

				con.commit()
				msg = "Record successfully added"
		except:
			con.rollback()
			msg = "error in insert operation"

		finally:
			return render_template("result.html",msg = msg)
			con.close()


if __name__ == '__main__':
	app.run(debug = True)