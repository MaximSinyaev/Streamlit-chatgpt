import streamlit as st
import streamlit_authenticator as stauth


from ocr import ocr_tab
from gpt import chat_with_file
from aunth import authenticate

# CREDENTIALS = {
#     "admin": "password123",
#     "user1": "securepass",
#     "user2": "mypassword"
# }


# if "logged_in" not in st.session_state:
#     st.session_state["logged_in"] = False
#     st.session_state["username"] = ""

# def login(username, password):
#     """Authenticate user based on username and password."""
#     if username in CREDENTIALS and CREDENTIALS[username] == password:
#         st.session_state["logged_in"] = True
#         st.session_state["username"] = username
#         st.success(f"Welcome, {username}!")
#     else:
#         st.error("Invalid username or password.")

# def logout():
#     """Log out the user."""
#     st.session_state["logged_in"] = False
#     st.session_state["username"] = ""
    
    
if __name__ == "__main__":
    
    
    if authenticate():
        st.title("Демонстрация для распоззнавания анализов")
            

        # Create tabs
        tab1, tab2, tab3 = st.tabs(["ChatGPT with File", "OCR from File", "Hash Generator"])
        
        with tab3:
                with st.expander("Hash generator"):
                    st.write("This tool generates password hashes for storing securely.")
                    password = st.text_input("Enter example password for hash")
                    
                    if st.button("Generate Password Hashes") and password:
                        raw_passwords = [password, "123124asd"]
                        hashed_passwords = stauth.Hasher([password]).hash(password)
                        st.write("Store these hashed passwords securely:")
                        st.code(hashed_passwords)
                    else:
                        st.error("Please enter a password to hash.")
        
                

        # Tab 1: ChatGPT functionality
        with tab1:
            chat_with_file()

        # Tab 2: OCR functionality
        with tab2:
            ocr_tab()

