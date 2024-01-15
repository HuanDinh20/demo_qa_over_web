import json
import requests

from bs4 import BeautifulSoup
from openai import OpenAI
from template import FAKE_HEADERS


def get_user_intent(user_query, category_to_link, client):
    intent_extractor = client.chat.completions.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system",
             "content": f"Read the dictionary mapping from category to url: {category_to_link}"},
            {"role": "user", "content": f"Extract all categories and all related information in the question."
                                        f"Return it as list of json format. Each document contains three "
                                        f"at most 3 keys: category, url, related_info"
                                        f"question: `Tôi muốn mua một chiếc iphone màu hồng, và Máy lọc không khí' "
                                        """[{
                                                        "category": "IPhone 15",
                                                        "url": "https://cellphones.com.vn/mobile/apple/iphone-15.html",
                                                        "related_info": "Pink"
                                                      },
                                                      {
                                                        "category": "Máy lọc không khí",
                                                        "url": "https://cellphones.com.vn/nha-thong-minh/may-loc-khong-khi.html", 
                                                        "related_info": "None"
                                                      }]
                                        """
                                        f"question: {user_query}. Extract all categories and all related information "
                                        f"in the question."
                                        f"Return it as list of json format, witch each document contrains three 3 keys "
                                        f"category, url, related_infor"}
        ], )
    response_message = intent_extractor.choices[0].message.content
    # response_message_dict = json.loads(response_message)
    return response_message


def get_text_from_intent(intent_list, client, headers=FAKE_HEADERS):
    product_infos = []
    try:
        intent_list = json.loads(intent_list)
    except:
        intent_list = intent_list
    for intent in intent_list:
        intent_url = intent.get("url")
        intent_request_data = requests.get(intent_url, headers=headers)
        soup = BeautifulSoup(intent_request_data.text, 'html.parser')
        product_links = [link for link in soup.find_all('a', href=True)]
        list_product_sublinks = [(link, link.get("href"), link.text) for link in product_links if link.h3 is not None]
        if len(list_product_sublinks) == 0:
            product_info = soup.text
            product_infos.append(product_info)
        else:
            for html, href, text in list_product_sublinks[:1]:

                infor_extractor = client.chat.completions.create(
                    model="gpt-3.5-turbo-0301",
                    messages=[
                        {"role": "system",
                         "content": f"Read the HTML below, follow instructions and return json format"},
                        {"role": "user", "content": f"Extract the information from the HTML"
    """(<a class="product__link button__link" href="https://cellphones.com.vn/iphone-15-pro-max.html" rel=""><div class="product__image"><img alt="iPhone 15 Pro Max 256GB | Chính hãng VN/A" class="product__img" height="358" loading="lazy" src="https://cdn2.cellphones.com.vn/358x358,webp,q10/media/wysiwyg/placehoder.png" width="358"/></div> <div class="product__name"><h3>iPhone 15 Pro Max 256GB | Chính hãng VN/A</h3></div> <div class="product__badge"></div> <!-- --> <div class="block-box-price"><!-- --> <!-- --> <span class="title-price" style="display:none;">
                 :
               </span> <div class="box-info__box-price"><p class="product__price--show">
           32.690.000₫
         </p> <p class="product__price--through">
             34.990.000₫
           </p> <div class="product__price--percent"><p class="product__price--percent-detail">
               Giảm 7%
             </p></div></div></div> <!-- --> <!-- --> <div class="block-trade-price">Giá lên đời: <div class="block-box-price"><!-- --> <!-- --> <span class="title-price" style="display:none;">
                 :
               </span> <div class="box-info__box-price"><p class="product__price--show">
           30.690.000₫
         </p> <!-- --></div></div></div> <div class="product__promotions"><div class="product__promotions"><div class="promotion"><p class="coupon-price">
                   Không phí chuyển đổi khi trả góp 0% qua thẻ tín dụng kỳ hạn 3-6 tháng
                 </p></div></div></div> <div class="product__promotions" style="display:none;"><div class="promotion"><p class="gift-cont"></p></div></div> <!-- --></a>,
     'https://cellphones.com.vn/iphone-15-pro-max.html',
     ' iPhone 15 Pro Max 256GB | Chính hãng VN/A     \n            :\n           \n      32.690.000₫\n     \n        34.990.000₫\n       \n          Giảm\xa07%\n           Giá lên đời:\xa0  \n            :\n           \n      30.690.000₫\n      \n              Không phí chuyển đổi khi trả góp 0% qua thẻ tín dụng kỳ hạn 3-6 tháng\n              ')
    
    """
                                                    """Thông tin về iphone iPhone 15 Pro Max 256GB
                                                    "Tên sản phẩm": "iPhone 15 Pro Max 256GB", 
                                                    "Giá": "30.690.000₫", 
                                                    "Giá lên đời":  32.690.000₫, 
                                                    "Lưu ý": "Không phí chuyển đổi khi trả góp 0% qua thẻ tín dụng kỳ hạn 3-6 tháng", 
                                                    "đường dẫn chi tiết sản phẩm": "https://cellphones.com.vn/iphone-15-pro-max.html"
                                                    
                                                    }
                                                    """
                                                    f"question: Extract the information from the HTML"
                                                    f" {html}"}
                    ], )
            response_message = infor_extractor.choices[0].message.content
            product_infos.append(response_message)

    return product_infos

