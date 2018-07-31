import graphene

class WikiSqlTable(graphene.ObjectType):
    id = graphene.ID()
    header = graphene.List(graphene.String)
    rows = graphene.List(graphene.List(graphene.String))

    def resolve_rows(self, info):
        return [['1','a','a'],['2','b','b']]

class RootQuery(graphene.ObjectType):
    tables = graphene.List(WikiSqlTable)

    def resolve_tables(self,info):
        return []
