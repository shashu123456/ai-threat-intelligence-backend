"""
Intelligent rule-based chatbot engine for the CyberShield CTI platform.
Handles phishing education, IP/URL analysis explanations, risk queries,
and general cybersecurity guidance.
"""

import re
from typing import Dict, Any


class ChatbotEngine:
    def __init__(self):
        self._rules = self._build_rules()

    def respond(self, message: str, context: Dict[str, Any] = None) -> str:
        context = context or {}
        text = message.lower().strip()

        # Context-aware responses (use last scan result if available)
        last_scan = context.get("last_scan", {})

        for pattern, handler in self._rules:
            if re.search(pattern, text):
                return handler(text, last_scan)

        return self._default_response(text)

    # ── Rule builder ───────────────────────────────────────────────────────────

    def _build_rules(self):
        return [
            # Greetings
            (r"\b(hi|hello|hey|howdy|greetings)\b", self._greet),
            # Help
            (r"\b(help|what can you do|capabilities|commands)\b", self._help),
            # Phishing education
            (r"\b(what is phishing|explain phishing|phishing meaning)\b", self._explain_phishing),
            (r"\b(how (to |do i )?(detect|identify|spot) phishing)\b", self._detect_phishing),
            (r"\b(phishing (examples?|types?|kinds?))\b", self._phishing_types),
            # Risk score
            (r"\b(risk score|what (does|is) (the )?risk|score mean)\b", self._explain_risk),
            (r"\b(high risk|critical|dangerous url|malicious)\b", self._high_risk_advice),
            # IP / domain
            (r"\b(ip address|what (is|are) ip|ip lookup|abuseipdb)\b", self._explain_ip),
            (r"\b(domain|tld|top.level domain|suspicious domain)\b", self._explain_domain),
            # SSL / HTTPS
            (r"\b(ssl|https|certificate|secure connection|tls)\b", self._explain_ssl),
            # URL shorteners
            (r"\b(short(en|ened|ener)?|bit\.ly|tinyurl|url (shortener|short))\b", self._explain_shorteners),
            # Machine learning
            (r"\b(ml|machine learning|ai|model|algorithm|random forest|how (does|do) (it|you) work)\b", self._explain_ml),
            # VT / threat intel
            (r"\b(virustotal|virus total|threat intel|threat feed|abuseipdb)\b", self._explain_threat_intel),
            # Last scan result
            (r"\b(last scan|my scan|scan result|what did you find|analysis)\b", self._last_scan_summary),
            # Safe browsing tips
            (r"\b(stay safe|protect|tips|best practices|how to be safe)\b", self._safety_tips),
            # Current threat landscape
            (r"\b(current threats?|latest attacks?|trending|news)\b", self._threat_landscape),
            # Entropy
            (r"\b(entropy|random domain|gibberish)\b", self._explain_entropy),
        ]

    # ── Handlers ───────────────────────────────────────────────────────────────

    def _greet(self, msg, ctx):
        return (
            "👋 Hey! I'm **CyberShield AI** — your threat intelligence assistant. "
            "I can explain scan results, teach you about phishing, break down risk scores, "
            "and guide you through cyber threats. What would you like to know?"
        )

    def _help(self, msg, ctx):
        return (
            "**Here's what I can help with:**\n\n"
            "🔍 **Scan Analysis** — Ask me about your last scan result\n"
            "🎣 **Phishing** — What it is, how to detect it, common types\n"
            "📊 **Risk Scores** — What scores mean and what to do\n"
            "🌐 **IP & Domains** — IP reputation, suspicious TLDs, entropy\n"
            "🔒 **HTTPS/SSL** — Why it matters and its limits\n"
            "🤖 **ML Model** — How the AI engine works\n"
            "🛡 **Safety Tips** — Best practices to stay protected\n\n"
            "Just type your question naturally!"
        )

    def _explain_phishing(self, msg, ctx):
        return (
            "**Phishing** is a cyberattack where criminals impersonate trusted entities "
            "(banks, tech companies, government agencies) to trick you into revealing "
            "sensitive data like passwords, credit card numbers, or personal information.\n\n"
            "**How it works:**\n"
            "1. Attacker registers a lookalike domain (e.g., `paypa1.com` vs `paypal.com`)\n"
            "2. Sends convincing emails/messages with urgent language\n"
            "3. Victim clicks the link and lands on a fake site\n"
            "4. Victim enters credentials → attacker captures them\n\n"
            "**Key stat:** Phishing accounts for **36% of all data breaches** (Verizon DBIR 2023)."
        )

    def _detect_phishing(self, msg, ctx):
        return (
            "**How to detect phishing URLs:**\n\n"
            "🔴 **Urgent red flags:**\n"
            "• URL uses an IP address instead of a domain (`[192.168.1.1](http://192.168.1.1/paypal)`)\n"
            "• `@` symbol in URL (browser ignores everything before it)\n"
            "• Free/suspicious TLD: `.tk`, `.ml`, `.xyz`, `.top`\n"
            "• URL shortener hiding the real destination\n"
            "• Brand name in subdomain, not domain (`paypal.fakehacker.com`)\n\n"
            "🟡 **Warning signs:**\n"
            "• HTTP instead of HTTPS\n"
            "• Misspelled brands (`amaz0n`, `microsofft`)\n"
            "• Excessive hyphens or random-looking domain\n"
            "• Unusually long URL with many parameters\n\n"
            "Always use CyberShield to scan suspicious links before clicking!"
        )

    def _phishing_types(self, msg, ctx):
        return (
            "**Common Phishing Attack Types:**\n\n"
            "🎣 **Phishing** — Mass emails targeting many victims\n"
            "🎯 **Spear Phishing** — Targeted, personalized attacks on specific individuals\n"
            "🐋 **Whaling** — Targets C-suite executives (CEO fraud)\n"
            "📱 **Smishing** — Phishing via SMS text messages\n"
            "📞 **Vishing** — Voice phishing via phone calls\n"
            "🖥 **Clone Phishing** — Duplicates legitimate emails with malicious links\n"
            "🌐 **Pharming** — Redirects DNS queries to fake websites\n"
            "👤 **Angler Phishing** — Fake customer service on social media"
        )

    def _explain_risk(self, msg, ctx):
        return (
            "**Risk Score (0–100):**\n\n"
            "The score is calculated from two components:\n\n"
            "**ML Probability (60%)** — RandomForest model trained on URL features "
            "(length, entropy, special characters, TLD reputation)\n\n"
            "**Heuristic Rules (40%)** — Bonus points for confirmed red flags:\n"
            "• Raw IP in URL → +15\n"
            "• `@` symbol → +10\n"
            "• Suspicious TLD → +10\n"
            "• URL shortener → +8\n"
            "• Brand keyword abuse → +7\n"
            "• No HTTPS → +5\n\n"
            "**Severity thresholds:**\n"
            "🟢 0–39: Low | 🟡 40–59: Medium | 🟠 60–79: High | 🔴 80–100: Critical"
        )

    def _high_risk_advice(self, msg, ctx):
        return (
            "🚨 **High Risk URL Detected — Immediate Actions:**\n\n"
            "1. **Do NOT visit** the URL under any circumstances\n"
            "2. **Do NOT enter** any credentials or personal info\n"
            "3. If you've already visited it:\n"
            "   • Change passwords for any related accounts immediately\n"
            "   • Enable 2FA on those accounts\n"
            "   • Run a malware scan on your device\n"
            "   • Check for unauthorized account activity\n"
            "4. **Report it:**\n"
            "   • Google Safe Browsing: `safebrowsing.google.com/safebrowsing/report_phish`\n"
            "   • PhishTank: `phishtank.com`\n"
            "   • Anti-Phishing Working Group: `reportphishing@apwg.org`"
        )

    def _explain_ip(self, msg, ctx):
        return (
            "**IP Address Analysis:**\n\n"
            "When a URL uses a raw IP instead of a domain name, it's a major red flag — "
            "legitimate services almost never do this.\n\n"
            "**What AbuseIPDB checks:**\n"
            "• Reports from security researchers worldwide\n"
            "• Categories: port scanning, brute force, web spam, phishing, DDoS\n"
            "• Abuse confidence score (0–100)\n\n"
            "**Abuse Confidence Score:**\n"
            "🟢 0–10: Clean | 🟡 11–25: Low | 🟠 26–75: Suspicious | 🔴 76–100: Malicious\n\n"
            "Even a 'clean' IP can host phishing — always combine with ML and URL analysis."
        )

    def _explain_domain(self, msg, ctx):
        return (
            "**Domain & TLD Analysis:**\n\n"
            "**High-risk free TLDs** used overwhelmingly in attacks:\n"
            "`.tk` `.ml` `.ga` `.cf` `.gq` (Freenom free domains)\n"
            "`.xyz` `.top` `.club` `.online` `.site` `.buzz`\n\n"
            "**Subdomain abuse** — Attackers exploit trusted brands:\n"
            "`paypal.com.account-verify.tk` ← `.tk` is the actual TLD, not PayPal!\n\n"
            "**Domain entropy** measures how 'random' a domain looks. "
            "Legitimate domains: `github.com` (entropy ≈ 2.9). "
            "DGA malware domains: `xkqzpfvmr.net` (entropy ≈ 3.9+).\n\n"
            "High entropy often means domain generation algorithm (DGA) malware."
        )

    def _explain_ssl(self, msg, ctx):
        return (
            "**HTTPS / SSL / TLS:**\n\n"
            "HTTPS encrypts traffic between you and the server — it prevents "
            "eavesdropping and man-in-the-middle attacks.\n\n"
            "⚠️ **Common misconception:** HTTPS does NOT mean a site is legitimate!\n"
            "Phishing sites can (and do) use valid SSL certificates. "
            "In 2023, **83% of phishing sites used HTTPS** (APWG report).\n\n"
            "**What HTTPS guarantees:**\n"
            "✅ Encrypted connection\n"
            "✅ Server identity verification (domain match)\n\n"
            "**What HTTPS does NOT guarantee:**\n"
            "❌ The site isn't malicious\n"
            "❌ Your data won't be stolen (if the site is fake)\n\n"
            "Always verify the domain, not just the padlock icon."
        )

    def _explain_shorteners(self, msg, ctx):
        return (
            "**URL Shorteners & Why They're Dangerous:**\n\n"
            "Services like `bit.ly`, `tinyurl.com`, and `t.co` are heavily abused "
            "in phishing campaigns because they:\n"
            "• Completely hide the destination URL\n"
            "• Bypass email security filters\n"
            "• Can redirect to different URLs after clicking\n\n"
            "**How to safely preview shortened URLs:**\n"
            "• Add `+` to bit.ly links: `bit.ly/abc123+`\n"
            "• Use `checkshorturl.com` or `unshorten.it`\n"
            "• Or just scan it here with CyberShield first! 🛡\n\n"
            "If you receive an unsolicited shortened URL — treat it as suspicious."
        )

    def _explain_ml(self, msg, ctx):
        return (
            "**How CyberShield's AI Engine Works:**\n\n"
            "**Model:** Random Forest Classifier (200 trees, max depth 12)\n\n"
            "**Features extracted from each URL (30 total):**\n"
            "• Length signals: URL length, domain length, path depth\n"
            "• Character signals: dots, hyphens, `@`, `?`, `=`, `%` encoding\n"
            "• Structural signals: HTTPS, IP usage, port number, subdomains\n"
            "• Semantic signals: brand keyword abuse, shortener detection\n"
            "• Entropy signals: domain randomness score\n\n"
            "**Pipeline:**\n"
            "`URL` → `Feature Extraction` → `RandomForest` → `Probability`\n"
            "→ `Heuristic Scoring` → `Risk Score (0–100)`\n\n"
            "The model is augmented by Google Safe Browsing, AbuseIPDB, "
            "and VirusTotal for a multi-layered defense approach."
        )

    def _explain_threat_intel(self, msg, ctx):
        return (
            "**Threat Intelligence Integrations:**\n\n"
            "🔍 **Google Safe Browsing** — Checks against Google's database of "
            "4 billion+ unsafe URLs updated every 30 minutes\n\n"
            "🔍 **AbuseIPDB** — Community-reported IP abuse database with "
            "100M+ reports from security researchers globally\n\n"
            "🔍 **VirusTotal** — Scans URLs against 70+ antivirus engines and "
            "URL scanners simultaneously\n\n"
            "CyberShield combines all three with its own ML model for a "
            "defense-in-depth approach — no single feed is 100% complete."
        )

    def _last_scan_summary(self, msg, ctx):
        if not ctx:
            return (
                "No recent scan found in this session. "
                "Use the URL Scanner to analyze a link and I'll explain the results!"
            )
        risk = ctx.get("risk_score", 0)
        pred = ctx.get("prediction", "unknown")
        url = ctx.get("url", "the URL")
        explanation = ctx.get("explanation", "")
        geo = ctx.get("geo_data", {})
        country = geo.get("country", "Unknown")
        ip = ctx.get("ip_address", "Unknown")

        status_emoji = "🚨" if pred == "phishing" else "✅"
        return (
            f"{status_emoji} **Last Scan Summary:**\n\n"
            f"**URL:** `{url}`\n"
            f"**Verdict:** {pred.upper()}\n"
            f"**Risk Score:** {risk}/100\n"
            f"**Origin:** {country} ({ip})\n\n"
            f"**Analysis:** {explanation}\n\n"
            + (
                "⚠️ I strongly recommend **not visiting** this URL."
                if pred == "phishing"
                else "✅ URL appears safe based on current analysis."
            )
        )

    def _safety_tips(self, msg, ctx):
        return (
            "**Cybersecurity Best Practices:**\n\n"
            "🔐 **Authentication**\n"
            "• Use a password manager (Bitwarden, 1Password)\n"
            "• Enable TOTP-based 2FA everywhere\n"
            "• Never reuse passwords\n\n"
            "🌐 **Browsing**\n"
            "• Scan suspicious links with CyberShield before clicking\n"
            "• Verify URLs carefully — check the actual domain\n"
            "• Don't trust urgency-based messages (\"Act now!\")\n\n"
            "📧 **Email**\n"
            "• Verify sender domain, not just display name\n"
            "• Never open unexpected attachments\n"
            "• When in doubt, call the company directly\n\n"
            "💻 **Device**\n"
            "• Keep OS and software updated\n"
            "• Use a reputable endpoint security solution\n"
            "• Use a VPN on public WiFi"
        )

    def _threat_landscape(self, msg, ctx):
        return (
            "**Current Cyber Threat Landscape (2024):**\n\n"
            "📈 **Top attack vectors:**\n"
            "1. Phishing (36% of breaches) — still the #1 initial access method\n"
            "2. Credential stuffing — automated login attacks using leaked passwords\n"
            "3. Supply chain attacks — targeting software dependencies\n"
            "4. Ransomware-as-a-Service — LockBit, ALPHV/BlackCat\n"
            "5. AI-generated deepfake phishing — hyper-personalized attacks\n\n"
            "🌍 **Most targeted sectors:**\n"
            "Finance, Healthcare, Government, Education, Critical Infrastructure\n\n"
            "🔴 **Emerging threats:**\n"
            "• QR code phishing ('quishing')\n"
            "• MFA fatigue attacks\n"
            "• Adversary-in-the-middle (AiTM) proxies bypassing 2FA\n\n"
            "Stay updated: `cisa.gov/alerts`, `threatpost.com`, `bleepingcomputer.com`"
        )

    def _explain_entropy(self, msg, ctx):
        return (
            "**Domain Entropy Explained:**\n\n"
            "Entropy measures the 'randomness' or unpredictability of characters "
            "in a string, using Shannon entropy (bits per character).\n\n"
            "**Formula:** H = -Σ p(x) × log₂(p(x))\n\n"
            "**Real examples:**\n"
            "• `google.com` → entropy ≈ 2.75 (predictable, human-readable)\n"
            "• `github.com` → entropy ≈ 2.92\n"
            "• `xkqzpfvmr.net` → entropy ≈ 3.95 (random — DGA malware pattern)\n\n"
            "**Why it matters:**\n"
            "Malware uses Domain Generation Algorithms (DGA) to generate thousands "
            "of random domain names as C2 fallbacks. High entropy (>3.5) is a "
            "strong indicator of DGA or automated domain registration abuse."
        )

    def _default_response(self, msg):
        return (
            "I'm not sure I understood that — I'm specialized in cybersecurity topics. "
            "Try asking about:\n\n"
            "• **Phishing** — 'What is phishing?'\n"
            "• **Risk scores** — 'What does the risk score mean?'\n"
            "• **Your last scan** — 'Explain my scan result'\n"
            "• **Safety tips** — 'How can I stay safe online?'\n"
            "• **How it works** — 'How does the AI model work?'\n\n"
            "Type `help` for a full list of topics."
        )
