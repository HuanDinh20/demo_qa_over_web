from openai import OpenAI

from routers import get_categories
from intent_detect import get_user_intent, get_text_from_intent
from query_engine import get_multistep_query_engine
from vector_store import get_vector_store
from template import openai_api_key


if __name__ == '__main__':
    url_home = ["https://cellphones.com.vn/", "https://www.thegioididong.com/"]
    client = OpenAI(api_key=openai_api_key)
    user_queries = ["iphone 15 giá bao nhiêu", "iphone 15có ưu đãi hay lưu ý gì không?"
                  "giá của samsung galaxy s27 là bao nhiêu?",
                  "so sánh giữa iphone 14 và iphone 15"]

    category_2_link = get_categories(url_home[0])
    intent_list = get_user_intent(user_query=user_queries[0],
                                  category_to_link=category_2_link, client=client)
    production_descriptions = get_text_from_intent(intent_list, client)

    index = get_vector_store(intent_list, production_descriptions)
    query_engine = get_multistep_query_engine(index)
    result = query_engine.query(user_queries[0])
    print(result.response)

