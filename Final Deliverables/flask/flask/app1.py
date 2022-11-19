import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests
import inputScript
import requests
import json


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Y8QDxTOovky3hPfWPM819qL_IFHlNCIt-HMcN_Ri0HcW"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



app = Flask(__name__)


#Redirects to the page to give the user input URL.
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict')
def predict():
    return render_template('main.html')


ans = ""   
bns = ""   
@app.route('/predict2', methods=['POST'])
def y_predict():
    url = request.form['URL']
    checkpredict = inputScript.main(url)
    payload_scoring = {"input_data": [{"field": [["having_IPhaving_IP_Address","URLURL_Length","Shortining_Service","having_At_Symbol","double_slash_redirecting",
        "Prefix_Suffix","having_Sub_Domain","SSLfinal_State","Domain_registeration_length","Favicon","port",
        "HTTPS_token","Request_URL","URL_of_Anchor","Links_in_tags","SFH","Submitting_to_email",
        "Abnormal_URL","Redirect","on_mouseover","RightClick",
        "popUpWidnow","Iframe","age_of_domain","DNSRecord","web_traffic	Page_Rank","Google_Index","Links_pointing_to_page","Statistical_report"
    ]], "values": checkpredict }]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/589c27c9-fc88-40fd-b7d3-8a015820e75d/predictions?version=2022-11-18', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    
    pred = response_scoring.json()
    
    prediction = pred['predictions'][0]['values'][0][0]
    
    if len(url)<1:
        utext = "Enter URL"
        return render_template('main.html',no_url=utext)
    elif prediction==1:
        utext="This is a legitimate website"
        return render_template('main.html', bns=utext)
    else:
        utext="This site is unsafe"
        return render_template('main.html', ans=utext)
    


 

if __name__=='__main__':
    app.run( host='0.0.0.0',debug=False)