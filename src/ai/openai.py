from abc import ABC, abstractmethod
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from pydantic import HttpUrl
from typing import Optional
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from .prompt.summary import DEFAULT_MAP_PROMPT_TEMPLATE_STRING, DEFAULT_REDUCE_PROMPT_TEMPLATE_STRING
from ai.base_llm import BaseLLM
from base import AIService
from models import Config


class OpenAIService(BaseLLM, AIService):
    def __init__(self, config: Config):
        super().__init__(config)

    def summary_mp(self, doc: str, api_token: str | None, proxy_server: Optional[HttpUrl]) -> str:
        if proxy_server is None:
            llm = OpenAI(temperature=0, openai_api_key=api_token,
                         client={})
        else:
            llm = OpenAI(temperature=0, openai_api_key=api_token,
                         openai_proxy=proxy_server, client={})

        MAP_PROMPT = PromptTemplate(
            input_variables=["text"], template=DEFAULT_MAP_PROMPT_TEMPLATE_STRING)

        REDUCE_PROMPT = PromptTemplate(
            input_variables=["text", ], template=DEFAULT_REDUCE_PROMPT_TEMPLATE_STRING)

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

    def summary_naive(self, doc: str, prompt_template: str | None) -> str:
        llm = OpenAI(temperature=0, openai_api_key=self.api_token,
                     openai_proxy=self.base_url, client={})

        MAP_PROMPT = PromptTemplate(
            input_variables=["text"], template=prompt_template if prompt_template else DEFAULT_MAP_PROMPT_TEMPLATE_STRING)

        chain = load_summarize_chain(llm, chain_type="stuff")
        chain.run()

        REDUCE_PROMPT = PromptTemplate(
            input_variables=["text", ], template=DEFAULT_REDUCE_PROMPT_TEMPLATE_STRING)

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

    def summary(self, doc: str, prompt_template: str | None) -> str:
        return self.summary_naive(doc, prompt_template)
