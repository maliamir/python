[Demo](https://youtu.be/LYADv5pxXkg)

# Introduction
This is a simple flask (a python based micro web-framework) web-application which exposes a POST action against an end-point "/converse" to evaluate a text response against the provided sentence in a JSON format.

- This REST end-point is essentially an AI Conversational which Bot classifies user input to recognize intent which is resolved by Machine Learning implemented with Keras having TensorFlow as backend.<br/><br/>
  Keras Deep Learning Library is used to build a classification model.<br/>Keras runs training on top of TensorFlow backend.<br/><br/>
  Lancaster Stemming Library (from nltk - Natural Language Tool-Kit) is used to collapse distinct word forms.<br/><br/>
  Chatbot Intents and Patterns to learn are defined in a plain JSON file. There is no need to have a huge vocabulary since it is a POC and very domain-specific. 
  conversations-model.py builds Classification Model using the small vocabulary defined in "intents.json".<br/>
  
- Conversational Context is maintained in Slack Bot backed by a separate Spring Boot Application.


# Install Python 3.7+
1. Download & install 3.7+ Python from:
   https://www.python.org/downloads/

2. Install pip as:<br/>
   Download: https://bootstrap.pypa.io/get-pip.py then
   /usr/local/bin/python3.7 get-pip.py

3. Set Proxy (if necessary):<br/>
   export https_proxy="http://www-proxy.host.name.com:80"

4. Install Flask:<br/>
   /usr/local/bin/pip3.7 install bumpy, pandas, ssl, flask, nltk

5. Install Tensorflow & Keras:<br/>
   /usr/local/bin/pip3.7 install tensorflow==1.14<br/>
   /usr/local/bin/pip3.7 install keras==2.2.5


# Download & install IDE: PyCharm and run web-application
1. Download & install PyCharm from:
   https://www.jetbrains.com/pycharm/download

2. Open this python project in PyCharm /bot and then run "conversations-endpoint.py”

POST is supported against end-point http://localhost:5001/converse 

Sample:<br/>
POST Request Payload:<br/>
{

    "sentence":
    "How are you?"
}

POST Response Payload:<br/>
{

    "intent": "greeting",
    "probability": "0.8266738",
    "response": "Hi there, how can I help?"
}
