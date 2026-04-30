# 🚀 urlshort — Clean Recon Grouper

`urlshort` is a powerful CLI tool for parsing, filtering, and grouping URLs from recon outputs like **dirsearch** and **httpx** into meaningful clusters.

It helps you quickly identify patterns, duplicates, and interesting endpoints during reconnaissance.

---

## 📂 Project File

* Main script: 

---

## ✨ Features

* 🔍 Parse multiple formats (dirsearch, httpx, raw logs)
* 🧠 Smart grouping modes:

  * `root`
  * `server`
  * `file`
  * `path`
* 🎯 Advanced filtering:

  * Status code
  * Title
  * Server
  * Content length / size
  * File extension
* 🎨 Colored output (optional)
* 📥 Supports:

  * File input
  * STDIN piping
* 💾 Save results to file

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/urlshort.git
cd urlshort
chmod +x urlshort.py
```

---

## 🚀 Usage

### Basic usage

```bash
python3 urlshort.py -l urls.txt
```

### Using STDIN

```bash
cat urls.txt | python3 urlshort.py
```

---

## 🔧 Options

| Option         | Description                                        |
| -------------- | -------------------------------------------------- |
| `-l, --list`   | Input file(s)                                      |
| `-o`           | Save output to file                                |
| `--group-mode` | Grouping method (`root`, `server`, `file`, `path`) |
| `--no-color`   | Disable colored output                             |

### 🎯 Filters

| Option | Description                            |
| ------ | -------------------------------------- |
| `-sc`  | Filter by status code (e.g. `200,403`) |
| `-ml`  | Match title                            |
| `-ms`  | Match server                           |
| `-mc`  | Match content length                   |
| `-msz` | Match size                             |
| `-ext` | Filter by extension (`php,js,json`)    |

---

## 🧪 Examples

### Group by server

```bash
python3 urlshort.py -l urls.txt --group-mode server
```

### Filter only 200 responses

```bash
python3 urlshort.py -l urls.txt -sc 200
```

### Find only `.js` files

```bash
python3 urlshort.py -l urls.txt -ext js
```

### Save output

```bash
python3 urlshort.py -l urls.txt -o result.txt
```

---

## 🧠 How It Works

* Extracts URLs using regex
* Parses metadata:

  * Status
  * Content length
  * Title
  * Server
* Applies filters
* Groups URLs based on selected mode
* Outputs sorted clusters by size

---

## 📊 Grouping Modes Explained

| Mode     | Description                |
| -------- | -------------------------- |
| `root`   | All URLs in one group      |
| `server` | Group by server header     |
| `file`   | Group by filename + size   |
| `path`   | Group by last path segment |

---

## 🎨 Example Output

```
### nginx (12)
https://example.com/admin
https://example.com/login

### apache (5)
https://test.com/api
```

---

## 🛠️ Requirements

* Python 3.x

No external dependencies required 🎉

---

## ⚠️ Notes

* Handles messy recon output gracefully
* Ignores invalid lines automatically
* Designed for speed and large datasets

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---
