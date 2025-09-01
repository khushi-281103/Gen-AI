import streamlit as st
import joblib

# Load the saved model (seo_blog_model.pkl from Colab)
model = joblib.load("seo_blog_model.pkl")

st.set_page_config(page_title="AI Blog Generator", page_icon="📝", layout="centered")
st.title("📝 AI Blog Generator with SEO Optimization")

# User Inputs
topic = st.text_input("Enter blog topic:")
keywords = st.text_area("Enter SEO keywords (comma-separated):")

if st.button("Generate Blog"):
    if topic.strip() == "":
        st.warning("Please enter a topic!")
    else:
        keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
        prompt = f"Write a detailed blog post about {topic}. Include SEO keywords: {', '.join(keyword_list)}."

        # Generate blog text
        result = model(
            prompt,
            max_new_tokens=400,        # generate new content beyond prompt
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

        blog_text = result[0]['generated_text']

        # Clean: remove prompt repetition if present
        if blog_text.startswith(prompt):
            blog_text = blog_text[len(prompt):].strip()

        # Display Blog Post
        st.subheader("Generated Blog Post:")
        st.write(blog_text)

        # Create SEO Meta Description (summary in 160 chars)
        meta_prompt = f"Summarize the following blog post into an SEO meta description (max 160 characters): {blog_text}"
        meta_result = model(
            meta_prompt,
            max_new_tokens=60,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        meta_desc = meta_result[0]['generated_text']

        # Clean meta description
        if meta_desc.startswith(meta_prompt):
            meta_desc = meta_desc[len(meta_prompt):].strip()

        st.subheader("Meta Description (SEO):")
        st.write(meta_desc)

        # Option to download blog
        st.download_button(
            label="📥 Download Blog Post",
            data=blog_text,
            file_name=f"{topic.replace(' ','_')}_blog.txt",
            mime="text/plain"
        )