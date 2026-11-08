from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT = ROOT / 'docs/blueprint/solana-overnight-trading-desk-blueprint-v2.6-consolidated.md'
EXPECTED = '9ab2ea573e88009e50a55f7829eb0b6cbf3e38c4826342c807073220f48ae905'
def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf8'))
