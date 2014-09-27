from arangodb.api import Document


def create_document_from_result_dict(result_dict, api):
    collection_name = result_dict['_id'].split('/')[0]

    doc = Document(
        id=result_dict['_id'],
        key=result_dict['_key'],
        collection=collection_name,
        api=api,
    )

    doc.is_loaded = True

    del result_dict['_id']
    del result_dict['_key']
    del result_dict['_rev']

    for result_key in result_dict:
        result_value = result_dict[result_key]

        doc.set(key=result_key, value=result_value)

    return doc