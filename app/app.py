import streamlit as st
from utils.scoring import score_proposal
from utils.review import review_proposal
from utils.pdf_reader import extract_text
from utils.text_cleaner import clean_text
from utils.chunker import chunk_text
from utils.embedder import get_embeddings
from utils.vector_store import create_index, search
from utils.llm import ask_llm


st.set_page_config(
    page_title="Research Proposal Review Assistant",
    page_icon="📚",
    layout="wide"
)

st.sidebar.title("📚 Research Proposal Review Assistant")
st.sidebar.markdown("---")
st.sidebar.write("### Features")
st.sidebar.write("✅ Question Answering")
st.sidebar.write("✅ Proposal Review")
st.sidebar.write("✅ Proposal Scoring")

st.sidebar.markdown("---")
st.sidebar.write("### Technology Stack")
st.sidebar.write("- Python")
st.sidebar.write("- Streamlit")
st.sidebar.write("- FAISS")
st.sidebar.write("- Sentence Transformers")
st.sidebar.write("- Gemini API")

# Main page
st.title("📚 AI-Powered Research Proposal Review Assistant")
st.markdown("### Review, Evaluate, and Query Research Proposals using RAG + Gemini")
st.divider() 

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


uploaded_file = st.file_uploader(
    "Upload Research Proposal (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    with st.spinner("Reading PDF..."):
        raw_text = extract_text(uploaded_file)

    with st.spinner("Cleaning text..."):
        cleaned_text = clean_text(raw_text)

    with st.spinner("Creating chunks..."):
        chunks = chunk_text(cleaned_text)

    with st.spinner("Generating embeddings..."):
        embeddings = get_embeddings(chunks)

    with st.spinner("Creating FAISS index..."):
        index = create_index(embeddings)

    st.success(f"PDF processed successfully! {len(chunks)} chunks created.") 

    st.subheader("📊 Proposal Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Words", len(cleaned_text.split()))

    with col2:
        st.metric("Chunks", len(chunks))

    with col3:
        st.metric("Embedding Dimension", embeddings.shape[1])

    st.divider()

    if st.button("📋 Generate Proposal Review"):

    # Use all chunks to create one large context
        context = "\n\n".join(chunks)

        with st.spinner("Reviewing research proposal..."):
            review = review_proposal(context)

        st.header("📋 Proposal Review")
        st.markdown(review) 

        st.download_button(
            label="📥 Download Review",
            data=review,
            file_name="proposal_review.txt",
            mime="text/plain"
        )

    if st.button("⭐ Generate Proposal Score"):

        context = "\n\n".join(chunks)

        with st.spinner("Evaluating proposal..."):
            score = score_proposal(context)

        st.header("⭐ Proposal Evaluation")
        st.markdown(score)    

        st.download_button(
            label="📥 Download Score",
            data=score,
            file_name="proposal_score.txt",
            mime="text/plain"
        )

    # Ask question
    question = st.text_input(
        "Ask a question about the proposal"
    )

    if question:

        # STEP 6: Embed the question
        query_embedding = get_embeddings([question])

        # STEP 7: Search similar chunks
        distances, indices = search(index, query_embedding, k=3)

        # STEP 8: Collect retrieved chunks
        retrieved_chunks = []
        retrieved_distances = []
        threshold = 0.50

        for i, idx in enumerate(indices[0]):
            distance = distances[0][i]
            if distance < threshold:
                retrieved_chunks.append(chunks[idx])
                retrieved_distances.append(distance)

        # If no chunk passes the threshold, use the nearest chunk
        if not retrieved_chunks:
            best_idx = indices[0][0]
            retrieved_chunks.append(chunks[best_idx])
            retrieved_distances.append(distances[0][0])

        # STEP 9: Create context
        context = "\n\n".join(retrieved_chunks) 
 
        # STEP 10: Ask Gemini
        with st.spinner("Analyzing proposal..."):
            answer = ask_llm(context, question)

        st.toast("Analysis completed! ✅")

# Save conversation
        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        # STEP 11: Display answer
        st.header(" AI Answer")
        st.markdown(answer)

        # Optional: show retrieved chunks
        with st.expander("Retrieved Chunks"):
            for i, chunk in enumerate(retrieved_chunks):
                st.markdown(f"### Chunk {i+1}")
                st.write(f"**L2 Distance:** {retrieved_distances[i]:.4f}")
                st.write(chunk)
                st.divider() 

        st.divider()

st.header("💬 Conversation History")

if len(st.session_state.chat_history) == 0:
    st.info("No questions asked yet.")

else:
    for i, chat in enumerate(st.session_state.chat_history, start=1):

        st.markdown(f"### Question {i}")

        st.markdown(f"**❓ Question:** {chat['question']}")

        st.markdown(f"**🤖 Answer:**")

        st.write(chat["answer"])

        st.divider() 
if st.button("🗑️ Clear Conversation History"):
    st.session_state.chat_history = []
    st.rerun()

st.divider()

st.caption(
    "AI-Powered Research Proposal Review System | "
    "Built using Streamlit, Sentence Transformers, FAISS, and Gemini"
)