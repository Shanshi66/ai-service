import logging
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.callbacks import get_openai_callback
from langchain.docstore.document import Document
from .summary import DEFAULT_MAP_PROMPT_TEMPLATE_STRING
from ai.base_llm import BaseLLM
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from base import AIService, CustomException, ErrorType
from models import Config, LLMResult, LLMConfig, LLMInput, ModelType, ChatSummaryInput, Usage, LLMType


class OpenAIService(BaseLLM, AIService):
    def __init__(self, config: Config):
        super().__init__(config)

    # use text model, too expensive
    # def summary_naive(self, llm_input, llm_config) -> LLMResult | None:
    #     llm = OpenAI(
    #         temperature=llm_config.temperature,
    #         openai_api_key=llm_config.api_token if llm_config.api_token else self.api_token,
    #         openai_api_base=llm_config.base_url if llm_config.base_url else self.base_url, client={},
    #         max_tokens=llm_config.max_tokens,
    #         max_retries=llm_config.max_retries,
    #         model_name=llm_config.model if llm_config.model else ModelType.openai_chat_default(),
    #     )
    #     prompt = PromptTemplate(
    #         input_variables=["text"], template=llm_input.prompt_template if llm_input.prompt_template else DEFAULT_MAP_PROMPT_TEMPLATE_STRING)

    #     chain = load_summarize_chain(
    #         llm, chain_type="stuff", prompt=prompt)
    #     doc = Document(page_content=llm_input.contents[0].content)
    #     with get_openai_callback() as cb:
    #         try:
    #             result = chain.run([doc])
    #         except Exception as e:
    #             logging.error('summary naive error: {}'.format(e))
    #             raise CustomException(
    #                 "Openai Network Error", ErrorType.LLM_NETWORK_ERROR)
    #         total_tokens = cb.total_tokens

    #     return LLMResult(
    #         result=result,
    #         token_usage=total_tokens,
    #         model=llm.model_name
    #         content_key=llm_input.contents[0].content_key
    #     )

    def summary_by_chat(self, llm_input: ChatSummaryInput, llm_config: LLMConfig) -> LLMResult:
        llm = ChatOpenAI(
            temperature=llm_config.temperature,
            openai_api_key=llm_config.api_token if llm_config.api_token else self.api_token,
            openai_api_base=llm_config.base_url if llm_config.base_url else self.base_url, client={},
            max_tokens=llm_config.max_tokens,
            max_retries=llm_config.max_retries,
            model_name=llm_config.model if llm_config.model else ModelType.openai_chat_default(),
        )
        system_message = SystemMessagePromptTemplate.from_template(
            llm_input.system_message)
        example_messages = []
        if llm_input.example_messages:
            for example in llm_input.example_messages:
                example_messages.append(
                    AIMessagePromptTemplate.from_template(example.ai_message))
                example_messages.append(
                    HumanMessagePromptTemplate.from_template(example.human_message))
        human_message_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_message_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message] + example_messages + [human_message_prompt])

        chain = LLMChain(llm=llm, prompt=chat_prompt)
        with get_openai_callback() as cb:
            try:
                result = chain.run([llm_input.content.content])
            except Exception as e:
                logging.error('summary naive error: {}'.format(e))
                raise CustomException(
                    "Openai Network Error", ErrorType.LLM_NETWORK_ERROR)
            usage = Usage(
                total_tokens=cb.total_tokens,
                total_cost=cb.total_cost,
                prompt_tokens=cb.prompt_tokens,
                completion_tokens=cb.completion_tokens,
            )
        return LLMResult(
            content_key=llm_input.content.content_key,
            result=result,
            usage=usage,
            model=llm.model_name,
            llm_type=LLMType.openai
        )

    def summary(self, llm_input: LLMInput, llm_config: LLMConfig) -> LLMResult:
        if isinstance(llm_input, ChatSummaryInput):
            return self.summary_by_chat(llm_input, llm_config)
        raise CustomException(
            "Currently not support other summary method except chat summary", ErrorType.NOT_SUPPORT)
