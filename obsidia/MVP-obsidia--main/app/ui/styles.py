"""Custom CSS styles for Obsidia interface."""
import streamlit as st

def inject_custom_css():
    """
    Inject custom CSS for professional appearance and subtle animations.
    """
    st.markdown("""
    <style>
    /* Smooth transitions for all interactive elements */
    button, .stButton > button {
        transition: all 0.3s ease;
    }
    
    button:hover, .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Stepper animation */
    .stepper-item {
        transition: all 0.4s ease;
    }
    
    .stepper-item.active {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    /* Card hover effects */
    .stExpander {
        transition: all 0.3s ease;
    }
    
    .stExpander:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Metrics animation */
    [data-testid="stMetricValue"] {
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Success/Warning/Error messages animation */
    .stAlert {
        animation: slideIn 0.4s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Sidebar improvements */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Header improvements */
    h1, h2, h3 {
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* Professional spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        [data-testid="column"] {
            min-width: 100% !important;
        }
    }
    
    /* Loading spinner customization */
    .stSpinner > div {
        border-color: #4CAF50 transparent transparent transparent;
    }
    
    /* Plotly chart improvements */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Code block improvements */
    .stCodeBlock {
        border-radius: 8px;
        background: #f5f5f5;
    }
    
    /* Tab improvements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(76, 175, 80, 0.1);
    }
    
    /* Download button improvements */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """, unsafe_allow_html=True)

def inject_responsive_meta():
    """
    Inject responsive meta tags for mobile optimization.
    """
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """, unsafe_allow_html=True)
