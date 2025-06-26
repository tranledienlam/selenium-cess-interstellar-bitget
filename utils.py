import time
import random
import inspect
import requests
import re
import ctypes
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from io import BytesIO
from google import genai
from PIL import Image

BIP39_WORDLIST = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual", "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance", "advice", "aerobic", "affair", "afford", "afraid", "again", "age", "agent", "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album", "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone", "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among", "amount", "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry", "animal", "ankle", "announce", "annual", "another", "answer", "antenna", "antique", "anxiety", "any", "apart", "apology", "appear", "apple", "approve", "april", "arch", "arctic", "area", "arena", "argue", "arm", "armed", "armor", "army", "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact", "artist", "artwork", "ask", "aspect", "assault", "asset", "assist", "assume", "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction", "audit", "august", "aunt", "author", "auto", "autumn", "average", "avocado", "avoid", "awake", "aware", "away", "awesome", "awful", "awkward", "axis", "baby", "bachelor", "bacon", "badge", "bag", "balance", "balcony", "ball", "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel", "base", "basic", "basket", "battle", "beach", "bean", "beauty", "because", "become", "beef", "before", "begin", "behave", "behind", "believe", "below", "belt", "bench", "benefit", "best", "betray", "better", "between", "beyond", "bicycle", "bid", "bike", "bind", "biology", "bird", "birth", "bitter", "black", "blade", "blame", "blanket", "blast", "bleak", "bless", "blind", "blood", "blossom", "blouse", "blue", "blur", "blush", "board", "boat", "body", "boil", "bomb", "bone", "bonus", "book", "boost", "border", "boring", "borrow", "boss", "bottom", "bounce", "box", "boy", "bracket", "brain", "brand", "brass", "brave", "bread", "breeze", "brick", "bridge", "brief", "bright", "bring", "brisk", "broccoli", "broken", "bronze", "broom", "brother", "brown", "brush", "bubble", "buddy", "budget", "buffalo", "build", "bulb", "bulk", "bullet", "bundle", "bunker", "burden", "burger", "burst", "bus", "business", "busy", "butter", "buyer", "buzz", "cabbage", "cabin", "cable", "cactus", "cage", "cake", "call", "calm", "camera", "camp", "can", "canal", "cancel", "candy", "cannon", "canoe", "canvas", "canyon", "capable", "capital", "captain", "car", "carbon", "card", "cargo", "carpet", "carry", "cart", "case", "cash", "casino", "castle", "casual", "cat", "catalog", "catch", "category", "cattle", "caught", "cause", "caution", "cave", "ceiling", "celery", "cement", "census", "century", "cereal", "certain", "chair", "chalk", "champion", "change", "chaos", "chapter", "charge", "chase", "chat", "cheap", "check", "cheese", "chef", "cherry", "chest", "chicken", "chief", "child", "chimney", "choice", "choose", "chronic", "chuckle", "chunk", "churn", "cigar", "cinnamon", "circle", "citizen", "city", "civil", "claim", "clap", "clarify", "claw", "clay", "clean", "clerk", "clever", "click", "client", "cliff", "climb", "clinic", "clip", "clock", "clog", "close", "cloth", "cloud", "clown", "club", "clump", "cluster", "clutch", "coach", "coast", "coconut", "code", "coffee", "coil", "coin", "collect", "color", "column", "combine", "come", "comfort", "comic", "common", "company", "concert", "conduct", "confirm", "congress", "connect", "consider", "control", "convince", "cook", "cool", "copper", "copy", "coral", "core", "corn", "correct", "cost", "cotton", "couch", "country", "couple", "course", "cousin", "cover", "coyote", "crack", "cradle", "craft", "cram", "crane", "crash", "crater", "crawl", "crazy", "cream", "credit", "creek", "crew", "cricket", "crime", "crisp", "critic", "crop", "cross", "crouch", "crowd", "crucial", "cruel", "cruise", "crumble", "crunch", "crush", "cry", "crystal", "cube", "culture", "cup", "cupboard", "curious", "current", "curtain", "curve", "cushion", "custom", "cute", "cycle", "dad", "damage", "damp", "dance", "danger", "daring", "dash", "daughter", "dawn", "day", "deal", "debate", "debris", "decade", "december", "decide", "decline", "decorate", "decrease", "deer", "defense", "define", "defy", "degree", "delay", "deliver", "demand", "demise", "denial", "dentist", "deny", "depart", "depend", "deposit", "depth", "deputy", "derive", "describe", "desert", "design", "desk", "despair", "destroy", "detail", "detect", "develop", "device", "devote", "diagram", "dial", "diamond", "diary", "dice", "diesel", "diet", "differ", "digital", "dignity", "dilemma", "dinner", "dinosaur", "direct", "dirt", "disagree", "discover", "disease", "dish", "dismiss", "disorder", "display", "distance", "divert", "divide", "divorce", "dizzy", "doctor", "document", "dog", "doll", "dolphin", "domain", "donate", "donkey", "donor", "door", "dose", "double", "dove", "draft", "dragon", "drama", "drastic", "draw", "dream", "dress", "drift", "drill", "drink", "drip", "drive", "drop", "drum", "dry", "duck", "dumb", "dune", "during", "dust", "dutch", "duty", "dwarf", "dynamic", "eager", "eagle", "early", "earn", "earth", "easily", "east", "easy", "echo", "ecology", "economy", "edge", "edit", "educate", "effort", "egg", "eight", "either", "elbow", "elder", "electric", "elegant", "element", "elephant", "elevator", "elite", "else", "embark", "embody", "embrace", "emerge", "emotion", "employ", "empower", "empty", "enable", "enact", "end", "endless", "endorse", "enemy", "energy", "enforce", "engage", "engine", "enhance", "enjoy", "enlist", "enough", "enrich", "enroll", "ensure", "enter", "entire", "entry", "envelope", "episode", "equal", "equip", "era", "erase", "erode", "erosion", "error", "erupt", "escape", "essay", "essence", "estate", "eternal", "ethics", "evidence", "evil", "evoke", "evolve", "exact", "example", "excess", "exchange", "excite", "exclude", "excuse", "execute", "exercise", "exhaust", "exhibit", "exile", "exist", "exit", "exotic", "expand", "expect", "expire", "explain", "expose", "express", "extend", "extra", "eye", "eyebrow", "fabric", "face", "faculty", "fade", "faint", "faith", "fall", "false", "fame", "family", "famous", "fan", "fancy", "fantasy", "farm", "fashion", "fat", "fatal", "father", "fatigue", "fault", "favorite", "feature", "february", "federal", "fee", "feed", "feel", "female", "fence", "festival", "fetch", "fever", "few", "fiber", "fiction", "field", "figure", "file", "film", "filter", "final", "find", "fine", "finger", "finish", "fire", "firm", "first", "fiscal", "fish", "fit", "fitness", "fix", "flag", "flame", "flash", "flat", "flavor", "flee", "flight", "flip", "float", "flock", "floor", "flower", "fluid", "flush", "fly", "foam", "focus", "fog", "foil", "fold", "follow", "food", "foot", "force", "forest", "forget", "fork", "fortune", "forum", "forward", "fossil", "foster", "found", "fox", "fragile", "frame", "frequent", "fresh", "friend", "fringe", "frog", "front", "frost", "frown", "frozen", "fruit", "fuel", "fun", "funny", "furnace", "fury", "future", "gadget", "gain", "galaxy", "gallery", "game", "gap", "garage", "garbage", "garden", "garlic", "garment", "gas", "gasp", "gate", "gather", "gauge", "gaze", "general", "genius", "genre", "gentle", "genuine", "gesture", "ghost", "giant", "gift", "giggle", "ginger", "giraffe", "girl", "give", "glad", "glance", "glare", "glass", "glide", "glimpse", "globe", "gloom", "glory", "glove", "glow", "glue", "goat", "goddess", "gold", "good", "goose", "gorilla", "gospel", "gossip", "govern", "gown", "grab", "grace", "grain", "grant", "grape", "grass", "gravity", "great", "green", "grid", "grief", "grit", "grocery", "group", "grow", "grunt", "guard", "guess", "guide", "guilt", "guitar", "gun", "gym", "habit", "hair", "half", "hammer", "hamster", "hand", "happy", "harbor", "hard", "harsh", "harvest", "hat", "have", "hawk", "hazard", "head", "health", "heart", "heavy", "hedgehog", "height", "hello", "helmet", "help", "hen", "hero", "hidden", "high", "hill", "hint", "hip", "hire", "history", "hobby", "hockey", "hold", "hole", "holiday", "hollow", "home", "honey", "hood", "hope", "horn", "horror", "horse", "hospital", "host", "hotel", "hour", "hover", "hub", "huge", "human", "humble", "humor", "hundred", "hungry", "hunt", "hurdle", "hurry", "hurt", "husband", "hybrid", "ice", "icon", "idea", "identify", "idle", "ignore", "ill", "illegal", "illness", "image", "imitate", "immense", "immune", "impact", "impose", "improve", "impulse", "inch", "include", "income", "increase", "index", "indicate", "indoor", "industry", "infant", "inflict", "inform", "inhale", "inherit", "initial", "inject", "injury", "inmate", "inner", "innocent", "input", "inquiry", "insane", "insect", "inside", "inspire", "install", "intact", "interest", "into", "invest", "invite", "involve", "iron", "island", "isolate", "issue", "item", "ivory", "jacket", "jaguar", "jar", "jazz", "jealous", "jeans", "jelly", "jewel", "job", "join", "joke", "journey", "joy", "judge", "juice", "jump", "jungle", "junior", "junk", "just", "kangaroo", "keen", "keep", "ketchup", "key", "kick", "kid", "kidney", "kind", "kingdom", "kiss", "kit", "kitchen", "kite", "kitten", "kiwi", "knee", "knife", "knock", "know", "lab", "label", "labor", "ladder", "lady", "lake", "lamp", "language", "laptop", "large", "later", "latin", "laugh", "laundry", "lava", "law", "lawn", "lawsuit", "layer", "lazy", "leader", "leaf", "learn", "leave", "lecture", "left", "leg", "legal", "legend", "leisure", "lemon", "lend", "length", "lens", "leopard", "lesson", "letter", "level", "liar", "liberty", "library", "license", "life", "lift", "light", "like", "limb", "limit", "link", "lion", "liquid", "list", "little", "live", "lizard", "load", "loan", "lobster", "local", "lock", "logic", "lonely", "long", "loop", "lottery", "loud", "lounge", "love", "loyal", "lucky", "luggage", "lumber", "lunar", "lunch", "luxury", "lyrics", "machine", "mad", "magic", "magnet", "maid", "mail", "main", "major", "make", "mammal", "man", "manage", "mandate", "mango", "mansion", "manual", "maple", "marble", "march", "margin", "marine", "market", "marriage", "mask", "mass", "master", "match", "material", "math", "matrix", "matter", "maximum", "maze", "meadow", "mean", "measure", "meat", "mechanic", "medal", "media", "melody", "melt", "member", "memory", "mention", "menu", "mercy", "merge", "merit", "merry", "mesh", "message", "metal", "method", "middle", "midnight", "milk", "million", "mimic", "mind", "minimum", "minor", "minute", "miracle", "mirror", "misery", "miss", "mistake", "mix", "mixed", "mixture", "mobile", "model", "modify", "mom", "moment", "monitor", "monkey", "monster", "month", "moon", "moral", "more", "morning", "mosquito", "mother", "motion", "motor", "mountain", "mouse", "move", "movie", "much", "muffin", "mule", "multiply", "muscle", "museum", "mushroom", "music", "must", "mutual", "myself", "mystery", "myth", "naive", "name", "napkin", "narrow", "nasty", "nation", "nature", "near", "neck", "need", "negative", "neglect", "neither", "nephew", "nerve", "nest", "net", "network", "neutral", "never", "news", "next", "nice", "night", "noble", "noise", "nominee", "noodle", "normal", "north", "nose", "notable", "note", "nothing", "notice", "novel", "now", "nuclear", "number", "nurse", "nut", "oak", "obey", "object", "oblige", "obscure", "observe", "obtain", "obvious", "occur", "ocean", "october", "odor", "off", "offer", "office", "often", "oil", "okay", "old", "olive", "olympic", "omit", "once", "one", "onion", "online", "only", "open", "opera", "opinion", "oppose", "option", "orange", "orbit", "orchard", "order", "ordinary", "organ", "orient", "original", "orphan", "ostrich", "other", "outdoor", "outer", "output", "outside", "oval", "oven", "over", "own", "owner", "oxygen", "oyster", "ozone", "pact", "paddle", "page", "pair", "palace", "palm", "panda", "panel", "panic", "panther", "paper", "parade", "parent", "park", "parrot", "party", "pass", "patch", "path", "patient", "patrol", "pattern", "pause", "pave", "payment", "peace", "peanut", "pear", "peasant", "pelican", "pen", "penalty", "pencil", "people", "pepper", "perfect", "permit", "person", "pet", "phone", "photo", "phrase", "physical", "piano", "picnic", "picture", "piece", "pig", "pigeon", "pill", "pilot", "pink", "pioneer", "pipe", "pistol", "pitch", "pizza", "place", "planet", "plastic", "plate", "play", "please", "pledge", "pluck", "plug", "plunge", "poem", "poet", "point", "polar", "pole", "police", "pond", "pony", "pool", "popular", "portion", "position", "possible", "post", "potato", "pottery", "poverty", "powder", "power", "practice", "praise", "predict", "prefer", "prepare", "present", "pretty", "prevent", "price", "pride", "primary", "print", "priority", "prison", "private", "prize", "problem", "process", "produce", "profit", "program", "project", "promote", "proof", "property", "prosper", "protect", "proud", "provide", "public", "pudding", "pull", "pulp", "pulse", "pumpkin", "punch", "pupil", "puppy", "purchase", "purity", "purpose", "purse", "push", "put", "puzzle", "pyramid", "quality", "quantum", "quarter", "question", "quick", "quit", "quiz", "quote", "rabbit", "raccoon", "race", "rack", "radar", "radio", "rail", "rain", "raise", "rally", "ramp", "ranch", "random", "range", "rapid", "rare", "rate", "rather", "raven", "raw", "razor", "ready", "real", "reason", "rebel", "rebuild", "recall", "receive", "recipe", "record", "recycle", "reduce", "reflect", "reform", "refuse", "region", "regret", "regular", "reject", "relax", "release", "relief", "rely", "remain", "remember", "remind", "remove", "render", "renew", "rent", "reopen", "repair", "repeat", "replace", "report", "require", "rescue", "resemble", "resist", "resource", "response", "result", "retire", "retreat", "return", "reunion", "reveal", "review", "reward", "rhythm", "rib", "ribbon", "rice", "rich", "ride", "ridge", "rifle", "right", "rigid", "ring", "riot", "ripple", "risk", "ritual", "rival", "river", "road", "roast", "robot", "robust", "rocket", "romance", "roof", "rookie", "room", "rose", "rotate", "rough", "round", "route", "royal", "rubber", "rude", "rug", "rule", "run", "runway", "rural", "sad", "saddle", "sadness", "safe", "sail", "salad", "salmon", "salon", "salt", "salute", "same", "sample", "sand", "satisfy", "satoshi", "sauce", "sausage", "save", "say", "scale", "scan", "scare", "scatter", "scene", "scheme", "school", "science", "scissors", "scorpion", "scout", "scrap", "screen", "script", "scrub", "sea", "search", "season", "seat", "second", "secret", "section", "security", "seed", "seek", "segment", "select", "sell", "seminar", "senior", "sense", "sentence", "series", "service", "session", "settle", "setup", "seven", "shadow", "shaft", "shallow", "share", "shed", "shell", "sheriff", "shield", "shift", "shine", "ship", "shiver", "shock", "shoe", "shoot", "shop", "short", "shoulder", "shove", "shrimp", "shrug", "shuffle", "shy", "sibling", "sick", "side", "siege", "sight", "sign", "silent", "silk", "silly", "silver", "similar", "simple", "since", "sing", "siren", "sister", "situate", "six", "size", "skate", "sketch", "ski", "skill", "skin", "skirt", "skull", "slab", "slam", "sleep", "slender", "slice", "slide", "slight", "slim", "slogan", "slot", "slow", "slush", "small", "smart", "smile", "smoke", "smooth", "snack", "snake", "snap", "sniff", "snow", "soap", "soccer", "social", "sock", "soda", "soft", "solar", "soldier", "solid", "solution", "solve", "someone", "song", "soon", "sorry", "sort", "soul", "sound", "soup", "source", "south", "space", "spare", "spatial", "spawn", "speak", "special", "speed", "spell", "spend", "sphere", "spice", "spider", "spike", "spin", "spirit", "split", "spoil", "sponsor", "spoon", "sport", "spot", "spray", "spread", "spring", "spy", "square", "squeeze", "squirrel", "stable", "stadium", "staff", "stage", "stairs", "stamp", "stand", "start", "state", "stay", "steak", "steel", "stem", "step", "stereo", "stick", "still", "sting", "stock", "stomach", "stone", "stool", "story", "stove", "strategy", "street", "strike", "strong", "struggle", "student", "stuff", "stumble", "style", "subject", "submit", "subway", "success", "such", "sudden", "suffer", "sugar", "suggest", "suit", "summer", "sun", "sunny", "sunset", "super", "supply", "supreme", "sure", "surface", "surge", "surprise", "surround", "survey", "suspect", "sustain", "swallow", "swamp", "swap", "swarm", "swear", "sweet", "swift", "swim", "swing", "switch", "sword", "symbol", "symptom", "syrup", "system", "table", "tackle", "tag", "tail", "talent", "talk", "tank", "tape", "target", "task", "taste", "tattoo", "taxi", "teach", "team", "tell", "ten", "tenant", "tennis", "tent", "term", "test", "text", "thank", "that", "theme", "then", "theory", "there", "they", "thing", "this", "thought", "three", "thrive", "throw", "thumb", "thunder", "ticket", "tide", "tiger", "tilt", "timber", "time", "tiny", "tip", "tired", "tissue", "title", "toast", "tobacco", "today", "toddler", "toe", "together", "toilet", "token", "tomato", "tomorrow", "tone", "tongue", "tonight", "tool", "tooth", "top", "topic", "topple", "torch", "tornado", "tortoise", "toss", "total", "tourist", "toward", "tower", "town", "toy", "track", "trade", "traffic", "tragic", "train", "transfer", "trap", "trash", "travel", "tray", "treat", "tree", "trend", "trial", "tribe", "trick", "trigger", "trim", "trip", "trophy", "trouble", "truck", "true", "truly", "trumpet", "trust", "truth", "try", "tube", "tuition", "tumble", "tuna", "tunnel", "turkey", "turn", "turtle", "twelve", "twenty", "twice", "twin", "twist", "two", "type", "typical", "ugly", "umbrella", "unable", "unaware", "uncle", "uncover", "under", "undo", "unfair", "unfold", "unhappy", "uniform", "unique", "unit", "universe", "unknown", "unlock", "until", "unusual", "unveil", "update", "upgrade", "uphold", "upon", "upper", "upset", "urban", "urge", "usage", "use", "used", "useful", "useless", "usual", "utility", "vacant", "vacuum", "vague", "valid", "valley", "valve", "van", "vanish", "vapor", "various", "vast", "vault", "vehicle", "velvet", "vendor", "venture", "venue", "verb", "verify", "version", "very", "vessel", "veteran", "viable", "vibrant", "vicious", "victory", "video", "view", "village", "vintage", "violin", "virtual", "virus", "visa", "visit", "visual", "vital", "vivid", "vocal", "voice", "void", "volcano", "volume", "vote", "voyage", "wage", "wagon", "wait", "walk", "wall", "walnut", "want", "warfare", "warm", "warrior", "wash", "wasp", "waste", "water", "wave", "way", "wealth", "weapon", "wear", "weasel", "weather", "web", "wedding", "weekend", "weird", "welcome", "west", "wet", "whale", "what", "wheat", "wheel", "when", "where", "whip", "whisper", "wide", "width", "wife", "wild", "will", "win", "window", "wine", "wing", "wink", "winner", "winter", "wire", "wisdom", "wise", "wish", "witness", "wolf", "woman", "wonder", "wood", "wool", "word", "work", "world", "worry", "worth", "wrap", "wreck", "wrestle", "wrist", "write", "wrong", "yard", "year", "yellow", "you", "young", "youth", "zebra", "zero", "zone", "zoo"
]

