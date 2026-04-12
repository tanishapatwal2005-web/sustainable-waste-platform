
import os
from openai import OpenAI
def get_bot_response(message):
    message = message.lower()

    # 🔹 LOCAL RESPONSES (NO API)
    if "plastic" in message:
        return "♻️ Plastic can be recycled. Clean it and put in recycling bin."

    elif "glass" in message:
        return "🍾 Glass is 100% recyclable. Rinse before disposal."

    elif "metal" in message:
        return "🔩 Metals like cans can be recycled easily."

    elif "paper" in message:
        return "📄 Paper should be dry and clean for recycling."

    elif "compost" in message:
        return "🌿 Composting turns organic waste into fertilizer."

    elif "reduce waste" in message:
        return "🌱 Use reusable items, avoid plastic, recycle properly."

    # 🔹 AI RESPONSE (ONLY FOR OTHER QUESTIONS)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content

    except Exception:
        return "⚠️ AI not available. Please try later."