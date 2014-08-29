from couchdb.design import ViewDefinition

"""The token from their ids"""
tokens = ViewDefinition('usertokens', 'by_user_id', """
function(doc){
  if(doc.type == 'usertoken'){
      emit(doc.user_id, doc);
  }
}
""")

l = locals().values()
docs = [v for v in l if isinstance(v, ViewDefinition)]
