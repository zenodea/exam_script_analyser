import requests
import bs4
from haystack.document_stores import FAISSDocumentStore
from haystack.utils import clean_wiki_text, convert_files_to_docs, fetch_archive_from_http, print_answers
from haystack.nodes import FARMReader, TransformersReader
from haystack.nodes import DensePassageRetriever
from haystack.pipelines import ExtractiveQAPipeline
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def readerCreation():
    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2",
                        use_gpu=True)
    return reader


def retreiveContext(queary, pipe):
    prediction = pipe.run(query=queary, params={"Retriever": {"top_k": 15}, "Reader": {"top_k": 5}})
    print_answers(prediction, details="minimum")


def retriveContext_ObtainKeywords(queary, pipe):
    prediction = pipe.run(query=queary, params={"Retriever": {"top_k": 15}, "Reader": {"top_k": 5}})


def retrieverCreation(document_store):
    retriever = DensePassageRetriever(
        document_store=document_store,
        query_embedding_model="vblagoje/dpr-question_encoder-single-lfqa-wiki",
        passage_embedding_model="vblagoje/dpr-ctx_encoder-single-lfqa-wiki",
    )
    document_store.update_embeddings(retriever)
    return retriever


def document_store_Creation(doc_dir):
    document_store = FAISSDocumentStore(embedding_dim=128, faiss_index_factory_str="Flat")
    # Let's first get some files that we want to use

    # Convert files to dicts
    docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text,
                                 split_paragraphs=True)

    print(docs[1])
    # Now, let's write the dicts containing documents to our DB.
    document_store.write_documents(docs)
    return document_store


def wikipediaRetrieval(wiki_page):
    for section in wiki_page:
        try:
            res = requests.get(f'https://en.wikipedia.org/wiki/{section}')
            res.raise_for_status()
            wiki = bs4.BeautifulSoup(res.text, "html.parser")
        except:
            pass
        # open a file named as your wiki page in write mode
        with open("data/" + section + ".txt", "w", encoding="utf-8") as f:
            for i in wiki.select('p'):
                # write each paragraph to the file
                f.write(i.getText())


class informationRetrieval:
    def __init__(self, listofkeywords):
        wikipediaRetrieval(listofkeywords)
        self.document_store = None
        self.retriever = None
        self.reader = None
        self.pipe = None

    def startDatabaseCreation(self, doc_dir):
        self.document_store = document_store_Creation(doc_dir)
        self.retriever = retrieverCreation(self.document_store)
        self.reader = readerCreation()
        self.pipe = ExtractiveQAPipeline(self.reader, self.retriever)

    def getAnswer(self, queary):
        retreiveContext(queary, self.pipe)
