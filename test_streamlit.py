import streamlit as st

st.title("🧪 Streamlit Test")
st.write("Hello Rob! Streamlit is working!")

# Test basic components
st.subheader("Basic Components Test")

# Text input
name = st.text_input("Enter your name:", "Rob")
st.write(f"Hello {name}!")

# Button
if st.button("Click me!"):
    st.write("Button clicked! ✅")

# Slider
value = st.slider("Pick a number", 1, 100, 50)
st.write(f"You picked: {value}")

# Columns
col1, col2 = st.columns(2)

with col1:
    st.write("Left column")
    st.metric("Coding Streak", "5 days", "+1")

with col2:
    st.write("Right column") 
    st.metric("Progress", "25%", "+5%")
    