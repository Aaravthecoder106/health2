import streamlit as st
import google.generativeai as genai
from groq import Groq

# Streamlit Secrets se dono keys nikalna
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
GROQ_KEY = st.secrets["GROQ_API_KEY"]

# AI Engines ko initialize karna
genai.configure(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)

def decode_medical_report(image_bytes, user_prompt=None, audio_bytes=None):
    """
    Super-advanced handler: Image, Text, aur Voice Audio 
    teeno ko ek sath support karta hai bina crash hue!
    """
    
    system_instruction = """
    You are an expert Medical Report Decoder AI. Your job is to simplify complex medical jargon, 
    lab reports, and prescriptions into easy-to-understand language for a common layman.
    
    Guidelines:
    1. Be highly empathetic, supportive, and friendly. Use relatable emojis.
    2. Break down heavy medical terms into simple explanations.
    3. Keep your tone light, clear, and comforting to reduce patient anxiety.
    4. Provide clear headings and bullet points in clean markdown.
    5. ALWAYS add a professional medical disclaimer at the very end stating you are an AI, not a doctor.
    """

    final_prompt = user_prompt if user_prompt else "Please decode this medical report and simplify it for me."

    try:
        print("⚡ Processing with Gemini 2.5 Flash...")
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )
        
        # Contents array jisme saara data pack hoga
        contents = [final_prompt]
        
        # 1. Agar image input upload kiya hai
        if image_bytes:
            contents.append({"mime_type": "image/jpeg", "data": image_bytes})
            
        # 2. Agar microphone se voice record kiya hai
        if audio_bytes:
            contents.append({"mime_type": "audio/wav", "data": audio_bytes})
            
        # Gemini main call
        response = model.generate_content(contents)
        return response.text

    except Exception as e:
        print(f"⚠️ Gemini busy or failed: {e}. Switching to Groq...")
        try:
            # Fallback to Groq Llama 3 (Text only processing)
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"{final_prompt}\n[Context: Processing query texts directly via backup engine]"}
                ],
                model="llama-3.1-8b-instant",
            )
            groq_response = chat_completion.choices[0].message.content
            return f"⚠️ *Note: Gemini server is currently busy. Response generated via Backup Engine (Llama 3).* \n\n{groq_response}"
        except Exception as groq_error:
            return f"😭 Absolute Engine Failure. Error: {groq_error}"
            
            
        
        
    
    
    
    

    
    
    
    
   

    
          


    
    
    
    
    
    
    
    
