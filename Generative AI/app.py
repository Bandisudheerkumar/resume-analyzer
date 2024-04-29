from flask import Flask, render_template, request, redirect, url_for
import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import re
from gtts import gTTS

app = Flask(__name__, static_url_path='/static')


# Set up OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk-proj-0GLgfOhG4wgq9juTSUAAT3BlbkFJp12Mz4CKjltbhHLg833B'

# Initialize the OpenAI model
llm_chatbot = OpenAI(temperature=0.6)

# Prompt template for the chatbot
prompt_template_chatbot = PromptTemplate(
    input_variables=['question'],
    template="{question}"
)

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    question = None
    response = None
    audio_link = None
    if request.method == 'POST':
        if 'question' in request.form:
            question = request.form['question']
            # Create LLMChain for the chatbot
            chain_chatbot = LLMChain(llm=llm_chatbot, prompt=prompt_template_chatbot)
            # Prepare input data
            input_data = {'question': question}
            # Generate response from the chatbot
            response = chain_chatbot.run(input_data)
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(response) 
            engine.runAndWait() 
        elif 'clear' in request.form and request.form['clear'] == 'true':
            # Clear chat history
            return redirect(url_for('index'))
        elif 'audio' in request.form and request.form['audio'] == 'true':
            # Convert response to audio
            if response:
                import pyttsx3 
  
                # initialisation 
                engine = pyttsx3.init() 
                  
                # testing 
                engine.say(response) 
                engine.runAndWait() 

    return render_template('index.html', question=question, response=response, audio_link=audio_link)

if __name__ == '__main__':
    app.run(debug=True)
