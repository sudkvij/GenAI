# -*- coding: utf-8 -*-
"""Langchain_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Pqfy3-aa0DW90k4vGSkQJ3rd9xEphGYK

LLM Chain
"""

#from langchain_openai import ChatOpenAI
#lim = ChatOpenAI(openai_api_key="")
from langchain_community.llms import Ollama
llm = Ollama(model="llama2")

llm.invoke("how can langsmith help with testing?")

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

chain = prompt | llm

chain.invoke({"input": "how can langsmith help with testing?"})

from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

chain.invoke({"input": "how can langsmith help with testing?"})

"""Retrieval Chain"""

from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()

from langchain_community.embeddings import OllamaEmbeddings
embeddings = OllamaEmbeddings()

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

from langchain.chains.combine_documents import create_stuff_documents_chain
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
<context>
{context}
</context>
Question: {input}""")
document_chain = create_stuff_documents_chain(llm, prompt)

from langchain_core.documents import Document
document_chain.invoke({
    "input": "how can langsmith help with testing?",
    "context": [Document(page_content="langsmith can let you visualize test results")]
})

from langchain.chains import create_retrieval_chain
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "how can langsmith help with testing?"})
print(response["answer"])

# LangSmith offers several features that can help with testing:...

"""Conversation Retrieval chain"""

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

# First we need a prompt that we can pass into an LLM to generate this search query

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

from langchain_core.messages import HumanMessage, AIMessage

chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
retriever_chain.invoke({
    "chat_history": chat_history,
    "input": "Tell me how"
})