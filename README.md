# GTM Lead Scoring Tool

An AI-powered application designed to help Go-To-Market (GTM) teams automate lead research, enrich company profiles using Gemini API, score companies based on an Ideal Customer Profile (ICP), and prioritize high-value leads for outbound sales.

---

## 🏗️ Project Structure

The project has a modular, scalable design:

```
GTM Lead Scoring Tool/
├── .env.example              # Template for credentials and configurations
├── .gitignore                # Git paths to ignore (data uploads, private files)
├── requirements.txt          # Python library dependencies
├── app.py                    # Streamlit main dashboard entrypoint
├── src/                      # Source package
│   ├── __init__.py           # Package marker
│   ├── config.py             # Configuration loader and Gemini SDK initiator
│   ├── enrichment.py         # AI enrichment query and batch handlers
│   ├── scoring.py            # Rule matching and priority tiering engine
│   └── utils.py              # File import/export and validation utilities
└── data/                     # Data directory for uploads/exports
    └── sample_leads.csv      # Sample leads template for test runs
```

---

## 🛠️ Tech Stack

- **Frontend/Dashboard:** [Streamlit](https://streamlit.io/)
- **Data Engineering:** [Pandas](https://pandas.pydata.org/)
- **AI/LLM:** [Gemini API](https://ai.google.dev/) (via the official `google-generativeai` SDK)
- **Visualizations:** [Plotly Express](https://plotly.com/python/)

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.9** or later installed on your system.

### 2. Clone & Setup Workspace
Navigate to the project directory and create a virtual environment:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows (Command Prompt)
.venv\Scripts\activate.bat
# On Windows (PowerShell)
.venv\Scripts\Activate.ps1
# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
Install all the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to a new file named `.env`:

```bash
cp .env.example .env
```

Open `.env` and configure your settings:
- **`GEMINI_API_KEY`**: Create an API key in [Google AI Studio](https://aistudio.google.com/) and paste it here.
- **`GEMINI_MODEL`**: Keep as `gemini-1.5-flash` or set to `gemini-1.5-pro` for deeper, more analytical profiling.

---

## 🖥️ Running the Application

Launch the Streamlit server from your terminal:

```bash
streamlit run app.py
```

The application will start, and a browser window should automatically open to `http://localhost:8501`.

---

## 💡 How it Works (Workflow)

1. **Upload CSV**: Upload any CSV containing a column of company names (optionally domains as well).
2. **AI Enrichment**: The app uses Gemini to query search info, extract technology stacks, growth signals (funding, hiring), and pain points.
3. **Lead Scoring**: Define your Ideal Customer Profile (ICP) parameters—such as preferred target industries, target company sizes, and key tech stack components—along with weights.
4. **Results Dashboard**: Sort and prioritize leads using visual charts, see metrics on tier segments, and download the enriched, prioritized CSV dataset.
