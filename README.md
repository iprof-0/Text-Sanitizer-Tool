# Text Sanitizer Tool 🛡️

A minimal, secure web-based text sanitization tool built with Flask.

This project allows users to remove a specific word from a given text in a **case-insensitive** and **safe** manner, with a clean modern UI.

> "No System is secure"

---

## ✨ Features

- Case-insensitive word removal
- Secure regex handling using `re.escape`
- Modern dark UI
- Copy-to-clipboard functionality
- Input validation & error handling
- Single-file architecture (simple & portable)

---

## 🖥️ Demo

The app automatically opens in your browser after launch:

```
http://127.0.0.1:5000
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/iprof-0/text-Sanitizer.git
cd text-sanitizer
```

### 2. Install [requirements](requirements.txt)
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```

Browser will open automatically.

---

## 🔐 Security Notes

- Uses `re.escape()` to prevent regex injection
- No user input is executed or evaluated
- Designed as a safe text-processing utility
- No external APIs or tracking

---

## 🧠 Architecture Decision

This project intentionally uses a **single-file architecture** for:
- Simplicity
- Fast auditing
- Easy sharing
- Educational clarity

---

## 🚀 Future Improvements (Optional)

- Word boundary matching (`\b`)
- Multiple word removal
- API / JSON mode
- Docker support
- Unit tests

---

## 📜 [License](LICENSE)

MIT License

---

## 👤 [Author](https://iprof-0.github.io/Zero)

[Zero](https://iprof-0.github.io/Zero/#contact) 
Cybersecurity Engineer  
"No System is secure"
