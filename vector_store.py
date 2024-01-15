import json

from llama_index.schema import Document
from llama_index.service_context import ServiceContext
from llama_index.indices import VectorStoreIndex
from llama_index.text_splitter import SentenceSplitter


def get_vector_store(intent_list, product_infos):
    try:
        intent_list = json.loads(intent_list)
    except:
        intent_list = intent_list
    context_document = [Document(text=product_infos, metadata=intent_list)]
    # context_document =
    sentence_spliter = SentenceSplitter(chunk_size=500, chunk_overlap=100)
    sv_context = ServiceContext.from_defaults(text_splitter=sentence_spliter)
    index = VectorStoreIndex.from_documents(
        context_document, service_context=sv_context
    )
    return index
