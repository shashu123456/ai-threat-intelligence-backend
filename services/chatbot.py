def ask_security_bot(question):

    q = question.lower()

    if "phishing" in q:

        return "Phishing is a cyber attack where attackers trick users into revealing sensitive information."

    if "safe" in q:

        return "Check domain age, HTTPS, suspicious keywords and redirects."

    if "attack" in q:

        return "Attack detected using machine learning URL analysis."

    if "prevent" in q:

        return "Always verify URLs, enable MFA and avoid clicking unknown links."

    return "Cyber security assistant ready."