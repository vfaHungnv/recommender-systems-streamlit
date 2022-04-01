import streamlit as st
import random

def show_product_info(col, df, didSelectedProduct):
    for c, i, n, p, u, up in zip(col, df['item_id'], df['name'], df['price'], df['thumbnail_url'], df['url_path']):
        with c:
            st.image(u)
            price_vs_name = f'''
                <p style="text-align:center; color:red; font-weight: 500;">{p:,} ₫</p>
                <a style="font-size: 13px; font-weight: 400; color:gray; text-decoration: none; line-height:30px" href="{up}">{n}</a>
            '''
            st.markdown(price_vs_name, unsafe_allow_html=True)
            st.button('xem chi tiết', key=i+random.randint(1, 1000), on_click=didSelectedProduct, args=(i,))