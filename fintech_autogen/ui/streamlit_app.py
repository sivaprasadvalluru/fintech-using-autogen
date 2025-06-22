import streamlit as st
import asyncio
from fintech_autogen.teams.master_orchestrator import MasterOrchestrator
from pathlib import Path

# Session state for authentication
def init_session():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'role' not in st.session_state:
        st.session_state['role'] = None
    if 'email' not in st.session_state:
        st.session_state['email'] = ''

init_session()

st.title('Fintech-AutoGen Platform')

if not st.session_state['authenticated']:
    st.subheader('Login')
    role = st.radio('Select your role:', ['User', 'Admin'])
    email = st.text_input('Enter your email:')
    if st.button('Login'):
        if email:
            st.session_state['authenticated'] = True
            st.session_state['role'] = role
            st.session_state['email'] = email
        else:
            st.warning('Please enter your email to continue.')
else:
    st.sidebar.write(f"Logged in as: {st.session_state['email']} ({st.session_state['role']})")
    if st.sidebar.button('Logout'):
        st.session_state['authenticated'] = False
        st.session_state['role'] = None
        st.session_state['email'] = ''
        st.rerun()

    if st.session_state['role'] == 'Admin':
        st.header('Admin Dashboard')
        st.write('''
        - Document upload for knowledge base
        - ChromaDB ingestion management
        - User management dashboard
        - System monitoring
        ''')
        # --- Document Upload for Knowledge Base ---
        st.subheader('Upload Document to Knowledge Base')
        uploaded_file = st.file_uploader('Choose a file to upload (txt, pdf, docx)', type=['txt', 'pdf', 'docx'])
        if uploaded_file is not None:
            # Save uploaded file to knowledge_base/kb_texts
            kb_dir = Path(__file__).parent.parent / 'knowledge_base' / 'kb_texts'
            kb_dir.mkdir(parents=True, exist_ok=True)
            file_path = kb_dir / uploaded_file.name
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.success(f'File "{uploaded_file.name}" uploaded and saved!')
            # Placeholder: In future, trigger ChromaDB ingestion
        # --- ChromaDB Ingestion Management ---
        st.subheader('ChromaDB Ingestion Management')
        st.info('ChromaDB ingestion controls will appear here.')
        # --- User Management Dashboard ---
        st.subheader('User Management')
        from fintech_autogen.database.queries import get_user_by_email
        import sqlite3
        db_path = Path(__file__).parent.parent / 'database' / 'fintech.db'
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT user_id, email, name, role, created_at FROM users')
        users = cur.fetchall()
        conn.close()
        st.table([{'User ID': u[0], 'Email': u[1], 'Name': u[2], 'Role': u[3], 'Created': u[4]} for u in users])
        # --- System Monitoring ---
        st.subheader('System Monitoring')
        # Show DB status
        db_exists = (Path(__file__).parent.parent / 'database' / 'fintech.db').exists()
        st.write(f"Database status: {'✅ Available' if db_exists else '❌ Not found'}")
        # Show agent/team status (basic)
        st.write('Agents/Teams loaded:')
        st.write('- MasterOrchestrator')
        st.write('- Financial Education Team')
        st.write('- Portfolio Optimization Team')
        st.write('- Market Research Team')
        st.info('Admin features coming soon...')
    else:
        st.header('User Dashboard')
        st.write('''
        - Chat interface with conversation history
        - Portfolio dashboard with visualizations
        - Educational content display
        ''')
        # --- Chat Interface ---
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        if 'orchestrator' not in st.session_state:
            st.session_state['orchestrator'] = MasterOrchestrator()
        st.subheader('Chat with Fintech Agents')
        for msg in st.session_state['chat_history']:
            st.markdown(f"**{msg['role']}:** {msg['content']}")
        user_input = st.text_input('Type your message:', key='chat_input')
        if st.button('Send', key='send_btn'):
            if user_input:
                st.session_state['chat_history'].append({'role': 'User', 'content': user_input})
                # Call orchestrator and get response
                async def get_agent_response(query):
                    response = await st.session_state['orchestrator'].run_stream(query)
                    return response
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    agent_response = loop.run_until_complete(get_agent_response(user_input))
                except Exception as e:
                    agent_response = f"[Agent error: {e}]"
                st.session_state['chat_history'].append({'role': 'Agent', 'content': str(agent_response)})
                st.rerun()
        # --- Portfolio Dashboard ---
        st.subheader('Portfolio Dashboard')
        from fintech_autogen.database.queries import get_user_by_email, get_user_portfolios, get_portfolio_holdings
        user = get_user_by_email(st.session_state['email'])
        if user:
            portfolios = get_user_portfolios(user['user_id'])
            if portfolios:
                for portfolio in portfolios:
                    st.markdown(f"**Portfolio:** {portfolio['name']}  ")
                    st.markdown(f"Description: {portfolio['description']}  ")
                    st.markdown(f"Cash Balance: ${portfolio['cash_balance']:.2f}")
                    holdings = get_portfolio_holdings(portfolio['portfolio_id'])
                    if holdings:
                        import pandas as pd
                        import plotly.express as px
                        df = pd.DataFrame(holdings)
                        df['Value'] = df['shares'] * df['current_price']
                        st.dataframe(df[['ticker', 'name', 'shares', 'avg_purchase_price', 'current_price', 'Value']])
                        fig = px.pie(df, names='ticker', values='Value', title=f"{portfolio['name']} Allocation")
                        st.plotly_chart(fig)
                    else:
                        st.info('No holdings in this portfolio.')
            else:
                st.info('No portfolios found for this user.')
        else:
            st.warning('User not found in database.')
        # --- Educational Content Display ---
        st.subheader('Educational Content')
        st.info('Personalized financial education content will appear here.')
        if st.button('Get Educational Content'):
            async def get_education():
                response = await st.session_state['orchestrator'].run_education('Provide a financial education topic for the user.')
                return response
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                edu_content = loop.run_until_complete(get_education())
            except Exception as e:
                edu_content = f"[Agent error: {e}]"
            st.session_state['edu_content'] = str(edu_content)
            st.rerun()
        if 'edu_content' in st.session_state:
            st.markdown(st.session_state['edu_content'])
