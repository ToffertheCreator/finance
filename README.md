# 💸 Personal Finance Tracker (WIP)

> A simple, object-oriented personal finance tracker app built with Python and KivyMD. Track transactions, view analytics, and manage your savings — all in one lightweight desktop GUI.

## 🚀 Features

🧾 Transaction Tracking – Add income or expenses with category tags and dates\
💰 Savings Manager – Track your current savings and history\
📊 Analytics – Visualize your income and expenses\
🖼️ Modern UI – Built with KivyMD using Material Design components

## 🧱 Tech Stack

Python 3.10+\
Kivy 2.3.1\
KivyMD 1.2.0\
Sqlite3

## 📦 Installation

1. **Clone or Download the Project**  
   `git clone https://github.com/ToffertheCreator/finance.git`  
   _(Or download ZIP and extract manually)_

2. **Navigate to Project Directory**  
   `cd finance`

3. **(Optional but Recommended) Create Virtual Environment**  
   `python -m venv venv`

   **Activate the virtual environment:**

   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install Required Dependencies**  
   `pip install -r requirements.txt`

   _If requirements.txt is missing, manually install:_  
   `pip install kivy kivymd matplotlib numpy`

5. **For Graph Features**  
   `pip install kivy-garden`  
   `garden install matplotlib`

   _Optional for additional graph widgets:_  
   `garden install graph`

6. **Run the Application**  
   `python screenmanager.py`

## 🚀 Future Enhancements (Planned Features)

- **User Authentication**: Secure login and multi-user accounts with personalized data storage.
- **Admin Role**: Admin functionality to manage user permissions, ideal for company setups (e.g., employers adding income for workers).
- **Cloud Sync & Backup**: Sync data to the cloud or export/import for backups and multi-device access.
- **Mobile App Version**: Android and iOS apps for easy finance tracking on the go.
- **Recurring Transactions**: Automatic recurring income and expense entries.
- **Advanced Budgeting Tools**: Monthly budget targets, progress tracking, alerts, and detailed breakdowns.
- **Notifications & Reminders**: Alerts for upcoming bills, low balances, or savings goal milestones.
- **Data Visualization**: More advanced, interactive charts, trends, and financial insights.
- **Dual Currency Support**: Track finances in multiple currencies with live exchange rate updates.
- **Custom Categories**: Create, edit, and organize your own transaction categories.
- **Export Reports**: Export financial reports to PDF, Excel, or CSV formats.
- **AI-Powered Insights**: Smart recommendations, spending pattern detection, and saving tips powered by AI.
- **Settings Improvements**:
  - **Theme Options**: Dark mode and additional themes for enhanced usability.
  - **Currency Preferences**: Ability to switch currency settings anytime.
