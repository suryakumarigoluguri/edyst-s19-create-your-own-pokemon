from flask import Flask,request,json,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    sprite = db.Column(db.String(300), unique=True)
    fg = db.Column(db.String)
    bg = db.Column(db.String)
    desc = db.Column(db.String)

    def __init__(self, name, sprite, fg, bg, desc):
        self.name = name
        self.sprite = sprite
        self.fg = fg
        self.bg = bg
        self.desc = desc

@app.errorhandler(404)
def not_found(e):
   return render_template("404.html"), 404

@app.route("/api/pokemon", methods=["POST"])
def add_pokemon():
    pk=request.get_json()
    name = pk["pokemon"]["name"]
    sprite = pk["pokemon"]["sprite"]
    fg = pk["pokemon"]["cardColours"]["fg"]
    bg = pk["pokemon"]["cardColours"]["bg"]
    desc = pk["pokemon"]["cardColours"]["desc"]
    new_pk = Pokemon(name, sprite, fg, bg, desc)
    db.session.add(new_pk)
    db.session.commit()
    pkdata = Pokemon.query.get(name==name).first()
    pk = {"pokemon":{"id":pkdata.id,"name":pkdata.name,"sprite":pkdata.sprite,"cardColours":{"fg":pkdata.fg,"bg":pkdata.bg,"desc":pkdata.desc}}}
    return json.dumps(pk)

@app.route('/api/pokemon/<int:id>',methods=["GET"])
def get_pokemon(id):
    pkdata = Pokemon.query.get(id)
    if (pkdata!=None):
        pk = {"pokemon":{"id":pkdata.id,"name":pkdata.name,"sprite":pkdata.sprite,"cardColours":{"fg":pkdata.fg,"bg":pkdata.bg,"desc":pkdata.desc}}}
        return json.dumps(pk)
    else:
        return render_template("404.html"), 404

@app.route("/api/pokemon/<int:id>", methods=["PATCH"])
def update_pokemon(id):
    pkdata = Pokemon.query.get(id)
    if (pkdata==None):
        return ("ID is not present so we can't update")
    else:
        add_pokemon()
    #user = User.query.get(id)
    #username = request.json['username']
    #email = request.json['email']
    #user.email = email
    #user.username = username
    #db.session.commit()
    #return user_schema.jsonify(user)

@app.route("/api/pokemon/<int:id>", methods=["DELETE"])
def delete_pokemon(id):
    pkdata = Pokemon.query.get(id)
    if (pkdata==None):
        return ("ID is not present so we can't delete")
    pk = {"pokemon":{"id":pkdata.id,"name":pkdata.name,"sprite":pkdata.sprite,"cardColours":{"fg":pkdata.fg,"bg":pkdata.bg,"desc":pkdata.desc}}}
    db.session.delete(pkdata)
    db.session.commit()
    return json.dumps(pk)

if __name__ == '__main__':
    app.run(host='localhost', port=8006, debug=True)