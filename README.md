# 🔍 Xiom — Website & Server Fingerprinting OSINT Tool

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.7+-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
[![GitHub releases](https://img.shields.io/github/release/xdrew87/Xiom.svg)](https://github.com/xdrew87/Xiom/releases/)

**Xiom** is a powerful command-line OSINT reconnaissance tool for website and server fingerprinting. Extract sensitive infrastructure details, server types, SSL certificates, DNS records, and technology stacks from any target URL in seconds.

Perfect for **security researchers**, **penetration testers**, **IT security professionals**, and **threat intelligence analysts**.

## ✨ Key Features

🔧 **Server Identification**
- Detect web server type, version, and configuration
- Identify CMS platforms (WordPress, Drupal, Joomla, etc.)
- Recognize web frameworks (Express, Django, Rails, Laravel, etc.)

🔐 **SSL/TLS Intelligence**
- Certificate details, issuers, and expiration dates
- Cipher suite and protocol version info
- Certificate chain analysis

📡 **DNS & Network Reconnaissance**
- A, AAAA, MX, NS, CNAME, TXT, SOA records
- IP address resolution and reverse lookups
- Nameserver detection

🌐 **HTTP Fingerprinting**
- Server headers and banner grabbing
- Technology stack detection
- Response metadata analysis

📊 **Multiple Output Formats**
- Beautiful colored terminal output (default)
- JSON export for automation and integration
- Detailed text reports

⚙️ **Extensible Configuration**
- API key support for enhanced data sources (VirusTotal, Shodan, AbuseIPDB)
- Custom timeout and retry settings
- Configurable port scanning

## 🚀 Quick Start

### Requirements
- **Python 3.7+**
- **pip** (Python package manager)
- **5 minutes** to set up

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/xdrew87/Xiom.git
   cd Xiom
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Copy config template (optional):**
   ```bash
   cp config.json.template config.json
   # Edit config.json to add API keys for enhanced features
   ```

4. **Run your first scan:**
   ```bash
   python3 xiom.py https://example.com
   ```

Done! 🎉

## 📖 Usage Guide

### Basic Scan
The simplest way to fingerprint a target:

```bash
python3 xiom.py https://example.com
```

### Common Use Cases

**Get JSON output for scripting/automation:**
```bash
python3 xiom.py https://example.com --json > results.json
```

**Verbose mode for debugging issues:**
```bash
python3 xiom.py https://example.com --verbose
```

**Custom config file:**
```bash
python3 xiom.py https://example.com --config custom_config.json
```

**Both HTTP and HTTPS versions:**
```bash
python3 xiom.py example.com  # Auto-detects https
python3 xiom.py http://example.com  # Force http
```

### Example Output

```
╔════════════════════════════════════════════════════════════╗
║                    XIOM FINGERPRINT REPORT                 ║
║                     https://example.com                     ║
╚════════════════════════════════════════════════════════════╝

[✓] SERVER INFORMATION
    Server:           nginx/1.21.0
    Operating System: Linux
    IP Address:       93.184.216.34

[✓] WEB FRAMEWORK
    Framework:        Express.js 4.17.1
    Runtime:          Node.js
    Language:         JavaScript

[✓] SSL/TLS CERTIFICATE
    Issuer:           Let's Encrypt Authority X3
    Valid From:       2023-01-15
    Valid Until:      2024-01-15
    Cipher Suite:     TLS 1.3

[✓] DNS RECORDS
    A Records:        93.184.216.34
    MX Records:       mail.example.com (priority: 10)
    NS Records:       ns1.example.com, ns2.example.com

[✓] OPEN PORTS
    80/tcp   (HTTP)     - Open
    443/tcp  (HTTPS)    - Open
    22/tcp   (SSH)      - Closed
```

## ⚙️ Configuration

### Basic Setup

Copy the template and edit with your settings:

```bash
cp config.json.template config.json
# Edit config.json
```

### config.json Reference

```json
{
  "timeout": 10,
  "verify_ssl": true,
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "api_keys": {
    "virustotal": "YOUR_API_KEY_HERE",
    "shodan": "YOUR_API_KEY_HERE"
  },
  "ports_to_scan": [80, 443, 22, 21, 8080, 8443, 3306, 5432],
  "max_retries": 3,
  "retry_delay": 2
}
```

### API Keys (Optional)

To unlock enhanced features, add API keys to `config.json`:

| Service | Features | How to Get |
|---------|----------|-----------|
| **VirusTotal** | Malware/phishing detection, domain reputation | [virustotal.com/gui](https://virustotal.com/gui) |
| **Shodan** | Open port enumeration, service version details | [shodan.io](https://shodan.io) |
| **AbuseIPDB** | IP reputation and threat data | [abuseipdb.com](https://www.abuseipdb.com) |

**Security Best Practice:** Never commit `config.json` with real API keys!

```bash
# Use environment variables instead
export VIRUSTOTAL_API_KEY="your_key_here"
export SHODAN_API_KEY="your_key_here"
```

Add `config.json` to `.gitignore` (already done).

## 🛡️ Security & Legal Disclaimer

⚠️ **IMPORTANT READ:** Xiom is designed for authorized security testing only.

### Responsible Use
- ✅ Only scan systems you **own or have written permission** to test
- ✅ Respect **rate limits** and API quotas
- ✅ Use for **legitimate security research** and **IT operations**
- ✅ Document and log all scanning activities
- ❌ **Never** scan third-party infrastructure without authorization
- ❌ **Never** use for malicious purposes

**Legal Warning:** Unauthorized computer access is **illegal** in most jurisdictions. Violators may face criminal prosecution and civil liability.

For security issues, see [SECURITY.md](SECURITY.md).

## 🔄 Workflow Example

```bash
# 1. Scan a website
python3 xiom.py https://github.com --json > github_scan.json

# 2. View results
cat github_scan.json | jq .

# 3. Extract specific data
cat github_scan.json | jq '.http.server'

# 4. Process results in your security tool
# (Post to Slack, log to SIEM, store in database, etc.)
```

## 🤝 Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to report bugs
- How to suggest features
- Development setup guide
- Pull request guidelines
- Code style conventions

**Quick start contributing:**

```bash
# 1. Fork the repo on GitHub
# 2. Create a branch for your feature
git checkout -b feature/your-feature

# 3. Make changes and test
python3 xiom.py https://example.com

# 4. Push and open a pull request
git push origin feature/your-feature
```

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for full details.

**TL;DR:** Free to use, modify, and distribute. Include the license in your project.

## 🆘 Support & Issues

- **Bug Reports:** [GitHub Issues](https://github.com/xdrew87/Xiom/issues)
- **Feature Requests:** [GitHub Issues - Feature Label](https://github.com/xdrew87/Xiom/issues?q=label%3Aenhancement)
- **Security Vulnerabilities:** See [SECURITY.md](SECURITY.md) for responsible disclosure
- **Questions?** Open an issue with the `question` label

## 🗺️ Roadmap

- [ ] Batch mode (scan multiple URLs from file)
- [ ] Export to PDF/HTML reports
- [ ] GUI version (Tkinter)
- [ ] Automated scanning schedules
- [ ] Custom fingerprint rules
- [ ] REST API for integration
- [ ] Subdomain enumeration
- [ ] Technology database updates

## 🔗 Links

- **GitHub:** https://github.com/xdrew87/Xiom
- **Author:** [@xdrew87](https://github.com/xdrew87)
- **Issues:** [Report a bug](https://github.com/xdrew87/Xiom/issues)
- **License:** [MIT](LICENSE)

---

**Built with ❤️ for security researchers, penetration testers, and IT professionals.**

*Stay curious. Stay ethical. Happy hunting! 🔍*
