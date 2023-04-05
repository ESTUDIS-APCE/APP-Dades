

import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['APCE12345']).generate()
print(hashed_passwords)