DIR_PATH = Path(__file__).parent

class SeedConverter:
    @staticmethod
    def _seed_to_indices(seed: List[str]) -> List[int]:
        """
        Chuyển danh sách từ seed thành danh sách chỉ số tương ứng.
        """

        return [BIP39_WORDLIST.index(word) for word in seed]

    @staticmethod
    def _indices_to_seed(indices: List[int]) -> List[str]:
        """
        Chuyển danh sách chỉ số thành danh sách từ seed tương ứng.
        """
        return [BIP39_WORDLIST[index] for index in indices]

    @staticmethod
    def _transform_indices(indices: List[int], key: int) -> List[int]:
        """
        Biến đổi danh sách chỉ số bằng cách sử dụng khóa (key).
        """
        return [(index + key) % len(BIP39_WORDLIST) for index in indices]

    @staticmethod
    def encrypt(seed: str, key: int = 42):
        """
        Chuyển đổi seed gốc thành seed khác dựa trên khóa (key).

        Args:
            seed (str): Chuỗi seed gốc (12 từ cách nhau bởi dấu cách).
            key (int): Khóa để mã hóa seed.

        Returns:
            str: Chuỗi seed mới (12 từ cách nhau bởi dấu cách).
        """
        seed_words = seed.split(" ")
        
        seed_indices = SeedConverter._seed_to_indices(seed_words)
        transformed_indices = SeedConverter._transform_indices(
            seed_indices, key)
        encrypt_words = SeedConverter._indices_to_seed(transformed_indices)
        return " ".join(encrypt_words)

    @staticmethod
    def decrypt(encrypted_seed: str, key: int = 42) -> str:
        """
        Chuyển đổi seed khác về seed gốc dựa trên khóa (key).

        Args:
            encrypted_seed (List[str]): Danh sách 12 từ seed đã mã hóa.
            key (int): Khóa để giải mã seed.

        Returns:
            str: Chuỗi seed gốc (12 từ cách nhau bởi dấu cách).
        """
        seed_words = encrypted_seed.split(" ")
        seed_indices = SeedConverter._seed_to_indices(seed_words)
        original_indices = SeedConverter._transform_indices(seed_indices, -key)
        original_seed = SeedConverter._indices_to_seed(original_indices)
        return " ".join(original_seed)

