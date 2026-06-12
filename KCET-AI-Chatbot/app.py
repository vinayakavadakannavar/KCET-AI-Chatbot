
import streamlit as st
import pandas as pd
from openai import OpenAI

# --- CONFIGURATION ---
OPENAI_API_KEY = "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"

# Initialize the OpenAI Client safely
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

st.set_page_config(page_title="KCET AI Counselling Chatbot", page_icon="🎓")

# --- EXPANDED DATA MATRIX (Up to 2.2 Lakh Ranks) ---
colleges = {
    "CSE": [
        ("RVCE Bangalore (E005)", 446), ("PES University, Bangalore (E009)", 1375),
        ("MSRIT Bangalore (E006)", 1687), ("BMSCE Bangalore (E003)", 1893),
        ("SJCE Mysore (E021)", 3057), ("UVCE Bangalore (E001)", 4732),
        ("UBDT College of Engineering, Davanagere (E061)", 26549),
        ("UBDT College of Engineering (H.GOV), Davanagere (E066)", 46754),
        ("Gurunanak Dev Engineering College, Bidar (E043)", 74869),
        ("Hira Sugar Institute of Technology, Nidasoshi (E040)", 78999),
        ("Khaja Bandanawaz University, Kalaburagi (E042)", 81995),
        ("Bheemanna Khandre Institute of Technology, Bhalki (E044)", 83488),
        ("GSSS Institute of Engineering for Women, Mysore", 105430),
        ("BTL Institute of Technology, Bangalore", 125600),
        ("Kalpataru Institute of Technology, Tiptur", 145890),
        ("STJ Institute of Technology, Ranebennur", 168000),
        ("Sri Taralabalu Jagadguru Institute, Ranebennur", 185500),
        ("Bahubali College of Engineering, Shravanabelagola", 215300)
    ],
    "ISE": [
        ("MSRIT Bangalore (E006)", 3083), ("UVCE Bangalore (E001)", 6502),
        ("DSCE Bangalore (E007)", 7704), ("BIT Bangalore (E008)", 9985),
        ("BMSIT Yelahanka, Bangalore (E126)", 20064),
        ("SJC Institute of Technology, Chickkaballapur (E014)", 67998),
        ("BLDEA's VP Dr. P.G. Halakatti College, Bijapur (E038)", 77486),
        ("PDA College of Engineering, Gulbarga (E059)", 96299),
        ("Proudhadevaraya Institute of Technology, Hospet", 115200),
        ("KLE Institute of Technology, Hubli", 135800),
        ("Vivekananda College of Engineering, Puttur", 175900),
        ("Coorg Institute of Technology, Ponnampet", 210500),
        ("SECAB Institute of Engineering & Technology, Bijapur", 218000)
    ],
    "ECE": [
        ("RVCE Bangalore (E005)", 914), ("MSRIT Bangalore (E006)", 3746),
        ("SJCE Mysore (E021)", 6081), ("UVCE Bangalore (E001)", 8155),
        ("UBDT College of Engineering, Davanagere (E061)", 38707),
        ("UBDT College of Engineering (H.GOV), Davanagere (E066)", 67453),
        ("SJC Institute of Technology, Chickkaballapur (E014)", 93563),
        ("Jain College of Engineering, Belgaum", 112500),
        ("K V G College of Engineering, Sullia", 148300),
        ("Rural Engineering College, Hulkoti", 165800),
        ("Shaikh College of Engineering, Belagavi", 195400),
        ("Anjuman Engineering College, Bhatkal", 212000),
        ("Sri Sairam College of Engineering, Anekal", 219500)
    ],
    "AIML": [
        ("PES University, Bangalore (E009)", 2168), ("MSRIT Bangalore (E006)", 2756),
        ("UBDT College of Engineering, Davanagere (E061)", 43335),
        ("UBDT College of Engineering (H.GOV), Davanagere (E066)", 72723),
        ("Tontadarya College of Engineering, Gadag (E028)", 81816),
        ("Rao Bahadur Y.Mahabaleswarappa College, Bellary (E045)", 86143),
        ("Navkis College of Engineering, Hassan", 108500),
        ("Smt. Kamala and Sri Venkappa M.Agadi College, Laxmeshwar", 132400),
        ("Ekalavya Institute of Technology, Chamarajanagar", 188600),
        ("B G S Institute of Technology, Mandya", 205000),
        ("Yenepoya Institute of Technology, Mangalore", 216000)
    ],
    "ME": [
        ("RVCE Bangalore (E005)", 5007), ("BMSCE Bangalore (E003)", 12643),
        ("UVCE Bangalore (E001)", 43950), ("BIT Bangalore (E008)", 59131),
        ("Dr. Ambedkar Institute of Tech, Bangalore (E004)", 85661),
        ("UBDT College of Engineering, Davanagere (E061)", 115000), 
        ("KLE Technological University, Belgaum", 135000),
        ("UBDT College of Engineering (H.GOV), Davanagere (E066)", 145000),
        ("Sri Dharmasthala Manjunatheshwara College, Dharwad", 168500),
        ("Gogte Institute of Technology, Belgaum", 192000),
        ("Bapuji Institute of Engineering and Technology, Davangere", 215400)
    ]
}

def lookup_colleges(user_rank, user_branch):
    results = []
    for college, cutoff in colleges.get(user_branch, []):
        if user_rank <= cutoff:
            results.append([college, cutoff])
    return results

# --- UI INTERFACE ---
st.title("🎓 Namma KCET AI Counselling Chatbot")
st.caption("A smart conversational assistant to help you navigate Karnataka Engineering College Options entry.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your KCET AI Guide. You can ask me general questions about document verification, option entry, or just give me your rank and branch (e.g., 'My rank is 145000 in ME') to check colleges!"}
    ]

# Display ongoing chat history on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle student text input within the chat space
if user_prompt := st.chat_input("Ask a question or enter your rank..."):
    
    # Display user input
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Process AI/Local response
    with st.chat_message("assistant"):
        ai_response = ""
        
        # Look for branch keywords and digits
        words = user_prompt.upper()
        found_branch = None
        for b in ["CSE", "ISE", "ECE", "AIML", "ME"]:
            if b in words:
                found_branch = b
                
        digits = ''.join(filter(str.isdigit, user_prompt))
        
        # Condition 1: User is asking for college predictions
        if digits and found_branch:
            user_rank = int(digits)
            matched_data = lookup_colleges(user_rank, found_branch)
            
            if matched_data:
                ai_response = f"Based on your rank **{user_rank:,}** in **{found_branch}**, here are the possible colleges from our expanded database:\n\n"
                for col, cut in matched_data:
                    ai_response += f"* **{col}** (Last year cutoff: {cut:,})\n"
            else:
                ai_response = f"I checked the numbers for rank **{user_rank:,}** in **{found_branch}**, but no colleges in our current extended database match that cutoff. Don't worry, try participating in extended rounds!"
                
        # Condition 2: General counseling doubt (Talks to ChatGPT)
        else:
            if client:
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a helpful expert counselor specialized strictly in Karnataka Examination Authority (KEA) KCET engineering counseling regulations. Answer the student's question accurately, concisely, and cleanly."},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    ai_response = response.choices[0].message.content
                except Exception as e:
                    ai_response =f"ERROR:{e}"
            else:
                ai_response = "My AI brain is offline because the API key is missing!"

        # Display answer
        st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
