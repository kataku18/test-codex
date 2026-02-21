from services.ai_writer import generate_caption


def test_generate_caption_fallback_without_api_key(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    text = generate_caption('新商品の告知', '既存フォロワー', 'フレンドリー')
    assert '新商品の告知' in text
    assert '#instagram' in text
