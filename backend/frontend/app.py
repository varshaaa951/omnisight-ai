import requests
import streamlit as st

st.set_page_config(
    page_title="OmniSight AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    .block-container{
        padding-top:1rem;
        padding-bottom:0rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 OmniSight AI Enterprise Dashboard")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 25 / 75 Layout
left, right = st.columns([1,3])

# ---------------- LEFT ---------------- #

with left:

    st.subheader("💬 Chat History")

    chat_container = st.container(height=600)

    with chat_container:

        if len(st.session_state.messages) == 0:
            st.info("No conversations yet.")

        else:

            for msg in st.session_state.messages:

                if msg["role"] == "User":
                    st.chat_message("user").write(msg["content"])
                else:
                    st.chat_message("assistant").write(msg["content"])

# ---------------- RIGHT ---------------- #

with right:

    tabs = st.tabs([
        "📊 Executive Summary",
        "👥 Customers",
        "📦 Orders",
        "📦 Inventory",
        "📄 Reports"
    ])

    with tabs[0]:

        c1, c2, c3 = st.columns(3)

        try:
            dashboard = requests.get(
                "http://127.0.0.1:8000/dashboard"
            ).json()
            c1.metric("Customers", dashboard["customers"])
            c2.metric("Orders", dashboard["orders"])
            c3.metric("Revenue", f"₹{dashboard['revenue']:,.0f}")
        except Exception:
            c1.metric("Customers", "-")
            c2.metric("Orders", "-")
            c3.metric("Revenue", "-")

        st.divider()

        if st.button("Generate Executive Summary"):
            try:
                response = requests.get(
                    "http://127.0.0.1:8000/ai-business-summary"
                )
                data = response.json()
                if isinstance(data, dict):
                    st.success(data.get("answer", str(data)))
                else:
                    st.success(data)
            except Exception:
                st.error("Backend Offline.")

    with tabs[1]:

        st.subheader("Customer Analytics")

        try:
            data = requests.get("http://127.0.0.1:8000/customers").json()
            st.dataframe(data, use_container_width=True)
        except Exception:
            st.warning("Customer data unavailable.")

    with tabs[2]:

        st.subheader("Order Analytics")

        try:
            data = requests.get("http://127.0.0.1:8000/orders").json()
            st.dataframe(data, use_container_width=True)
        except Exception:
            st.warning("Order data unavailable.")

    with tabs[3]:

        st.subheader("Inventory Analytics")

        try:
            data = requests.get("http://127.0.0.1:8000/inventory").json()
            st.dataframe(data, use_container_width=True)
        except Exception:
            st.warning("Inventory data unavailable.")

    with tabs[4]:

        st.subheader("Reports")

        st.success("PDF reports will appear here.")

question = st.chat_input("Ask OmniSight AI...")

if question:
    st.session_state.messages.append(
        {
            "role": "User",
            "content": question
        }
    )

    try:
        response = requests.get(
            f"http://127.0.0.1:8000/rag/{question}"
        )
        data = response.json()
        if isinstance(data, dict):
            answer = data.get("answer", str(data))
        else:
            answer = str(data)
    except Exception:
        answer = "Backend Offline."

    st.session_state.messages.append(
        {
            "role": "Assistant",
            "content": answer
        }
    )

    st.rerun()