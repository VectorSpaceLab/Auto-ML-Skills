# Retrieval And RAG Workflows

## Tiny No-Key Index

```python
docs = [Document(page_content="LangChain uses LCEL.", metadata={"id": "lc"})]
embedding = DeterministicFakeEmbedding(size=16)
store = InMemoryVectorStore(embedding=embedding)
store.add_documents(docs)
hits = store.similarity_search("LCEL", k=1)
```

## Split Documents

```python
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
```

## Retriever As Runnable

```python
retriever = store.as_retriever(search_kwargs={"k": 3})
docs = retriever.invoke("question")
```

## RAG LCEL Shape

```python
chain = {
    "context": retriever,
    "question": RunnablePassthrough(),
} | prompt | model | parser
```

If the prompt expects a string context, add a formatting lambda that joins retrieved documents.

## Production Vector Stores

For persistent stores, install the dedicated integration package and record collection/index name, embedding model, dimension, distance metric, persistence path or endpoint, and cleanup policy.
