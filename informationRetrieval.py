class informationRetrieval:
    def __init__(self, listofkeywords, doc_dir):
        self.wikipediaRetrieval(listofkeywords)
        self.document_store = self.document_store_Creation(doc_dir)
        self.retriever = retrieverCreation(self.document_store)
        self.reader = readerCreation()
        self.pipe = ExtractiveQAPipeline(self.reader, self.retriever)

    def wikipediaRetrieval(self, wiki_page):
        for section in wiki_page:
            res = requests.get(f'https://en.wikipedia.org/wiki/{section}')
            res.raise_for_status()
            wiki = bs4.BeautifulSoup(res.text, "html.parser")

            # open a file named as your wiki page in write mode
            with open("data/" + section + ".txt", "w", encoding="utf-8") as f:
                for i in wiki.select('p'):
                    # write each paragraph to the file
                    f.write(i.getText())


    def document_store_Creation(self, doc_dir):
        document_store = FAISSDocumentStore(faiss_index_factory_str="Flat")
        # Let's first get some files that we want to use

        # Convert files to dicts
        docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text,
                                     split_paragraphs=True)

        # Now, let's write the dicts containing documents to our DB.
        document_store.write_documents(docs)
        return document_store

    def retrieverCreation(document_store):
        retriever = DensePassageRetriever(
            document_store=document_store,
            query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
            passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
            max_seq_len_query=64,
            max_seq_len_passage=256,
            batch_size=16,
            use_gpu=True,
            embed_title=True,
            use_fast_tokenizers=True,
        )
        document_store.update_embeddings(retriever)
        return retriever

    def readerCreation(self):
        reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2",
                            use_gpu=True)
        return reader


    def retreiveContext(self, queary, pipe):
        prediction = pipe.run(query=queary, params={"Retriever": {"top_k": 15}, "Reader": {"top_k": 1}})
        print_answers(prediction, details="minimum")