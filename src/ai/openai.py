import logging
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.callbacks import get_openai_callback
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

    @classmethod
    def get_summary_model(cls, char_num: int) -> ModelType:
        if char_num <= 3500:
            return ModelType.openai_gpt35
        else:
            return ModelType.openai_gpt35_16

    def summary_by_chat(self, llm_input: ChatSummaryInput, llm_config: LLMConfig) -> LLMResult:
        model = self.get_summary_model(llm_input.count_chars())
        logging.debug('char_count: {}, summary model: {}'.format(
            llm_input.count_chars(), model))
        llm = ChatOpenAI(
            temperature=llm_config.temperature,
            openai_api_key=llm_config.api_token if llm_config.api_token else self.api_token,
            openai_api_base=llm_config.base_url if llm_config.base_url else self.base_url, client={},
            max_tokens=llm_config.max_tokens,
            max_retries=llm_config.max_retries if llm_config.max_retries else 3,
            model_name=llm_config.model if llm_config.model else model,
        )
        system_message = SystemMessagePromptTemplate.from_template(
            llm_input.system)
        example_messages = []
        if llm_input.examples:
            for example in llm_input.examples:
                example_messages.append(
                    AIMessagePromptTemplate.from_template(example.ai))
                example_messages.append(
                    HumanMessagePromptTemplate.from_template(example.human))
        human_message_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_message_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message] + example_messages + [human_message_prompt])

        chain = LLMChain(llm=llm, prompt=chat_prompt)
        with get_openai_callback() as cb:
            try:
                result = chain.run([llm_input.content])
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
