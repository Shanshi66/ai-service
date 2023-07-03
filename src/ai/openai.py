import logging
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.callbacks import get_openai_callback
from langchain.docstore.document import Document
from .prompt.summary import DEFAULT_MAP_PROMPT_TEMPLATE_STRING
from ai.base_llm import BaseLLM
from base import AIService, CustomException, ErrorType
from models import Config, LLMResult, LLMConfig, LLMInput, ModelType


class OpenAIService(BaseLLM, AIService):
    def __init__(self, config: Config, llm_config: LLMConfig):
        super().__init__(config)
        self.model = llm_config.model if llm_config.model else ModelType.openai_default()
        self.llm = OpenAI(
            temperature=llm_config.temperature,
            openai_api_key=llm_config.api_token if llm_config.api_token else self.api_token,
            openai_api_base=llm_config.base_url if llm_config.base_url else self.base_url, client={})

    def summary_naive(self, llm_input) -> LLMResult | None:
        prompt = PromptTemplate(
            input_variables=["text"], template=llm_input.prompt_template if llm_input.prompt_template else DEFAULT_MAP_PROMPT_TEMPLATE_STRING)

        chain = load_summarize_chain(
            self.llm, chain_type="stuff", prompt=prompt)
        doc = Document(page_content=llm_input.contents[0].content)
        with get_openai_callback() as cb:
            try:
                result = chain.run([doc])
            except Exception as e:
                logging.error('summary naive error: {}'.format(e))
                raise CustomException(
                    "Openai Network Error", ErrorType.LLM_NETWORK_ERROR)
            total_tokens = cb.total_tokens

        return LLMResult(
            result=result,
            token_usage=total_tokens,
            model=self.model
        )

    def summary(self, llm_input: LLMInput) -> LLMResult | None:
        if len(llm_input.contents) > 1:
            raise CustomException(
                "Currently, this service not support multi contents", ErrorType.NOT_SUPPORT)
        return self.summary_naive(llm_input)
