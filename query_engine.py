from llama_index.llms import OpenAI
from llama_index.service_context import ServiceContext
from llama_index.query_engine.multistep_query_engine import StepDecomposeQueryTransform, MultiStepQueryEngine

from template import openai_api_key


def get_multistep_query_engine(index, model="gpt-4"):
    model = "gpt-3.5-turbo-0301"
    llm = OpenAI(temperature=0, model=model, api_key=openai_api_key)
    service_context_gpt4 = ServiceContext.from_defaults(llm=llm)
    index_summary = "Used to answer questions about the a product"
    step_decompose_transform = StepDecomposeQueryTransform(llm=llm, verbose=True)
    query_engine = index.as_query_engine(service_context=service_context_gpt4)
    query_engine = MultiStepQueryEngine(
        query_engine=query_engine,
        query_transform=step_decompose_transform,
        index_summary=index_summary,
    )
    return query_engine

