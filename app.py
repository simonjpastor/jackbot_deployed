import json 
import numpy as np
from sklearn.preprocessing import LabelEncoder
#from colorama import Fore, Style, Back
import random
import pickle
import streamlit as st
from streamlit_chat import message
import random
import os
os.environ['KERAS_BACKEND'] = 'tensorflow'
from tensorflow import keras
#from keras import models, preprocessing

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


#Streamlit
icon = [":fr:",":kr:",":crown:","old_key",":computer:",":desktop_computer:",":robot_face:"]
st.set_page_config(
    page_title="Jackbot",
    page_icon=f"{icon[random.randrange(0,7)]}"
)

st.image('images/jackson_logo.png')
st.markdown("<h1 style='text-align: center; color: black;'>Jackbot, The Jackson Chatbot</h1>", unsafe_allow_html=True)

st.markdown("<p style='color: black;'><strong>Disclaimer: This is not an official Jackson resource. Official Jackson resources can be found <a href='https://jackson.yale.edu/'>here</a>.</strong><br> Jackbot is a final project by TJ Han (M.A 22') and Simon Pastor (M.P.P 23') as part of the <em> Introduction to Artificial Intelligence and Its Applications </em> class by the great Casey King!</p>", unsafe_allow_html=True)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

random_number_list = list(range(0, 89, 2))
random.shuffle(random_number_list)

def get_text():
    suggestion = f"""Ask me anything! """
    input_text = st.text_input(suggestion, key="input")
    return input_text

user_input_bool = 1


if user_input_bool != 0:
    user_input = get_text()


#Code
with open("intents.json") as file:
    data = json.load(file)

with open("file.txt", 'r') as f:
    faqs = [line.rstrip('\n') for line in f]

# load trained model
model = keras.models.load_model('chat_model')

# load tokenizer object
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load label encoder object
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# parameters
max_len = 20

def bot(user_input):
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([user_input]),
                                             truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for i in data['intents']:
        if i['tag'] == tag:
            result = np.random.choice(i['responses'])

    return result
        # print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,random.choice(responses))

#Back to Streamlit
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("")
with col2:
    if st.button('Send Message 🚀', key="input1"):
        if "casey" in user_input.lower():
            st.session_state.past.append(str(user_input))
            st.session_state.generated.append(str("Hello Casey, we hope you're well and enjoying your teaching retirement! We just wanted to say thank you so much for this semester, this class was one of our best ever! We feel both very grateful and lucky to have been able to take it. We wish you all the best for all the upcoming projects and look forward to seeing you again very soon !"))
        else:
            output = bot(str(user_input.lower()))
            st.session_state.past.append(str(user_input).capitalize())
            st.session_state.generated.append(str(output).lower())
with col3:
    if st.button('Generate & Ask Random Question 🤔', key="input2"):
        user_input_bool = 0
        random_number = random_number_list[0]
        random_input = faqs[random_number]
        #output = bot(str(random_input.lower()))
        output = faqs[random_number + 1].capitalize()
        random_number_list.pop(0)
        st.session_state.past.append(str(random_input).capitalize())
        st.session_state.generated.append(str(output).lower())
with col4:
    st.write("")

#Casey Exception
if st.session_state['generated']:
    if st.session_state["generated"][-1].startswith("Hello Casey"):
        col5, col6, col7 = st.columns([1,6,1])
        with col5:
            st.write("")

        with col6:
            st.markdown("<h1 style='text-align: center; color: blue;'>THANK YOU CASEY!</h1>", unsafe_allow_html=True)
            st.image("images/class.png", width=500)

        with col7:
            st.write("")

#Display Messages
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
