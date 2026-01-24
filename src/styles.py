import streamlit as st

def get_custom_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        :root {
            --primary-color: #10b981; /* Emerald 500 */
            --primary-dark: #059669; /* Emerald 600 */
            --bg-color: #f8f9fa;
            --text-color: #1f2937;
            --card-bg: #ffffff;
            --sidebar-bg: #ffffff;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: var(--text-color);
            background-color: var(--bg-color);
        }

        /* Hide Streamlit Default Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Layout Adjustments */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 5rem;
            max-width: 1200px;
        }

        /* Custom Header */
        .orbital-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .orbital-logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .orbital-logo span {
            color: var(--primary-color);
        }

        /* Search Bar Placeholder */
        .search-bar {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 999px;
            padding: 0.5rem 1rem;
            width: 300px;
            color: #9ca3af;
            font-size: 0.875rem;
        }

        /* User Profile */
        .user-profile {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: white;
            padding: 0.25rem 0.5rem;
            border-radius: 999px;
            border: 1px solid #e5e7eb;
        }
        
        .user-avatar {
            background: var(--primary-color);
            color: white;
            width: 2rem;
            height: 2rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.8rem;
        }

        /* Cards */
        .orbital-card {
            background: var(--card-bg);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: var(--shadow-sm);
            border: 1px solid #f3f4f6;
            transition: all 0.2s ease;
        }
        
        .orbital-card:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }

        /* Typography */
        h1 {
            font-weight: 700;
            color: #111827;
            font-size: 2.25rem !important;
        }
        
        h2 {
            font-weight: 600;
            color: #1f2937;
            font-size: 1.5rem !important;
            margin-bottom: 1rem !important;
        }
        
        h3 {
            font-weight: 600;
            color: #374151;
            font-size: 1.1rem !important;
        }
        
        /* Pills & Tags */
        .meta-tag {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            background: #f3f4f6;
            color: #4b5563;
            padding: 0.25rem 0.75rem;
            border-radius: 0.5rem;
            font-size: 0.875rem;
            font-weight: 500;
        }

        /* Primary Button (Main Content Only) */
        .main .stButton button {
            background-color: var(--primary-color) !important;
            color: white !important;
            border: none;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .main .stButton button:hover {
            background-color: var(--primary-dark) !important;
            box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3);
        }

        /* Sidebar History Buttons */
        [data-testid="stSidebar"] .stButton button {
            background-color: transparent !important;
            color: #374151 !important;
            border: 1px solid transparent !important;
            text-align: left !important;
            padding: 0.75rem !important;
            font-weight: 500 !important;
            width: 100%;
            border-radius: 0.5rem;
            display: flex;
            justify-content: flex-start;
        }

        [data-testid="stSidebar"] .stButton button:hover {
            background-color: #f3f4f6 !important;
            border-color: #e5e7eb !important;
            color: #111827 !important;
        }
        
        [data-testid="stSidebar"] .stButton button:focus {
            background-color: #ecfdf5 !important;
            color: #059669 !important;
            border-color: #d1fae5 !important;
        }

        /* Executive Insights Card */
        .insight-card {
            background-color: white;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: var(--shadow-sm);
            height: 100%;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: white;
            border-right: 1px solid #f3f4f6;
        }
        
        .history-item {
            padding: 1rem;
            border-radius: 0.75rem;
            margin-bottom: 0.5rem;
            cursor: pointer;
            border: 1px solid transparent;
        }
        
        .history-item:hover {
            background-color: #f0fdf9; /* Emerald 50 */
            border-color: #d1fae5;
        }
        
        .history-title {
            font-weight: 600;
            font-size: 0.9rem;
            color: #1f2937;
            margin-bottom: 0.25rem;
        }
        
        .history-meta {
            font-size: 0.75rem;
            color: #9ca3af;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1; 
        }
        ::-webkit-scrollbar-thumb {
            background: #d1d5db; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #9ca3af; 
        }

    </style>
    """
