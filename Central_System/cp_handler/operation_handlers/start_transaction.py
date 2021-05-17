

async def handle_start_transaction():
    pass

"""
# concurrent_tx: Identifier is already involved in another transaction and multiple transactions
# are not allowed. (Only relevant for a StartTransaction.req.)
if _id_tag.in_use == True:
    _id_tag_info.status = AuthorizationStatus.concurrent_tx

# create new transaction or check id_Tag of ongoing transaction
else:
"""