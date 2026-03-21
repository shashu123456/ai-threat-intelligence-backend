from services.threat_feed import check_openphish
from services.reputation_service import check_reputation

def calculate_threat_score(url):
    score = 0

    if check_openphish(url):
        score += 50

    reputation = check_reputation(url)
    score += reputation

    return min(score, 100)