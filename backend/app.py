from flask import Flask,request,json,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    sprite = db.Column(db.String, unique=True)
    fg = db.Column(db.String)
    bg = db.Column(db.String)
    desc = db.Column(db.String)

    def __init__(self, name, sprite, fg, bg, desc):
        self.name = name
        self.sprite = sprite
        self.fg = fg
        self.bg = bg
        self.desc = desc

class PokemonSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','name', 'sprite','fg','bg','desc')
    
pokemon_schema=PokemonSchema()
pokemons_schema=PokemonSchema(many=True)

@app.errorhandler(404)
def not_found(e):
   return render_template("404.html"), 404

@app.route("/api/pokemon/", methods=["POST"])
def add_pokemon():
    pk=request.get_json()
    if len(pk["pokemon"]["name"])>50:
        return("Name value has exceeded the limit...")
    name = pk["pokemon"]["name"]
    if len(pk["pokemon"]["sprite"])>300:
        return("sprite value has exeeded the limit...")
    sprite = pk["pokemon"]["sprite"]
    fg = pk["pokemon"]["cardColours"]["fg"]
    bg = pk["pokemon"]["cardColours"]["bg"]
    desc = pk["pokemon"]["cardColours"]["desc"]
    new_pk = Pokemon(name, sprite, fg, bg, desc)
    db.session.add(new_pk)
    db.session.commit()
    pkdata = Pokemon.query.filter(Pokemon.name==name).first()
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

@app.route('/api/pokemon/',methods=["GET"])
def get_all_pokemon():
    all_pks = Pokemon.query.all()
    if(all_pks==None):
        return render_template("404.html"), 404
    result = pokemons_schema.dump(all_pks)
    re=[]
    for i in result.data:
        pk = {"pokemon":{"id":i["id"],"name":i["name"],"sprite":i["sprite"],"cardColours":{"fg":i["fg"],"bg":i["bg"],"desc":i["desc"]}}}
        re.append(pk)
    return jsonify(re)


@app.route("/api/pokemon/<int:id>", methods=["PATCH"])
def update_pokemon(id):
    pkdata = Pokemon.query.get(id)
    if (pkdata==None):
        return render_template("404.html"), 404
    else:
        pk=request.get_json()
        if len(pk["pokemon"]["name"])>50:
            return("Name value has exceeded the limit...")
        if len(pk["pokemon"]["sprite"])>300:
            return("sprite value has exeeded the limit...")
        pkdata.name = pk["pokemon"]["name"]
        pkdata.sprite = pk["pokemon"]["sprite"]
        pkdata.fg = pk["pokemon"]["cardColours"]["fg"]
        pkdata.bg = pk["pokemon"]["cardColours"]["bg"]
        pkdata.desc = pk["pokemon"]["cardColours"]["desc"]
        db.session.commit()
        pkdata = Pokemon.query.get(id)
        pk = {"pokemon":{"id":pkdata.id,"name":pkdata.name,"sprite":pkdata.sprite,"cardColours":{"fg":pkdata.fg,"bg":pkdata.bg,"desc":pkdata.desc}}}
        return json.dumps(pk)


@app.route("/api/pokemon/<int:id>", methods=["DELETE"])
def delete_pokemon(id):
    pkdata = Pokemon.query.get(id)
    if (pkdata==None):
        return render_template("404.html"), 404
    pk = {"pokemon":{"id":pkdata.id,"name":pkdata.name,"sprite":pkdata.sprite,"cardColours":{"fg":pkdata.fg,"bg":pkdata.bg,"desc":pkdata.desc}}}
    db.session.delete(pkdata)
    db.session.commit()
    return json.dumps(pk)

if __name__ == '__main__':
    app.run(host='localhost', port=8006, debug=True)
