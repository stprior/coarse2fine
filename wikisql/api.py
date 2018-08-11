import graphene
from flask_graphql import GraphQLView
from flask import Flask
from schema import build_schema
import apprun
import engine

(rootQueryClass,mutationsClass) = build_schema('/home/stevop/repos/coarse2fine/data_model/wikisql/data')
schema = graphene.Schema(query=rootQueryClass, mutation=mutationsClass)

app = Flask(__name__)

#(translator, opt) = apprun.initialise(app)

@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers']= 'Origin, X-Requested-With, Content-Type, Accept'
    return response

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

engine.init('/home/stevop/repos/coarse2fine/data_model/wikisql')

# Optional, for adding batch query support (used in Apollo-Client)
#app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view('graphql', schema=schema, batch=True))
