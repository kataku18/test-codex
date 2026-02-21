from __future__ import annotations

import os


def _fallback_caption(topic: str, audience: str, tone: str, extra_instructions: str) -> str:
    parts = [
        f"{audience}向けに{tone}なトーンで、{topic}についてお届けします。",
        "気になったポイントをコメントで教えてください。",
        "#instagram #ai #automation",
    ]
    if extra_instructions:
        parts.insert(1, f"補足: {extra_instructions}")
    return "\n".join(parts)


def generate_caption(topic: str, audience: str, tone: str, extra_instructions: str = '') -> str:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return _fallback_caption(topic, audience, tone, extra_instructions)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        prompt = (
            'あなたはInstagram投稿のプロです。\\n'
            f'- テーマ: {topic}\\n'
            f'- 対象読者: {audience}\\n'
            f'- トーン: {tone}\\n'
            f'- 追加要望: {extra_instructions or "なし"}\\n'
            '日本語で80〜160文字程度、自然なハッシュタグを3つ付けてください。'
        )
        response = client.responses.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'),
            input=prompt,
            max_output_tokens=220,
        )
        text = response.output_text.strip()
        return text or _fallback_caption(topic, audience, tone, extra_instructions)
    except Exception:
        return _fallback_caption(topic, audience, tone, extra_instructions)
