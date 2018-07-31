import graphene
from flask_graphql import GraphQLView
from flask import Flask
from schema import RootQuery
import apprun


schema = graphene.Schema(query=RootQuery)

app = Flask(__name__)

(translator, opt) = apprun.initialise(app)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

# Optional, for adding batch query support (used in Apollo-Client)
#app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view('graphql', schema=schema, batch=True))

