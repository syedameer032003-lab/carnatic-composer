COMPOSER_MEMORY = {
    "chunk_usage": {},
    "chunk_preference": {}
}

def update(category, key):
    store = COMPOSER_MEMORY[category]
    store[key] = store.get(key, 0) + 1

def penalty(category, key, entropy):
    usage = COMPOSER_MEMORY[category].get(key, 0)
    base = 1 / (1 + usage)
    return min(base + (entropy * 0.5), 1.0)

def boost(category, key):
    pref = COMPOSER_MEMORY[category].get(key, 0)
    return 1 + (pref * 0.2)
