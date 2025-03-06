# 🔍 Domain Scanner - Domain & DNS Reconnaissance Tool

## 📝 **Tool Description**
**Domain Scanner** allows you to search for domains based on extensions, extract DNS records, and find subdomains. It is useful for security testing and reconnaissance for various domains.

## 🚀 **Features**
- Search for domains by extension (e.g., `.com`, `.net`, `.org`).
- Analyze DNS records of domains.
- Automatically extract subdomains.
- Save all data in text files for later use.

## 📌 **Requirements**
Make sure you have the following tools installed on **Kali Linux** or any distribution supporting Python:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip -y
pip install requests dnspython argparse
```

## 🎯 **How to Use**

### 🔹 Search for Domains by Extension
```bash
python3 domain_scanner.py --search .com
```
Results will be saved in `found_domains.txt`.

### 🔹 Analyze DNS Records for a Specific Domain
```bash
python3 domain_scanner.py --dns example.com
```
Results will be saved in `dns_results.txt`.

### 🔹 Analyze DNS Records from a File
```bash
python3 domain_scanner.py --dns-file domains.txt
```

### 🔹 Search for Subdomains of a Domain
```bash
python3 domain_scanner.py --subdomains example.com
```
Results will be saved in `all_subdomains.txt`.

### 🔹 Automatically Run All Processes
```bash
python3 domain_scanner.py --search .com --all
```
This option collects domains, analyzes their DNS, and searches for subdomains automatically.

## 📂 **Generated Files**
- **`found_domains.txt`** → Contains discovered domains.
- **`dns_results.txt`** → Contains DNS analysis results.
- **`all_subdomains.txt`** → Contains discovered subdomains.

## 🛠 **Contributing & Development**
If you want to improve **Domain Scanner**, you can contribute via GitHub by submitting a **Pull Request** or suggesting improvements through **Issues**.

## 📜 **Legal Disclaimer**
This tool is intended for security testing and learning purposes only. The author is not responsible for any illegal use of this tool.

---

✅ **Ready to explore domains? Get started now with Domain Scanner!** 🚀

## Author

**Mohammed Bakkali**  
_Web Developer_ 