import pandas as pd
import pickle

def Load_Object(filename):    
    with open(filename, 'rb') as file:
        obj = pickle.load(file)
    return obj

def gensim_recommend_handle(view_product, products, dictionary, tfidf, index):
    # Convert search words int Sparse Vectors
    view_product = view_product.lower().split()
    lst_remove = ['~',':',"'",'+','[','\\','@','^','{','%', 
              '(','-','"','*','|',',','&','<','`','}',
              '.','_','=',']','!','>',';','?','#','$',')',
              '/','•','&','','️',' ',',','.','...','-',':',
              ';','?','%','(',')','+','/','|','g','ml','“',
              '”','…','.....','zezé','rio','de','josé',
              '._giá','[',']','!','#','"','=','*',':)','l']
    tmp = []
    for text in view_product:
        if not text in lst_remove:
            tmp.append(text)
    view_product = tmp
    kw_vector = dictionary.doc2bow(view_product)
    
    # Calculate similarity
    sim = index[tfidf[kw_vector]]
    
    # print result
    lst_id = []
    lst_score = []
    for i in range(len(sim)):
        lst_id.append(i)
        lst_score.append(sim[i])
        
    df_result = pd.DataFrame({
        'id' : lst_id,
        'score' : lst_score
    })
    
    # 8 highest scores
    highest_scores = df_result.sort_values(by='score', ascending=False).head(8).tail(8)
    idToList = list(highest_scores['id'])
    
    products_find = products[products.index.isin(idToList)]
    results = products_find[['item_id', 'name']]
    results = pd.concat([results, highest_scores], axis=1).sort_values(by='score', ascending=False)
    return results