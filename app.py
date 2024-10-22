from pickletools import read_stringnl_noescape
from flask import Flask, render_template,request
import pickle
import numpy as np
app=Flask(__name__)

model_df=pickle.load(open('model\popular_groc.pkl','rb'))
model_pt=pickle.load(open('model\groc_pt.pkl','rb'))
model_groc=pickle.load(open('model\groc.pkl','rb'))
model_scores=pickle.load(open('model\similarity_scores.pkl','rb'))


@app.route('/')
def index():
    return render_template('index.html',
                           groc_name=list(model_df['Item'].values),                           
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    x=np.where(model_pt.index==model_groc)[0][0]
    print(x)
    similar_items=sorted(list(enumerate(model_scores[x])),key=lambda x:x[1],reverse=True)[1:6]
    
    data=[]
    for i in similar_items:
        item=[]
        temp_df=model_groc[model_groc['Item']==model_pt.index[i[0]]]   
        #print(temp_df.drop_duplicates('Book-Title')['Book-Author'])
        item.append(list(temp_df.drop_duplicates('Item')['Item'].values))

        data.append(item)
        
    print(data)
    return render_template('recommend.html',data=data)
    
    
if __name__ == '__main__':
    app.run(debug=True)