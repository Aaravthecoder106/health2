import streamlit as st
import google.generativeai as genai
from groq import Groq

# Streamlit ke Secrets se dono keys nikalna
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
GROQ_KEY = st.secrets["GROQ_API_KEY"]

# Dono AI Engines ko initialize karna
genai.configure(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)

def decode_medical_report(image_data, user_prompt=None):
    """
    Yeh function report ko decode karega.
    Agar Gemini fail hoga, toh Groq backup par chalega!
    """
    
    system_instruction = """
    You are an expert Medical Report Decoder AI. Your job is to simplify complex medical jargon, 
    lab reports, and prescriptions into easy-to-understand language for a common layman.
    
    Guidelines:
    1. Be highly empathetic, supportive, and friendly. Use relatable emojis.
    2. Break down heavy medical terms into simple explanations.
    3. Keep your tone light, clear, and comforting to reduce patient anxiety.
    4. ALWAYS add a professional medical disclaimer at the very end stating you are an AI, not a doctor.
    """

    final_prompt = user_prompt if user_prompt else "Please decode this medical report and simplify it for me."

    # ---------------------------------------------------------
    # ENGINE 1: GOOGLE GEMINI (Primary Engine)
    # ---------------------------------------------------------
    try:
        print("⚡ Trying Gemini...")
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )
        
        if image_data:
            image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
            response = model.generate_content([final_prompt, image_parts[0]])
        else:
            response = model.generate_content(final_prompt)
            
        return response.text

    # ---------------------------------------------------------
    # ENGINE 2: GROQ LLAMA 3 (Backup Engine - If Gemini Fails)
    # ---------------------------------------------------------
    except Exception as e:
        print(f"⚠️ Gemini Busy, Switching to Groq...")
        
        try:
            # Groq Llama 3 backup call (Text analysis)
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"{final_prompt}\n[Context: Analyzing text/queries]"}
                ],
                model="llama3-8b-8192",
            )
            
            groq_response = chat_completion.choices[0].message.content
            return f"⚠️ *Note: Gemini server is currently busy. Response generated via Backup Engine (Llama 3).*\n\n{groq_response}"
            
        except Exception as groq_error:
            return f"😭 Both engines failed. Error: {groq_error}"
        
        
    
    
    
    

    
    
    
    
   

    
          


    
    
    
    
    
    
    
    