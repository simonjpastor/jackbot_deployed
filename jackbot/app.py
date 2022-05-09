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

st.image('jackson_logo.png')
st.markdown("<h1 style='text-align: center; color: black;'>Jackbot, The Jackson Chatbot</h1>", unsafe_allow_html=True)

st.markdown("<p style='color: black;'><strong>Disclaimer: This is not an official Jackson resource. Official Jackson resources can be found <a href='https://jackson.yale.edu/'>here</a>.</strong><br> Jackbot is a final project by TJ Han (M.A 22') and Simon Pastor (M.P.P 23') as part of the <em> Introduction to Artificial Intelligence and Its Applications </em> class by the great Casey King!</p>", unsafe_allow_html=True)
#st.markdown("<p style='color: black;'>Jackbot is the result of a final project by TJ Han (M.A 22') and Simon Pastor (M.P.P 23')</p>", unsafe_allow_html=True)

faqs = ["Who are you?",
"I'm Jackbot, your bot assistant. I am happy to talk about Jackson and what makes it great and unique.",
"What are you?",
"I'm Jackbot, an Artificial Intelligent bot. I am happy to talk about Jackson and what makes it great and unique.",
"Who you are?",
"My name is Jackbot created by Simon and TJ. I am happy to talk about Jackson and what makes it great and unique.",
"Where are you from?",
"I am from New Haven, Conneticut! The cultural capital of Conneticut!",
"Which city are you from?",
"I am from New Haven, where Jackson is located!",
"Which state are you from?",
"I am proud citizen of New Haven, Conneticut!",
"what is your name?",
"You can call me Jackbot!",
"what should I call you?",
"You can call me Jackbot!",
"what is your name?",
"I'm Jackbot!"
"How do I apply for the fellowships listed on the Jackson website?'",
"I think Jackson offers very generous funding for its students. It shows in the statistics on our website! 100% of Jackson students who requested financial aid received it, with an average of $47,800! Oh, how can you be considered in the first place? You can simply check the box in the application!",
"Tell me more about Funding",
"In my opinion, Jackson is very generous in terms of funding. I do not want to be so technical, but 100% of Jackson students who requested financial aid received it, with an average of $47,800! How can you be considered for funding? Just make sure that you check the appropriate box in the application!",
"Does Jackson offer funding?",
"I think Jackson offers very generous funding for its students. It shows in the statistics on our website! 100% of Jackson students who requested financial aid received it, with an average of $47,800! Oh, how can you be considered in the first place? You can simply check the box in the application!",
"How can I pay for the school?",
"I understand that it is stressful to think about funding even before you get into the school! But it is an important part of your study. I would be happy to help you! I believe that Jackson is very good at financially helping students. 100% of Jackson students who requested financial aid received it, with an average of $47,800! Make sure you check the appropriate box in the application to be considered!",
"What are the opportunities for scholarship, fellowship or other forms of funding?",
"I understand that it is stressful to think about funding even before you get into the school! But it is an important part of your study. I would be happy to help you! I believe that Jackson is very good at financially helping students. 100% of Jackson students who requested financial aid received it, with an average of $47,800! Make sure you check the appropriate box in the application to be considered!",
"I am currently an undergraduate student, may I still apply?",
"Welcome! I am happy to hear that you are considering Jackson! However, I would recommend having 1-2 years of work experience after college unles syou are applying as part of a relevant fellowship or program. Is it helpful?",
"How many years of professional experience should I have to be considered?",
"I am glad that you are considering Jackson at the very early stage of your career! Thank you so much! Of course, you can apply as a current college student. However, most of the students have 3-4 years of professional experience.",
"How many years of work experience required to apply for Jackson?",
"It is a difficult quesiton to answer to be honest. Technically, you can apply as a graduating senior in college! However, please be mindful that the most of the current students have at least 3-4 years of work experience before joining Jackson",
"I have been preparing to apply for the M.A. in Global Affairs at Jackson, but cannot find reference to that degree option on the Jackson website anymore. What happened to it?",
"Hey! Thank you for your question! Let me explain this in a simple way. In short, Jackson no longer offers M.A. programs in Global Affairs. Instead, now it offers M.P.P. program.",
"I know that Jackson offered M.A. program in global affairs. However, now it only offers M.P.P MPP Mater in Public Policy program. Can you tell me what happened?",
"I am glad that you asked this question! As Jackson became a professional school in Fall 2022, JAckson decided to launch Master in Public Policy (M.P.P.) programs instead of M.A. programs in Global Affairs.",
"Does Jackson offer M.P.P Master in Public Policy or M.A. Master in Global Affairs",
"First of all, sorry for the confusion. In fact, Jackson no longer offers M.A. programs in Global Affairs. Instead, now it offers M.P.P. program.",
"I want to talk to the admission team. What would be the best way to do it?",
"Jackson provides a lot of ways that you can reach out! First, I think it would be good idea for you to check previous recorded webinars on the website. It should give you some ideas about the program and admission process. Second, you can also join those webinars yourself in the future! Lastly, I recommend you to check the admission calender on the website so that you can join either in person or through zoom.",
"Does Jackson offer webinars?",
"Yes, webinars are listed on the Jackson website",
"What event does Jackson have for prospective students?",
"Actually, Jackson is trying very hard to reach out to prospective students. I recommend you to go through the previous webinars recording on the website. You can also join future webinars and other events in the future. Please stay tuned!",
"Is there an admission event that I can join or participate in?",
"It is a great idea to meet people at Jackson in order to get to know the school better. You can get general idea about the school by (1) checking previous webinars, (2) join those webinars yourself, or (3) join other admission events listed on the website. So, stay tuned!",
"When is the deadline for submitting applications?",
"A great question! I want to really stress that Jackson will NOT accept applications received after the deadline of 11:59pm Eastern Time on 2 January. Of course, it is strongly advised to submit applications well before the deadline in order to avoid the possibility of technical issues in accessing your application",
"By when should I submit my application?",
"A great question! I want to really stress that Jackson will NOT accept applications received after the deadline of 11:59pm Eastern Time on 2 January. Of course, it is strongly advised to submit applications well before the deadline in order to avoid the possibility of technical issues in accessing your application",
"When is the deadline of the application?",
"A great question! I want to really stress that Jackson will NOT accept applications received after the deadline of 11:59pm Eastern Time on 2 January. Of course, it is strongly advised to submit applications well before the deadline in order to avoid the possibility of technical issues in accessing your application",
"How can I apply for an application fee waiver, if I meet the eligibility requirements?",
"Yes! It is a great question! I will give you this tip so you can save some money. To encourage early applications, Jackson will waive the application fee for all applications received by December 1. A form is not required to receive the waiver. However, remember, no preference will be given to early applications. Of course, you may still apply until our deadline of January 2, but the fee will not be waived automatically for applications submitted after 11:59 pm EST on December 1.",
"How can I get a waiver for the application fee?",
"Yes! It is a great question! I will give you this tip so you can save some money. To encourage early applications, Jackson will waive the application fee for all applications received by December 1. A form is not required to receive the waiver. However, remember, no preference will be given to early applications. Of course, you may still apply until our deadline of January 2, but the fee will not be waived automatically for applications submitted after 11:59 pm EST on December 1.",
"If I apply ealier, can I get application fee waivered?",
"Yes! It is a great question! I will give you this tip so you can save some money. To encourage early applications, Jackson will waive the application fee for all applications received by December 1. A form is not required to receive the waiver. However, remember, no preference will be given to early applications. Of course, you may still apply until our deadline of January 2, but the fee will not be waived automatically for applications submitted after 11:59 pm EST on December 1.",
"I applied but my recommendaiton may get there late. What should I do?",
"I know you are a very busy person. Ideally, all applicaiton materials have to be submitted to the school by the deadline. However, Jackson does not want to penalize you simply because your recommender(s) did not submit it on time. Please let the admission know your situation if that happens.",
"I applied but my recommendaiton may get there late. What should I do?",
"I know you are a very busy person. Ideally, all applicaiton materials have to be submitted to the school by the deadline. However, Jackson does not want to penalize you simply because your recommender(s) did not submit it on time. Please let the admission know your situation if that happens.",
"I applied but my recommendaiton may get there late. What should I do?",
"I know you are a very busy person. Ideally, all applicaiton materials have to be submitted to the school by the deadline. However, Jackson does not want to penalize you simply because your recommender(s) did not submit it on time. Please let the admission know your situation if that happens.",
"Does Jackson have rolling admission?",
"I am sorry to say this, but Jackson does not have rolling admissions, so if you want to submit their application by December 1, be mindful that it does not improve your chances of admission. Your decision does not go out earlier. All decisions go out in the middle of March and Jackson does have a final application deadline of January 2.",
"If I apply early, my application can get a priority? Like rolling admission?",
"I am sorry to say this, but Jackson does not have rolling admissions, so if you want to submit their application by December 1, be mindful that it does not improve your chances of admission. Your decision does not go out earlier. All decisions go out in the middle of March and Jackson does have a final application deadline of January 2.",
"When is the deadline for test score (GRE) report?"
"Thank you for thinking ahead of the plan! I want to be careful here. Jackson requires GRE score, and ideally the score has to be reported by January 2. However, Jackson will most likely accep test score that come in within a week of January. For your information, test scores usually take about 10 to 14 days.  So if you take your tests by the end of December, that's usually sufficient to get them into your application in time to be considered.",
"When would be the last day that I can take GRE test?"
"Thank you for thinking ahead of the plan! I want to be careful here. Jackson requires GRE score, and ideally the score has to be reported by January 2. However, Jackson will most likely accep test score that come in within a week of January. For your information, test scores usually take about 10 to 14 days.  So if you take your tests by the end of December, that's usually sufficient to get them into your application in time to be considered.",
"By when the GRE Test score to be reported?"
"Thank you for thinking ahead of the plan! I want to be careful here. Jackson requires GRE score, and ideally the score has to be reported by January 2. However, Jackson will most likely accep test score that come in within a week of January. For your information, test scores usually take about 10 to 14 days.  So if you take your tests by the end of December, that's usually sufficient to get them into your application in time to be considered.",
"Can the GRE requirement be waived?",
"It is an important question! I know GRE is not the favorite thing for applicants. Unfortunately, general GRE is required for M.P.P. application.",
"Should I take the GRE for my application to be considered?",
"It is an important question! I know GRE is not the favorite thing for applicants. Unfortunately, general GRE is required for M.P.P. application.",
"Is the GRE required?",
"It is an important question! I know GRE is not the favorite thing for applicants. Unfortunately, general GRE is required for M.P.P. application.",
"Should I take GRE to apply for Jackson?",
"It is an important question! I know GRE is not the favorite thing for applicants. Unfortunately, general GRE is required for M.P.P. application.",
"Why did Jackson introduce the masters in public policy M.P.P. program instead of the M.A.in global affairs?"
"I get this question a lot! So, I am glad that you raise this question.The Graduate School of Arts and Sciences at Yale is mostly Ph.D. program, so as you're poking around within the application form, you will probably notice that it's very very Ph.D. focused. So Jackson is a professional program we consider our sell our Master's degrees terminal degrees that you can receive these degrees and go out and do international policy and get on the get in the field and go make a difference in the world. That's part of the reason for their change from an MA to an MPP. We wanted to signal that we are professional program, not an academic program toward Ph.D.",
"What is the difference between M.A. and M.P.P?",
"I get this question a lot! So, I am glad that you raise this question.The Graduate School of Arts and Sciences at Yale is mostly Ph.D. program, so as you're poking around within the application form, you will probably notice that it's very very Ph.D. focused. So Jackson is a professional program we consider our sell our Master's degrees terminal degrees that you can receive these degrees and go out and do international policy and get on the get in the field and go make a difference in the world. That's part of the reason for their change from an MA to an MPP. We wanted to signal that we are professional program, not an academic program toward Ph.D.",
"What should we expect from M.P.P. programs?",
"I get this question a lot! So, I am glad that you raise this question.The Graduate School of Arts and Sciences at Yale is mostly Ph.D. program, so as you're poking around within the application form, you will probably notice that it's very very Ph.D. focused. So Jackson is a professional program we consider our sell our Master's degrees terminal degrees that you can receive these degrees and go out and do international policy and get on the get in the field and go make a difference in the world. That's part of the reason for their change from an MA to an MPP. We wanted to signal that we are professional program, not an academic program toward Ph.D.",
]


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

random_number_list = list(range(0, 89, 2))
random.shuffle(random_number_list)

def get_text():
    #question = ["Where is Yale University located?",'How can I contact Jackson?','Are there opportunities to earn money during the academic year?','I am currently an undergraduate student, may I still apply?', 'When is the deadline for submitting applications?']
    suggestion = f"""Ask me anything! """
    input_text = st.text_input(suggestion, key="input")
    return input_text

user_input_bool = 1


if user_input_bool != 0:
    user_input = get_text()


#Code
with open("intents.json") as file:
    data = json.load(file)

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


if st.session_state['generated']:
    if st.session_state["generated"][-1].startswith("Hello Casey"):
        col5, col6, col7 = st.columns([1,6,1])
        with col5:
            st.write("")

        with col6:
            st.markdown("<h1 style='text-align: center; color: blue;'>THANK YOU CASEY!</h1>", unsafe_allow_html=True)
            st.image("class.png", width=500)

        with col7:
            st.write("")

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
