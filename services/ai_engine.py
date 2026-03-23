"""
AI Engine — URL feature extraction + phishing prediction.

Training: if phishing_model.pkl is missing the engine auto-trains a
RandomForest on a compact built-in dataset so the app always works.
"""

import os
import re
import math
import pickle
import socket
import hashlib
import logging
from urllib.parse import urlparse
from typing import Dict, Tuple

import numpy as np

logger = logging.getLogger(__name__)

# ── Feature constants ──────────────────────────────────────────────────────────
SUSPICIOUS_TLDS = {
    ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".club",
    ".online", ".site", ".info", ".biz", ".buzz", ".work",
}

BRAND_KEYWORDS = {
    "paypal", "amazon", "apple", "microsoft", "google", "facebook",
    "instagram", "netflix", "bank", "secure", "account", "login",
    "verify", "update", "confirm", "signin", "ebay", "wellsfargo",
    "chase", "citibank", "usps", "fedex", "dhl",
}

SHORTENERS = {
    "bit.ly", "tinyurl.com", "goo.gl", "ow.ly", "t.co",
    "is.gd", "buff.ly", "rebrand.ly", "short.io",
}

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "phishing_model.pkl")


class AIEngine:
    def __init__(self):
        self.model = self._load_or_train_model()

    # ── Public API ─────────────────────────────────────────────────────────────

    def extract_features(self, url: str) -> Dict[str, float]:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace("www.", "")
        path = parsed.path
        full = url.lower()

        features: Dict[str, float] = {
            # Length-based
            "url_length": len(url),
            "domain_length": len(domain),
            "path_length": len(path),
            "num_subdomains": domain.count("."),
            # Character-based
            "num_dots": url.count("."),
            "num_hyphens": url.count("-"),
            "num_underscores": url.count("_"),
            "num_slashes": url.count("/"),
            "num_at": url.count("@"),
            "num_question": url.count("?"),
            "num_equals": url.count("="),
            "num_ampersand": url.count("&"),
            "num_percent": url.count("%"),
            "num_digits": sum(c.isdigit() for c in url),
            # Boolean indicators (0/1)
            "has_ip": float(self._is_ip_address(domain)),
            "has_https": float(url.startswith("https://")),
            "has_at_symbol": float("@" in url),
            "has_double_slash": float("//" in path),
            "has_port": float(bool(parsed.port)),
            "is_shortened": float(domain in SHORTENERS),
            "has_brand_keyword": float(self._contains_brand(full, domain)),
            "has_suspicious_tld": float(self._has_suspicious_tld(domain)),
            "has_hex_encoding": float("%2f" in full or "%2e" in full),
            "has_data_uri": float(url.lower().startswith("data:")),
            # Entropy
            "domain_entropy": self._entropy(domain),
            "path_entropy": self._entropy(path),
            # Query string
            "query_length": len(parsed.query),
            "num_query_params": len(parsed.query.split("&")) if parsed.query else 0,
            # Ratio
            "digit_ratio": sum(c.isdigit() for c in domain) / max(len(domain), 1),
            "special_char_ratio": sum(
                not c.isalnum() for c in url
            ) / max(len(url), 1),
        }
        return features

    def predict(
        self, url: str, features: Dict[str, float]
    ) -> Tuple[str, float, float, str]:
        """Returns (prediction, confidence, risk_score, explanation)."""
        feature_vector = np.array(list(features.values())).reshape(1, -1)

        proba = self.model.predict_proba(feature_vector)[0]
        phishing_prob = float(proba[1])
        prediction = "phishing" if phishing_prob >= 0.5 else "safe"
        confidence = max(proba)

        risk_score = self._calculate_risk_score(features, phishing_prob)
        explanation = self._generate_explanation(url, features, prediction, risk_score)

        return prediction, confidence, risk_score, explanation

    # ── Model management ───────────────────────────────────────────────────────

    def _load_or_train_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    model = pickle.load(f)
                logger.info("Loaded existing phishing model.")
                return model
            except Exception as e:
                logger.warning(f"Failed to load model ({e}), retraining...")

        return self._train_fallback_model()

    def _train_fallback_model(self):
        """Train a minimal RandomForest on a hand-crafted balanced dataset."""
        from sklearn.ensemble import RandomForestClassifier

        safe_urls = [
            "[google.com](https://www.google.com/search?q=hello)",
            "[github.com](https://github.com/openai/gpt-4)",
            "[stackoverflow.com](https://stackoverflow.com/questions/1)",
            "[wikipedia.org](https://www.wikipedia.org/wiki/Python)",
            "[docs.python.org](https://docs.python.org/3/library/os.html)",
            "[amazon.com](https://www.amazon.com/dp/B09G3HRMVB)",
            "[mail.google.com](https://mail.google.com/mail/u/0/)",
            "[linkedin.com](https://www.linkedin.com/in/johndoe)",
            "[news.ycombinator.com](https://news.ycombinator.com/item?id=1234)",
            "[reddit.com](https://www.reddit.com/r/python/)",
            "[medium.com](https://medium.com/@user/article)",
            "[youtube.com](https://www.youtube.com/watch?v=abc123)",
            "[twitter.com](https://twitter.com/openai)",
            "[flask.palletsprojects.com](https://flask.palletsprojects.com/en/2.0.x/)",
            "[pytorch.org](https://pytorch.org/tutorials/beginner/blitz/cifar10.html)",
        ]
        phishing_urls = [
            "[paypa1-secure-login.tk](http://paypa1-secure-login.tk/verify?account=true)",
            "[192.168.1.1](http://192.168.1.1/amazon-login/update)",
            "[secure-apple-id.gq](http://secure-apple-id.gq/signin&redirect=phish)",
            "[bit.ly](http://bit.ly/3xPhIsH)",
            "[amaz0n-account-suspended.xyz](http://amaz0n-account-suspended.xyz/login)",
            "[microsofft-secure.online](http://microsofft-secure.online/office365)",
            "[go0gle-verify.cf](http://go0gle-verify.cf/accounts/login?continue=phish)",
            "[facebook-security-check.ml](http://facebook-security-check.ml/checkpoint)",
            "[update-your-bank-account.biz](http://update-your-bank-account.biz/hsbc)",
            "[netf1ix-billing.top](http://netf1ix-billing.top/update-payment)",
            "[appleid-locked.work](http://appleid-locked.work/unlock?token=abc)",
            "[secure.paypal.account-verify.ga](http://secure.paypal.account-verify.ga/signin)",
            "[chase-bank-alert.tk](http://chase-bank-alert.tk/review?case=3332)",
            "[instagram-login-confirm.xyz](http://instagram-login-confirm.xyz/2fa)",
            "[verify-wellsfargo-login.club](http://verify-wellsfargo-login.club/secure)",
        ]

        all_urls = safe_urls + phishing_urls
        labels = [0] * len(safe_urls) + [1] * len(phishing_urls)

        X = np.array([
            list(self.extract_features(u).values()) for u in all_urls
        ])
        y = np.array(labels)

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_split=2,
            random_state=42,
            class_weight="balanced",
        )
        model.fit(X, y)

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)

        logger.info("Trained and saved fallback phishing model.")
        return model

    # ── Scoring ────────────────────────────────────────────────────────────────

    def _calculate_risk_score(
        self, features: Dict[str, float], ml_prob: float
    ) -> float:
        score = ml_prob * 60  # ML contributes 60 points max

        # Heuristic bonus points
        if features["has_ip"]:
            score += 15
        if features["has_at_symbol"]:
            score += 10
        if features["is_shortened"]:
            score += 8
        if features["has_suspicious_tld"]:
            score += 10
        if features["has_brand_keyword"]:
            score += 7
        if features["url_length"] > 100:
            score += 5
        if features["domain_entropy"] > 3.5:
            score += 5
        if features["has_port"]:
            score += 5
        if features["has_https"] == 0:
            score += 5

        return min(round(score, 2), 100.0)

    def _generate_explanation(
        self,
        url: str,
        features: Dict[str, float],
        prediction: str,
        risk_score: float,
    ) -> str:
        reasons = []

        if features["has_ip"]:
            reasons.append("URL uses a raw IP address instead of a domain name")
        if features["has_at_symbol"]:
            reasons.append("'@' symbol present — browser ignores everything before it")
        if features["is_shortened"]:
            reasons.append("URL shortener detected — masks the true destination")
        if features["has_suspicious_tld"]:
            reasons.append("Domain uses a high-risk free TLD (e.g., .tk, .xyz, .ml)")
        if features["has_brand_keyword"]:
            parsed = urlparse(url)
            reasons.append(
                f"Brand impersonation keyword detected in URL structure"
            )
        if not features["has_https"]:
            reasons.append("No HTTPS — connection is unencrypted")
        if features["url_length"] > 100:
            reasons.append(f"Unusually long URL ({int(features['url_length'])} chars)")
        if features["domain_entropy"] > 3.5:
            reasons.append(
                f"High domain entropy ({features['domain_entropy']:.2f}) — "
                "suggests randomly generated domain"
            )
        if features["has_port"]:
            reasons.append("Non-standard port detected in URL")
        if features["num_subdomains"] > 3:
            reasons.append(
                f"Excessive subdomain depth ({int(features['num_subdomains'])})"
            )

        if not reasons:
            if prediction == "safe":
                return "No significant threat indicators detected. URL appears legitimate."
            reasons.append("ML model flagged statistical anomalies in URL structure")

        prefix = (
            f"⚠ THREAT DETECTED (Risk: {risk_score:.0f}/100). "
            if prediction == "phishing"
            else f"ℹ Low-risk indicators noted (Score: {risk_score:.0f}/100). "
        )
        return prefix + " | ".join(reasons) + "."

    # ── Feature helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _is_ip_address(domain: str) -> bool:
        try:
            socket.inet_aton(domain.split(":")[0])
            return True
        except OSError:
            return False

    @staticmethod
    def _contains_brand(full_url: str, domain: str) -> bool:
        for brand in BRAND_KEYWORDS:
            if brand in full_url:
                # Not a threat if the brand IS the domain (e.g., paypal.com)
                if not (domain == f"{brand}.com" or domain.endswith(f".{brand}.com")):
                    return True
        return False

    @staticmethod
    def _has_suspicious_tld(domain: str) -> bool:
        return any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS)

    @staticmethod
    def _entropy(s: str) -> float:
        if not s:
            return 0.0
        freq = {}
        for c in s:
            freq[c] = freq.get(c, 0) + 1
        length = len(s)
        return -sum((f / length) * math.log2(f / length) for f in freq.values())
