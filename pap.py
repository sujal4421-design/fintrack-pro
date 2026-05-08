import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# -------------------- Page Config --------------------
st.set_page_config(page_title="FinTrack Pro", page_icon="💰", layout="wide")

# -------------------- Custom CSS --------------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #F5F7FA;
    color: #1E293B;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #E2E8F0;
}

/* Buttons */
.stButton>button {
    background-color: #6366F1;
    color: white;
    border-radius: 8px;
    border: none;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: white;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #CBD5E1;
}

</style>
""", unsafe_allow_html=True)

# -------------------- Initialize --------------------
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=['Date', 'Category', 'Amount', 'Description']
    )

# -------------------- Functions --------------------
def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame(
        [[date, category, amount, description]],
        columns=st.session_state.expenses.columns
    )

    st.session_state.expenses = pd.concat(
        [st.session_state.expenses, new_expense],
        ignore_index=True
    )


def visualize_expenses():

    if not st.session_state.expenses.empty:

        df = st.session_state.expenses.groupby(
            'Category'
        )['Amount'].sum().reset_index()

        # ---------------- Bar Chart ----------------
        st.subheader("📊 Bar Chart")

        fig1, ax1 = plt.subplots()

        sns.barplot(
            data=df,
            x='Category',
            y='Amount',
            ax=ax1
        )

        plt.xticks(rotation=45)

        ax1.set_title("Expenses by Category")

        st.pyplot(fig1)

        # ---------------- Pie Chart ----------------
        st.subheader("🥧 Pie Chart")

        fig2, ax2 = plt.subplots()

        ax2.pie(
            df['Amount'],
            labels=df['Category'],
            autopct='%1.1f%%'
        )

        ax2.set_title("Expense Distribution")

        st.pyplot(fig2)

        # ---------------- Line Chart ----------------
        st.subheader("📈 Daily Expense Trend")

        daily = st.session_state.expenses.groupby(
            'Date'
        )['Amount'].sum()

        st.line_chart(daily)

    else:
        st.warning("No expenses to visualize!")


def download_expenses():

    csv = st.session_state.expenses.to_csv(
        index=False
    ).encode('utf-8')

    st.download_button(
        label="⬇️ Download Expenses CSV",
        data=csv,
        file_name='expenses.csv',
        mime='text/csv'
    )


# -------------------- Title --------------------
st.markdown(
    "<h1 style='text-align:center; color:#6366F1;'>💰 FinTrack Pro</h1>",
    unsafe_allow_html=True
)

st.markdown("### Personal Finance Management Dashboard")

# -------------------- Sidebar --------------------
with st.sidebar:

    st.header('➕ Add Expense')

    date = st.date_input('Date')

    category = st.selectbox(
        'Category',
        [
            '🍔 Food',
            '🚕 Transport',
            '🎬 Entertainment',
            '💡 Utilities',
            '🛒 Shopping',
            '📚 Education',
            '📦 Other'
        ]
    )

    amount = st.number_input(
        'Amount',
        min_value=0.0,
        format="%.2f"
    )

    description = st.text_input('Description')

    if st.button('Add Expense'):

        add_expense(
            date,
            category,
            amount,
            description
        )

        st.success('Expense Added Successfully!')

    st.divider()

    # ---------------- Budget ----------------
    st.header('💵 Monthly Budget')

    budget = st.number_input(
        'Set Your Budget',
        min_value=0.0,
        value=5000.0
    )

    st.divider()

    # ---------------- File Upload ----------------
    st.header('📂 Upload CSV')

    uploaded_file = st.file_uploader(
        "Upload Expense File",
        type=['csv']
    )

    if uploaded_file is not None:

        st.session_state.expenses = pd.read_csv(
            uploaded_file
        )

        st.success("File Uploaded Successfully!")

    st.divider()

    # ---------------- Download ----------------
    st.header('💾 Save Data')

    download_expenses()

    st.divider()

    # ---------------- Clear ----------------
    if st.button("🗑️ Clear All Expenses"):

        st.session_state.expenses = pd.DataFrame(
            columns=[
                'Date',
                'Category',
                'Amount',
                'Description'
            ]
        )

        st.warning("All Expenses Cleared!")

# -------------------- Dashboard Metrics --------------------
if not st.session_state.expenses.empty:

    total_expense = st.session_state.expenses[
        'Amount'
    ].sum()

    highest_expense = st.session_state.expenses[
        'Amount'
    ].max()

    total_transactions = len(
        st.session_state.expenses
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💵 Total Expense",
        f"₹ {total_expense:.2f}"
    )

    col2.metric(
        "📊 Transactions",
        total_transactions
    )

    col3.metric(
        "🔥 Highest Expense",
        f"₹ {highest_expense:.2f}"
    )

    # ---------------- Budget Status ----------------
    st.subheader("💰 Budget Status")

    progress = min(total_expense / budget, 1.0)

    st.progress(progress)

    if total_expense > budget:

        st.error("⚠️ Budget Exceeded!")

    else:

        remaining = budget - total_expense

        st.success(
            f"✅ Remaining Budget: ₹ {remaining:.2f}"
        )

else:
    total_expense = 0

# -------------------- Tabs --------------------
tab1, tab2, tab3 = st.tabs([
    "📋 Expenses",
    "🔍 Search & Filter",
    "📊 Analytics"
])

# =====================================================
# TAB 1 - EXPENSES
# =====================================================
with tab1:

    st.header('📋 Expense Records')

    if not st.session_state.expenses.empty:

        st.dataframe(
            st.session_state.expenses
        )

        st.subheader("🕒 Recent Transactions")

        st.table(
            st.session_state.expenses.tail(5)
        )

        # ---------------- Delete Expense ----------------
        st.subheader("🗑️ Delete Expense")

        row_number = st.number_input(
            "Enter Row Number to Delete",
            min_value=0,
            max_value=len(
                st.session_state.expenses
            ) - 1,
            step=1
        )

        if st.button("Delete Selected Row"):

            st.session_state.expenses.drop(
                row_number,
                inplace=True
            )

            st.session_state.expenses.reset_index(
                drop=True,
                inplace=True
            )

            st.success(
                "Expense Deleted Successfully!"
            )

    else:
        st.info("No expenses added yet.")

# =====================================================
# TAB 2 - SEARCH & FILTER
# =====================================================
with tab2:

    st.header("🔍 Search Expenses")

    if not st.session_state.expenses.empty:

        search = st.text_input(
            "Search by Description"
        )

        filtered = st.session_state.expenses[
            st.session_state.expenses[
                'Description'
            ]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

        st.dataframe(filtered)

        st.subheader("📅 Filter by Date")

        selected_date = st.date_input(
            "Select Date",
            key="filter_date"
        )

        filtered_date = st.session_state.expenses[
            st.session_state.expenses[
                'Date'
            ].astype(str) == str(selected_date)
        ]

        st.dataframe(filtered_date)

    else:
        st.warning(
            "No data available for searching."
        )

# =====================================================
# TAB 3 - ANALYTICS
# =====================================================
with tab3:

    st.header('📊 Expense Analytics')

    if not st.session_state.expenses.empty:

        # ---------------- Highest Spending Category ----------------
        category_df = (
            st.session_state.expenses
            .groupby('Category')['Amount']
            .sum()
            .reset_index()
        )

        highest = category_df.loc[
            category_df['Amount'].idxmax()
        ]

        st.subheader(
            "🏆 Highest Spending Category"
        )

        st.write(
            f"{highest['Category']} : ₹ {highest['Amount']:.2f}"
        )

        # ---------------- Highest Expenses ----------------
        st.subheader("📌 Highest Expenses")

        sorted_df = (
            st.session_state.expenses
            .sort_values(
                by='Amount',
                ascending=False
            )
        )

        st.dataframe(sorted_df)

        # ---------------- AI Expense Suggestions ----------------
        st.subheader("🤖 Smart Expense Suggestions")

        category_totals = (
            st.session_state.expenses
            .groupby('Category')['Amount']
            .sum()
        )

        food_expense = category_totals.get(
            '🍔 Food',
            0
        )

        transport_expense = category_totals.get(
            '🚕 Transport',
            0
        )

        shopping_expense = category_totals.get(
            '🛒 Shopping',
            0
        )

        entertainment_expense = category_totals.get(
            '🎬 Entertainment',
            0
        )

        # Food Suggestion
        if food_expense > 3000:
            st.warning(
                "⚠️ Your food expenses are quite high this month."
            )

        # Shopping Suggestion
        if shopping_expense > 5000:
            st.warning(
                "🛒 You spent a lot on shopping. Try limiting unnecessary purchases."
            )

        # Entertainment Suggestion
        if entertainment_expense > 2000:
            st.info(
                "🎬 Entertainment spending increased this month."
            )

        # Transport Suggestion
        if transport_expense > 2500:
            st.info(
                "🚕 Transport expenses are higher than usual."
            )

        # Budget Analysis
        if total_expense > budget:

            st.error(
                "🚨 You have exceeded your monthly budget!"
            )

        elif total_expense > budget * 0.8:

            st.warning(
                "⚠️ You already used more than 80% of your budget."
            )

        else:

            st.success(
                "✅ Great job managing your expenses!"
            )

        # ---------------- Charts ----------------
        visualize_expenses()

    else:
        st.warning("No analytics available.")

# -------------------- Footer --------------------
st.markdown("---")

st.markdown(
    "<center>Made through using Python & Streamlit</center>",
    unsafe_allow_html=True
)