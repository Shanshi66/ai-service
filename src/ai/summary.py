from abc import ABC, abstractmethod
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from pydantic import HttpUrl
from typing import Optional
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from .prompt.summary import MAP_PROMPT_TEMPLATE_STRING, REDUCE_PROMPT_TEMPLATE_STRING


class SummaryService(ABC):
    @classmethod
    @abstractmethod
    def summary(cls, doc: str, api_token: str, proxy_server: Optional[HttpUrl]) -> str:
        pass


class LangChainSummaryService(SummaryService):
    @classmethod
    def summary(cls, doc: str, api_token: str, proxy_server: Optional[HttpUrl]) -> str:
        if proxy_server is None:
            llm = OpenAI(temperature=0, openai_api_key=api_token,
                         client={})
        else:
            llm = OpenAI(temperature=0, openai_api_key=api_token,
                         openai_proxy=proxy_server, client={})

        MAP_PROMPT = PromptTemplate(
            input_variables=["text"], template=MAP_PROMPT_TEMPLATE_STRING)

        REDUCE_PROMPT = PromptTemplate(
            input_variables=["text", ], template=REDUCE_PROMPT_TEMPLATE_STRING)

        map_llm_chain = LLMChain(llm=llm, prompt=MAP_PROMPT)
        reduce_llm_chain = LLMChain(llm=llm, prompt=REDUCE_PROMPT)

        generative_result_reduce_chain = StuffDocumentsChain(
            llm_chain=reduce_llm_chain,
            document_variable_name="text",
        )

        combine_documents = MapReduceDocumentsChain(
            llm_chain=map_llm_chain,
            combine_document_chain=generative_result_reduce_chain,
            document_variable_name="text",
        )

        map_reduce = MapReduceChain(
            combine_documents_chain=combine_documents,
            text_splitter=TokenTextSplitter(chunk_size=3000)
        )

        return map_reduce.run(doc)
