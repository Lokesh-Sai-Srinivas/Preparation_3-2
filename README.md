# 📚 Exam Master

**Exam Master** is a premium, interactive study application built with Streamlit, designed to help university students master complex subjects through "Topper-standard" exam-ready answers.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## ✨ Features

- **🎯 Topper-Standard Content**: Every answer is structured for maximum marks with headings, introductions, bulleted points, and conclusions.
- **📊 Dynamic Visuals**: Automatic rendering of **Graphviz flowcharts** and **Markdown tables** for enhanced conceptual understanding.
- **📐 Specific Marking Schemes**: 
  - **Short Questions**: Optimized for 2 marks (Precise & Illustrated).
  - **Long Questions**: Detailed 10-mark (or 5+5) essay-style responses.
- **🌙 Premium UI**: A sleek, dark-themed interface designed for focused late-night study sessions.
- **📂 Dynamic Content Loading**: Automatically scans the `data/` folder for new subjects and units.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Streamlit

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/exam-master.git
   cd exam-master
   ```

2. **Install dependencies**:
   ```bash
   pip install streamlit
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

---

## 📁 Project Structure

```text
├── app.py              # Main Streamlit application with Custom CSS
├── data/               # Content repository
│   └── Subject Name/   # Category folder
│       └── Unit Name/  # Specific Unit folder
│           ├── Short.json   # 2-Mark Questions
│           └── Long.json    # 10-Mark Questions
└── README.md
```

---

## 🛠️ How to Add Your Own Content

You can easily expand the question bank by following this structure in the `data/` folder:

1. Create a folder for your **Subject**.
2. Create a sub-folder for the **Unit**.
3. Create a `Short.json` or `Long.json` file following this schema:

```json
[
    {
        "q": "Your Question Here?",
        "a": "### Heading\n\n**1. Intro**\nAnswer content...\n\n**2. Conclusion**\nSummary.",
        "graphviz": "digraph G { ... }",
        "table": "| Header | Content |"
    }
]
```

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Created By
**A. Lokesh Sai Srinivas**
