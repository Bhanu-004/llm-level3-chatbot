#  Level 3: LLM Agent Chatbot

A smart, multi-tool chatbot powered by Google's Gemini API.  
This agent supports natural language queries with step-by-step task execution — including math calculations, German translation, and factual lookup.

---

##  Features

- Multi-step Task Handling
- Calculator Tool (basic arithmetic)
- Translator Tool (English → German)
- Knowledge Queries (e.g., capital cities)
- GUI Chat Interface (built with Tkinter)
- Interaction Logging (`.txt` and `.json`)

---

##  Tools Used

- `google.generativeai` (Gemini 1.5 Flash)
- `GoogleTranslator` for translation
- Custom `calculator_tool.py`
- `tkinter` for GUI
- Python 3.10+

---

##  File Structure
├── full_agent_gui.py # Main chatbot logic
├── calculator_tool.py # Math operation handler
├── translator_tool.py # Text translation (to German)
├── interaction_logs.txt # Chat log (plaintext)
├── interaction_logs.json # Chat log (structured)