class Utility:
    @staticmethod
    def wait_time(second: int = 5, fix: bool = False) -> True:
        '''
        Đợi trong một khoảng thời gian nhất định.  Với giá trị dao động từ -50% đên 50%

        Args:
            seconds (int) = 2: Số giây cần đợi.
            fix (bool) = False: False sẽ random, True không random
        '''
        if not fix:
            gap = 0.4
            second = random.uniform(second * (1 - gap), second * (1 + gap))

        time.sleep(second)
        return True

    @staticmethod
    def timeout(second: int = 5):
        """
        Trả về một hàm kiểm tra, cho biết liệu thời gian đã vượt quá giới hạn timeout hay chưa.

        Hàm này được dùng để thay thế biểu thức lặp kiểu:
            start_time = time.time()
            while time.time() - start_time < seconds:

        Args:
            secons (int): Thời gian giới hạn tính bằng giây.

        Returns:
            Callable[[], bool]: Một hàm không tham số, trả về True nếu vẫn còn trong thời gian cho phép, False nếu đã hết thời gian.
        """
        start_time = time.time()
        
        def checker():
            return time.time() - start_time < second
        
        return checker

    @staticmethod
    def logger(profile_name: str = 'System', message: str = 'Chưa có mô tả nhật ký', show_log: bool = True):
        '''
        Ghi và hiển thị thông báo nhật ký (log)
        
        Cấu trúc log hiển thị:
            [profile_name][func_thuc_thi]: {message}
        
        Args:
            profile_name (str): tên hồ sơ hiện tại
            message (str): Nội dung thông báo log.
            show_log (bool, option): cho phép hiển thị nhật ký hay không. Mặc định: True (cho phép)
        '''
        if show_log:
            func_name = inspect.stack()[2].function
            print(f'[{profile_name}][{func_name}]: {message}')
    
    @staticmethod
    def print_section(title: str, icon: str = "🔔"):
        print("\n"+"=" * 60)
        print(f"{icon} {title.upper()}")
        print("=" * 60+"\n")

    @staticmethod
    def is_proxy_working(proxy_info: str = None):
        ''' Kiểm tra proxy có hoạt động không bằng cách gửi request đến một trang kiểm tra IP
        
        Args:
            proxy_info (str, option): thông tin proxy được truyền vào có dạng sau
                - "ip:port"
                - "username:password@ip:port"
        
        Returns:
            bool: True nếu proxy hoạt động, False nếu không.
        '''
        if not proxy_info:
            return False
        
        proxies = {
            "http": f"http://{proxy_info}",
            "https": f"https://{proxy_info}",
        }
        
        test_url = "http://ip-api.com/json"  # API kiểm tra địa chỉ IP

        try:
            response = requests.get(test_url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                print(f"✅ Proxy hoạt động! IP: {response.json().get('query')}")
                return True
            else:
                print(f"❌ Proxy {proxy_info} không hoạt động! Mã lỗi: {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"❌ Proxy {proxy_info} lỗi: {e}")
            return False
    
    @staticmethod
    def read_data(*field_names):
        '''
        Lấy dữ liệu từ tệp data.txt

        Args:
            *field_names: tên các trường cần lấy

        Returns:
            list: danh sách các dictionary, mỗi dictionary là một profile

        Xử lý dữ liệu:
            - Nếu parts trong dòng ít hơn field_names, field_name được gán bằng None
            - Nếu parts trong dòng nhiều hơn field_names, phần tử còn lại sẽ được gán vào `extra_fields`
            - Dữ liệu phải bắt đầu bằng `profile_name`, kết thúc bằng `extra_fields` (optional) và `proxy_info` (optional)
        '''
        data_path = DIR_PATH /'data.txt'

        if not data_path.exists():
            print(f"File {data_path} không tồn tại.")
            return []

        proxy_re = re.compile(r"^(?:\w+:\w+@)?\d{1,3}(?:\.\d{1,3}){3}:\d{1,5}$")
        profiles = []

        with open(data_path, 'r') as file:
            data = file.readlines()

        for line in data:
            parts = [part.strip() for part in line.strip().split('|')]
            
            # Kiểm tra và tách proxy nếu có
            proxy_info = parts[-1] if proxy_re.match(parts[-1]) else None
            if proxy_info:
                parts = parts[:-1]
                
            # Kiểm tra số lượng dữ liệu
            if len(parts) < 1:
                print(f"Warning: Dữ liệu không hợp lệ - {line}")
                continue
                
            # Tạo dictionary với các trường được chỉ định
            profile = {}
            # Gán giá trị cho các field có trong parts
            for i, field_name in enumerate(field_names):
                if i < len(parts):
                    profile[field_name] = parts[i]
                else:
                    profile[field_name] = None

            profile['extra_fields'] = parts[len(field_names):]
            profile['proxy_info'] = proxy_info
            profiles.append(profile)
        
        return profiles
    
    @staticmethod
    def fake_data(field_name: str = "profile_name", numbers: int = 0):
        profiles = []
        for i in range(numbers):
            profile = {}
            profile[field_name] = str(i + 1)
            profiles.append(profile)
        return profiles
    
    @staticmethod
    def read_token(name_bot: str) -> Optional[List[tuple]]:
        """
        Lấy thông tin token từ tệp `token.txt` dựa trên tên bot.

        Tệp cấu hình `token.txt` phải nằm trong cùng thư mục với tệp mã nguồn. 
        Mỗi dòng trong tệp phải có định dạng: [tên_bot]|[giá trị_1]|[giá trị_2]|...

        Ví dụ dòng hợp lệ:
            tele_bot|123456|ABCDEF
            ai_bot|apikey_abc|user_xyz

        Args:
            name_bot (str): Tên định danh của bot, ví dụ: 'tele_bot', 'ai_bot', v.v.

        Returns:
            Optional[List[tuple]]: 
                - Danh sách tuple chứa dữ liệu tương ứng với bot nếu tìm thấy.
                - Danh sách rỗng nếu không tìm thấy dòng nào phù hợp.
                - None nếu tệp không tồn tại hoặc gặp lỗi khi đọc.
        
        Ghi chú:
            - Nếu tệp không tồn tại, sẽ ghi log và trả về None.
            - Nếu dòng không hợp lệ (ít hơn 2 phần tử), sẽ ghi cảnh báo nhưng bỏ qua dòng đó.
        """
        token_path = DIR_PATH / 'token.txt'
        tokens = []

        if not token_path.exists():
            Utility.logger(message=f"⚠️ Tệp {token_path} không tồn tại.")
            return None
    
        try:
            with open(token_path, 'r') as file:
                data = file.readlines()
            for line in data:
                if line.strip().startswith(name_bot):
                    parts = [part.strip() for part in line.strip().split('|')]
                    if len(parts) >= 2:
                        tokens.append(tuple(parts[1:]))
                    else:
                        Utility.logger(
                            message=f'Nội dung dòng {line.strip()} không hợp lệ. Định dạng đúng "{name_bot}|[giá trị_1]|[giá trị_2]|...".')
            return tokens
        
        except Exception as e:
            Utility.logger(message=f'Lỗi khi đọc tệp {token_path}: {e}')
            return None
        
class TeleHelper:
    def __init__(self) -> None:
        self.valid: bool = False
        self.bot_name = None
        self._chat_id = None
        self._token = None
        self._endpoint = None
        
        self._get_token()
        if not self.valid:
            print('❌ Telegram bot không hoạt động')

    def _check_token_valid(self) -> bool:
        if not self._token:
            return False

        url = f"{self._endpoint}/bot{self._token}/getMe"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get("ok"):
                self.bot_name = f"@{data['result']['username']}"
                print(f"✅ Telegram bot hoạt động: {self.bot_name}")
                return True
            else:
                return False
        except Exception as e:
            return False

    def _get_token(self):
        """
        Đọc token Telegram từ file cấu hình và khởi tạo thông tin bot.

        Nếu đọc được token hợp lệ (đúng định dạng và được Telegram xác nhận),
        thì gán giá trị vào các thuộc tính:
            - self._chat_id
            - self._token
            - self._endpoint
            - self.valid = True

        Returns:
            bool: True nếu tìm thấy và xác thực được token, ngược lại False.
        """
        tokens = Utility.read_token('tele_bot')
        if tokens is not None:
            print(f'🛠️  Đang kiểm tra token Telegram bot...')
            for token in tokens:
                if len(token) >= 2:
                    self._chat_id = token[0]
                    self._token = token[1]
                    if len(token) >= 3 and 'http' in token[2]:
                        self._endpoint = token[-1].rstrip('/')
                    else:
                        self._endpoint = 'https://api.telegram.org'
                    self.valid = self._check_token_valid()
                    if self.valid:
                        return True

            return False

    def send_photo(self, screenshot_png, message: str = 'khởi động...'):
        """
        Gửi tin nhắn đến Telegram bot. Kiểm tra token trước khi gửi.
        """
        if not self.valid or not all([self._chat_id, self._token]):
            Utility.logger(message="❌ Không thể gửi tin nhắn: Token không hợp lệ hoặc chưa được thiết lập.")
            self.valid = False
            return False

        url = f"{self._endpoint}/bot{self._token}/sendPhoto"

        
        data = {'chat_id': self._chat_id,
                'caption': message}
        # Gửi ảnh lên Telegram
        try:
            with BytesIO(screenshot_png) as screenshot_buffer:
                files = {
                    'photo': ('screenshot.png', screenshot_buffer, 'image/png')
                }
                response = requests.post(url, files=files, data=data, timeout=5)
                res_json = response.json()

                if not res_json.get("ok"):
                    Utility.logger(message=f"❌ Gửi ảnh thất bại: {res_json}")
                    self.valid = False
                    return False

                return True

        except requests.exceptions.RequestException as e:
            Utility.logger(message=f"❌ Lỗi kết nối khi gửi tin nhắn: {e}")
            self.valid = False
            return False

class AIHelper:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Khởi tạo AI Helper với API key và model name
        
        Args:
            api_key (str): API key của Gemini
            model_name (str, optional): Tên model sử dụng. Mặc định là "gemini-2.0-flash"
            
        Returns:
            bool: True nếu AI hoạt động, False nếu không hoạt động
        """
        self.is_working = False
        self.model_name = model_name
        self.valid = False
        self._token = None
        self._client = None
        
        self._get_token()
        if not self.valid:
            print('❌ AI bot không hoạt động')

    def _check_token_valid(self) -> bool:
        try:
            client = genai.Client(api_key=self._token)
            _ = client.models.list()
            self._client = client
            print("✅ AI bot hoạt động")
            return True
        except Exception as e:
            print(f"❌ Token lỗi: {e}")
            return False
        
    def _get_token(self):
        """
        Đọc token AI Gemini từ file cấu hình và khởi tạo thông tin bot.

        Nếu đọc được token hợp lệ (đúng định dạng và được Telegram xác nhận),
        thì gán giá trị vào các thuộc tính:
            - self._chat_id
            - self._token
            - self._endpoint
            - self.valid = True

        Returns:
            bool: True nếu tìm thấy và xác thực được token, ngược lại False.
        """
        tokens = Utility.read_token('ai_bot')
        if tokens is not None:
            print(f'🛠️  Đang kiểm tra token AI bot...')
            for token in tokens:
                if len(token) >= 1:
                    self._token = token[0]
                    self.valid = self._check_token_valid()
                    if self.valid:
                        return True

            return False

    @staticmethod
    def _process_image(image: Image) -> Image:
        """
        Xử lý ảnh để tối ưu kích thước trước khi gửi lên AI
        
        Args:
            image (Image): Ảnh cần xử lý
            
        Returns:
            Image: Ảnh đã được resize
        """
        if type(image) == bytes:
            image = Image.open(BytesIO(image))
            
        width, height = image.size
        max_size = 384
        
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        new_size = (new_width, new_height)
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    def ask(self, prompt: str, image: Image = None) -> tuple[str | None, str | None]:
        """
        Gửi prompt và ảnh lên AI để phân tích
        
        Args:
            prompt (str): Câu hỏi hoặc yêu cầu gửi đến AI
            image (Image, optional): Ảnh cần phân tích. Nếu None, sẽ trả về None
            
        Returns:
            tuple[str | None, str | None]: 
                - Phần tử đầu tiên: Kết quả phân tích từ AI hoặc None nếu có lỗi
                - Phần tử thứ hai: Thông báo lỗi hoặc None nếu không có lỗi
        """
        result = None
        try:
            if image:
                resized_image = self._process_image(image)
                response = self._client.models.generate_content(
                                    model=self.model_name,
                                    contents=[resized_image, prompt]
                                )
            else:
                response = self._client.models.generate_content(
                                    model=self.model_name,
                                    contents=prompt
                                )
            
            result = response.text
            return result, None
            
        except Exception as e:
            error_message = str(e)
            if "INVALID_ARGUMENT" in error_message or "API key not valid" in error_message:
                return None, f"API key không hợp lệ. Vui lòng kiểm tra lại token."
            elif "blocked" in error_message.lower():
                return None, f"Prompt vi phạm chính sách nội dung - {error_message}"
            elif "permission" in error_message.lower():
                return None, f"Không có quyền truy cập API - {error_message}"
            elif "quota" in error_message.lower() or "limit" in error_message.lower():
                return None, f"Vượt quá giới hạn tài nguyên - {error_message}"
            elif "timeout" in error_message.lower() or "deadline" in error_message.lower():
                return None, f"Vượt quá thời gian xử lý - {error_message}"
            else:
                return None, f"Lỗi không xác định khi gửi yêu cầu đến AI - {error_message}"

class Chromium:
    """
    Hỗ trợ tự động tải về và giải nén trình duyệt Chromium từ GitHub, bằng công cụ 7zr.exe.

    Nguồn github: https://github.com/macchrome/winchrome/releases
    """
    def __init__(self):
        f"""
        Khởi tạo class với các tham số mặc định:
        - URL tải Chromium và công cụ 7zr.exe
        - Tên tệp nén và công cụ giải nén
        - Đường dẫn thư mục tải và thư mục đích
        """
        self._CHROMIUM_URL = "https://github.com/macchrome/winchrome/releases/download/v136.7103.97-M136.0.7103.97-r1440670-Win64/ungoogled-chromium-136.0.7103.97-1_Win64.7z"
        self._EXE_URL = "https://www.7-zip.org/a/7zr.exe"
        self._FILE_CHROMIUM = "chromium136.7z"
        self._FILE_EXE = "7zr.exe"
        self._TARGET_FOLDER_NAME = "chromium136"
        self._DOWLOAD_PATH = Path(self._get_system_drive()) / 'chromium'

        self.path = self._setup()
    
    @staticmethod
    def _get_system_drive() -> Path:
        """
        Lấy ổ hệ điều hành hiện tại (ví dụ: 'C:\\', 'D:\\').
        Trả về một chuỗi đường dẫn ổ đĩa có hậu tố '\\' để đảm bảo đúng định dạng tuyệt đối.
        """
        buffer = ctypes.create_unicode_buffer(260)
        ctypes.windll.kernel32.GetWindowsDirectoryW(buffer, 260)
        return Path(buffer.value).drive + "\\"

    def _show_download_progress(self, block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = downloaded / total_size * 100 if total_size > 0 else 0
        percent = percent if percent < 100 else 100
        bar_len = 40
        filled_len = int(bar_len * downloaded // total_size) if total_size else 0
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write(f"\r📥 [{bar}] {percent:5.1f}%")
        sys.stdout.flush()

    def _download_file(self, file_name: str, url: str) -> Path | None:
        """
        Tải một tập tin từ URL nếu chưa tồn tại trong thư mục chỉ định.

        Args:
            file_name (str): Tên tệp cần tải.
            url (str): URL nguồn.

        Returns:
            Path | None: Trả về đường dẫn tệp nếu mới tải, None nếu tệp đã tồn tại.
        """
        file_path = self._DOWLOAD_PATH / file_name

        if file_path.exists():
            size = file_path.stat().st_size
            if size > 0:
                print(f"✅ Đã tồn tại {file_name}")
                return file_path
            else:
                print(f"❌ File lỗi ({size} bytes). Xóa file...")
                file_path.unlink(missing_ok=True)
        try:
            print(f"⬇️ Đang tải {file_name}...")
            urllib.request.urlretrieve(url, file_path, reporthook=self._show_download_progress)
            Utility.wait_time(2)
            
            if file_path.exists():
                if file_path.stat().st_size > 0:
                    print(f"✅ Tải {file_name} thành công")
                    return file_path
                else:
                    print(f"❌ File tải bị lỗi ({size} bytes). Xóa file...")
                    file_path.unlink(missing_ok=True)
            else:
                print(f"❌ Không tìm thấy {file_path} đã tải...")

        except Exception as e:
            print(f"❌ Lỗi quá trình tải: {e}")
        
        return None
    
    def _delete_file(self, file_path: Path):
        """
        Xóa một tệp nếu tồn tại.

        Args:
            file_path (Path): Đường dẫn đến tệp cần xóa.

        Returns:
            bool: True nếu xóa thành công, False nếu thất bại.
        """
        if file_path.exists() and file_path.is_file():
            try:
                file_path.unlink()
                return True
            except Exception as e:
                print(f"❌ Không thể xóa file {file_path}: {e}")
        else:
            print(f"⚠️ File không tồn tại: {file_path}")
        return False

    def _extract_7z_with_7zr(self, file_path: Path | None, tool_extract: Path | None)-> Path | None:
        """
        Giải nén tệp `.7z` bằng công cụ `7zr.exe`, và tìm thư mục mới được tạo sau khi giải nén.

        Args:
            file_path (Path): Đường dẫn đến file `.7z`.
            tool_extract (Path): Đường dẫn đến `7zr.exe`.

        Returns:
            Path | None: Trả về thư mục mới được giải nén, hoặc None nếu thất bại.
        """
        before_folders = set(f.name for f in self._DOWLOAD_PATH.iterdir() if f.is_dir())

        timeout = time.time()+10
        if not (tool_extract and file_path):
            if not tool_extract:
               print(f"❌ tool_extract không thể là None")
            if not file_path:
               print(f"❌ file_path không thể là None") 
            return None
        
        while True:
            if tool_extract and tool_extract.exists():
                if file_path and file_path.exists() and (file_path.stat().st_size / (1024 *1024) > 100):
                    break
            if timeout - time.time() < 0:
                print(f'Lỗi không tìm thấy đủ 2 file: {self._FILE_CHROMIUM} (>100M) - {self._FILE_EXE} (500k)')
                return None
            Utility.wait_time(1)

        try:
            result = subprocess.run(
                [str(tool_extract), 'x', str(file_path), f'-o{self._DOWLOAD_PATH}', '-y'],
                capture_output=True, text=True
            )
        except Exception as e:
            Utility.logger(f'Lỗi giải nén file: {e}')
            return None
        
        if result.returncode == 0:
            print("✅ Giải nén hoàn tất.")
            self._delete_file(file_path)
            self._delete_file(tool_extract)
            after_folders = set(f.name for f in self._DOWLOAD_PATH.iterdir() if f.is_dir())
            new_folders = list(after_folders - before_folders)
            if new_folders:
                for name in new_folders:
                    if "ungoogled" in name.lower():
                        return self._DOWLOAD_PATH / name
                return self._DOWLOAD_PATH / new_folders[0]
            else:
                print("⚠️ Không tìm thấy thư mục mới.")
                return None
        else:
            print(f"❌ Giải nén lỗi: {result.stderr}")
            return None
    
    def _setup(self) -> Path | None:
        """
        Hàm chính để thiết lập trình duyệt Chromium:
        - Tạo thư mục tải nếu chưa có
        - Kiểm tra nếu thư mục đích đã tồn tại thì bỏ qua
        - Nếu chưa có, tải xuống và giải nén
        - Đổi tên thư mục giải nén thành thư mục đích

        Returns:
            Path | None: Trả về path chrome.exe, hoặc None nếu thất bại.
        """
        self._DOWLOAD_PATH.mkdir(parents=True, exist_ok=True)

        target_dir = self._DOWLOAD_PATH / self._TARGET_FOLDER_NAME
        target_chromium = target_dir / 'chrome.exe'

        if target_chromium.exists():
            return target_chromium
        else:
            chromium_path = self._download_file(self._FILE_CHROMIUM, self._CHROMIUM_URL)
            exe_path = self._download_file(self._FILE_EXE, self._EXE_URL)
            if chromium_path and exe_path:
                extracted_folder = self._extract_7z_with_7zr(chromium_path, exe_path)
                if extracted_folder:
                    extracted_chromium = extracted_folder / 'chrome.exe'
                    if (extracted_chromium).exists():
                        extracted_folder.rename(target_dir)
                        if target_chromium.exists():
                            print(f"✅ Phiên bản chromium lưu tại: {target_dir}")
                            return target_chromium
                        else:
                            print(f"❌ Không tìm thấy {target_chromium}")
                    else:
                        print(f"❌ Không tìm thấy {extracted_chromium}")
                else:
                    print(f"❌ Không tìm thấy {extracted_folder}")
            else:
                print(f"❌ Không thể thực hiện giải nén vì thiếu file.")
            
        return None
    
if __name__ == "__main__":
    profiles = Utility.read_data('profile_name', 'pass', 'seeds')
    ai = AIHelper()
    ai.ask("Giới thiệu về bạn?")
    # print(tele.token)
    # Seed ban đầu
    # original_seed = "gas vacuum social float present exist atom gold relax glance credit soldier"
    # key = 42  # Khóa để chuyển đổi

    # # Chuyển đổi seed gốc thành seed khác
    # encrypted_seed = SeedConverter.encrypt(original_seed, key)

    # # Chuyển đổi seed khác về seed gốc
    # decrypted_seed = SeedConverter.decrypt(encrypted_seed, key)

    # # Kiểm tra kết quả
    # assert original_seed == decrypted_seed, "Seed sau giải mã không khớp với seed gốc!"
