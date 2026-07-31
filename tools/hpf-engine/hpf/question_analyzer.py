# Question Analyzer
# Routes a question to a reasoning mode and extracts roles and entities.

import re

MODE_SIGNALS = {
    "decide": [
        r"\bshould i\b", r"\bis it a good (idea|choice|move)\b",
        r"\bwhat should (i|we)\b", r"\brecommend\b",
        r"\bwhat.s the best\b", r"\bought (i|we) to\b",
    ],
    "compare": [
        r"\bdifference\b", r"\bvs\b", r"\bversus\b",
        r"\bcompare\b", r"\bwhich is better\b",
        r"\bwhich (one|should) (i|we)\b",
    ],
    "troubleshoot": [
        r"\bbroken\b", r"\bfailing\b", r"\bcrash\b",
        r"\berror\b", r"\bdoesn't work\b", r"\bdoes not work\b",
        r"\bwhy (do|does|is|are|can't|didn't)\b",
        r"\bnot working\b", r"\bfix\b",
    ],
    "explain": [
        r"\bwhat is\b", r"\bwhat are\b",
        r"\bhow does\b", r"\bhow do\b",
        r"\btell me about\b", r"\bexplain\b",
        r"\bdefine\b", r"\bwhat.*mean\b",
    ],
    "design": [
        r"\bdesign\b", r"\bimplement\b",
        r"\bhow should (i|we)\b",
        r"\barchitecture\b", r"\bbuild\b",
        r"\bcreate a\b",
    ],
}

MODE_PRIORITY = ["decide", "compare", "troubleshoot", "explain", "design"]

ROLE_PATTERNS = [
    (r"\bprotocol\b", "protocol"),
    (r"\bframework\b", "framework"),
    (r"\btool\b", "tool"),
    (r"\blibrary\b", "library"),
    (r"\bpattern\b", "pattern"),
    (r"\bprinciple\b", "principle"),
    (r"\bconcept\b", "concept"),
    (r"\bstrategy\b", "strategy"),
    (r"\barchitecture\b", "architecture"),
    (r"\bdesign\b", "design"),
    (r"\bsession\b", "session"),
    (r"\bdetection\b", "detection"),
    (r"\bextraction\b", "extraction"),
    (r"\bselector\b", "selector"),
    (r"\bhealth\b", "health"),
    (r"\bprofile\b", "profile"),
    (r"\bmigration\b", "migration"),
    (r"\bautomation\b", "automation"),
]

KNOWN_ENTITIES = [
    "cdp", "chrome devtools protocol", "devtools protocol",
    "webdriver", "w3c webdriver",
    "nodriver", "selenium", "playwright", "puppeteer",
    "retry", "backoff", "circuit breaker",
    "selector", "data-testid", "xpath", "css selector",
    "anti-detection", "fingerprinting", "bot detection",
    "browser profile", "session", "browser profiles",
    "health check", "session lifecycle", "session management",
    "incremental extraction", "data extraction", "scraper", "scraping",
    "proxy", "rotation", "captcha",
    "self-healing", "resilient", "download pipeline", "production pipeline",
    "migrate", "migration",
    "browser", "crash", "navigation", "navigations",
    "multiple navigations", "blocked", "gets blocked",
    "expire", "expiration",
]


def extract_entities(question):
    entities = []
    q = question.lower()
    for entity in KNOWN_ENTITIES:
        if entity in q:
            entities.append(entity)

    # Dynamic entity extraction from question words
    words = q.split()
    for i, word in enumerate(words):
        word = word.strip("?,.;:!\"'")
        if not word or len(word) < 3:
            continue
        if word in ("the", "and", "for", "are", "not", "but", "why", "how", "what", "does"):
            continue
        if word.endswith("ing") or word.endswith("ion"):
            if word not in entities:
                entities.append(word)

    return entities


def extract_roles(question):
    roles = []
    q = question.lower()
    for pattern, role in ROLE_PATTERNS:
        if re.search(pattern, q):
            if role not in roles:
                roles.append(role)
    return roles


def detect_mode(question):
    q = question.lower()
    matched = {}
    for mode in MODE_PRIORITY:
        for pattern in MODE_SIGNALS[mode]:
            if re.search(pattern, q):
                matched[mode] = True
                break

    # Explanatory "why" (e.g., "Why do browser profiles matter?")
    if "troubleshoot" in matched:
        explanatory_markers = ["matter", "important", "benefit", "advantage", "purpose"]
        for marker in explanatory_markers:
            if marker in q:
                matched.pop("troubleshoot", None)
                matched["explain"] = True
                break

    for mode in MODE_PRIORITY:
        if mode in matched:
            return mode
    return "explain"


def analyze(question):
    return {
        "mode": detect_mode(question),
        "entities": extract_entities(question),
        "roles": extract_roles(question),
    }
