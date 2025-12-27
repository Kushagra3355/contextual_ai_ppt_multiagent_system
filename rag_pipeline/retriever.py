def get_retriever(vectorstore, k=5):
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )


# def retrieve_with_citations(query, retriever):
#     docs = retriever.get_relevant_documents(query)

#     results = []
#     for i, doc in enumerate(docs, start=1):
#         citation = {
#             "id": i,
#             "text": doc.page_content,
#             "source": doc.metadata.get("filename", "unknown"),
#             "page": doc.metadata.get("page", "N/A"),
#         }
#         results.append(citation)

#     return results
