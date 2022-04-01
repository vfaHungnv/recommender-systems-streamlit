import numpy as np
import pandas as pd
import streamlit as st
import math
from utils import Load_Object, gensim_recommend_handle
from widgets import show_product_info

PRODUCT_NUMBER = 4
df_product = pd.read_csv('./dataset/product_v2.csv')

if 'PRODUCT_ID' not in st.session_state:
	st.session_state.PRODUCT_ID = None
if 'LIST_FEATURE' not in st.session_state:
	st.session_state.LIST_FEATURE = 0
# if 'CURRENT_GROUP' not in st.session_state:
#     st.session_state.CURRENT_GROUP = None

with open('./resources/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

menu = ['GIỚI THIỆU', 'DANH SÁCH SẢN PHẨM', 'TÌM KIẾM SẢN PHẨM', 'GỢI Ý SẢN PHẨM CHO KHÁCH HÀNG', 'CHI TIẾT SẢN PHẨM']
index_of_menu = list(range(len(menu)))
choice = st.sidebar.selectbox('CHỨC NĂNG', index_of_menu, format_func=lambda x: menu[x], key='LIST_FEATURE')

def didSelectedProduct(id=0):
    if id == 0: 
        st.session_state.LIST_FEATURE = choice
    else:
        st.session_state.PRODUCT_ID = id
        st.button('Back', on_click=didSelectedProduct, args=(0,))
        st.session_state.LIST_FEATURE = 4

st.header('HỆ THỐNG ĐỀ XUẤT SẢN PHẨM') 

if choice == 0:
    st.subheader('Giới thiệu')
    st.markdown('''
        - Tiki là một hệ sinh thái thương mại “all in one”, trong đó có tiki.vn, là website thương mại điện tử đứng top 2 của Việt Nam, top 6 khu vực Đông Nam Á.
        - Trên trang này đã triển khai nhiều tiện ích hỗ trợ nâng cao trải nghiệm người dùng và họ muốn xây dựng nhiều tiện ích hơn nữa.
        - Giả sử công ty này chưa triển khai Recommender System và bạn được yêu cầu triển khai hệ thống này, bạn sẽ làm gì?

        **Mục tiêu/ vấn đề:** Xây dựng Recommendation System cho một hoặc một số nhóm hàng hóa trên tiki.vn giúp đề xuất và gợi ý cho người dùng/ khách hàng. => Xây dựng các mô hình đề xuất:
        - Content-based filtering
        - Collaborative filtering
    ''')
    st.image('./resources/img.jpg')
    st.write(' ```(Nhóm thực hiện: Lưu Trung Tín, Nguyễn Văn Hùng)```')

elif choice == 1:
    st.subheader('Danh sách sản phẩm')
    # sb_group = st.selectbox('Chọn loại sản phẩm: ',df_product['group'].unique(), key='CURRENT_GROUP')
    sb_group = st.selectbox('Chọn loại sản phẩm: ',df_product['group'].unique())

    df = df_product[df_product['group']==sb_group]
    j = int(3 if len(df)>=12 else math.ceil(len(df)/4))
    for i in range(0, j):
        product_cols = st.columns(PRODUCT_NUMBER)
        df_new = df.iloc[i*PRODUCT_NUMBER:(1+i)*PRODUCT_NUMBER]
        show_product_info(product_cols, df_new, didSelectedProduct)

elif choice == 2:
    st.subheader('Tìm kiếm sản phẩm')
    flag = False
    content = st.text_area(label='Tìm sản phẩm, danh mục, mô tả hay thương hiệu mong muốn ...')
    if content != '':
        flag = True
    if flag:
        # TODO: recommendation Gensim
        dictionary = Load_Object('./dataset/dictionary_gensim.pkl')
        tfidf = Load_Object('./dataset/ftidf_gensim.pkl')
        index = Load_Object('./dataset/index_gensim.pkl')

        df_gensim = gensim_recommend_handle(content, df_product, dictionary, tfidf, index)
        df_new_1 = df_product[df_product['item_id'].isin(df_gensim['item_id'].to_list())]
        for i in range(0, 2):
            product_cols = st.columns(PRODUCT_NUMBER)
            df_new = df_new_1.iloc[i*PRODUCT_NUMBER:(1+i)*PRODUCT_NUMBER]
            show_product_info(product_cols, df_new, didSelectedProduct)

elif choice == 3:
    st.subheader('Gợi ý sản phẩm cho khách hàng')
    df_review = pd.read_csv('./dataset/surprise_recommend_v1.csv')
    name_list = list(df_review['name'])
    index_of_name_list = list(range(len(name_list)))
    sb_customer = st.selectbox('Chọn khách hàng login để được gợi ý sản phẩm: ', index_of_name_list, format_func=lambda x: name_list[x], key='CUSTOMER_INDEX')
    customer_id = df_review['customer_id'][sb_customer]

    # TODO: recommendation BaselineOnly
    df_surpise = df_review[df_review['customer_id']==customer_id].reset_index()
    item_ids = list(map(int, df_surpise['item_ids'][0].split(', ')))
    df_new_1 = df_product[df_product['item_id'].isin(item_ids)]
    for i in range(0, 2):
        product_cols = st.columns(PRODUCT_NUMBER)
        df_new = df_new_1.iloc[i*PRODUCT_NUMBER:(1+i)*PRODUCT_NUMBER]
        show_product_info(product_cols, df_new, didSelectedProduct)

elif choice == 4:
    st.subheader('Chi tiết sản phẩm:')
    if st.session_state.PRODUCT_ID == None: 
        st.write('Vui lòng chọn sản phẩm từ danh mục trước khi xem chi tiết sản phẩm!!!')
    else:
        df_new = df_product[df_product['item_id']==st.session_state.PRODUCT_ID].reset_index()
        thumbnail_col, name_col = st.columns([4,6])
        with thumbnail_col:
            st.image(df_new['thumbnail_url'][0])
        with name_col:
            content = f'''
                <p style="font-size: 15px; font-weight: 400; color:gray; text-decoration: none; line-height:30px">{df_new["name"][0]}</p>
                <p style="color:red; font-weight: 500; font-size: 20px;">{df_new["price"][0]:,} ₫</p>
                <p style="font-size: 15px; font-weight: 400; color:gray; text-decoration: none; line-height:30px">Rating: {df_new["rating"][0]} / 5</p>
                <p style="font-size: 15px; font-weight: 400; color:gray; text-decoration: none; line-height:30px">Thương hiệu: { '' if pd.isna(df_new["brand"][0]) else df_new["brand"][0] }</p>
            '''
            st.markdown(content, unsafe_allow_html=True)
        with st.expander('Mô tả sản phẩm'):
            st.markdown(df_new['description_html'][0], unsafe_allow_html=True)

        # TODO: recommendation Cosine
        st.subheader('Gợi ý sản phẩm tương tự:')
        df_cb = pd.read_csv('./dataset/CB_1_new.csv')
        df_cb = df_cb[df_cb['product_id']==st.session_state.PRODUCT_ID]
        df_new = df_product[df_product['item_id'].isin(df_cb['rcmd_product_id'].to_list())]
        product_cols = st.columns(PRODUCT_NUMBER)
        show_product_info(product_cols, df_new, didSelectedProduct)