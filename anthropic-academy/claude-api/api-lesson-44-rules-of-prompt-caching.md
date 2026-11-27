# Lesson 44: Rules of prompt caching

**Curs:** Building with the Claude API (Anthropic Academy — Lliçó 44 de 67)  
**Data:** 2026-11-27

## Conceptes clau
- **TTL i coincidència exacta:** La memòria cau dura 5 minuts (o 1 hora opcional) i requereix que tot el prefix fins al *breakpoint* sigui idèntic.
- **Format *longhand* obligatori:** Cal fer servir blocs estructurats amb `"cache_control": {"type": "ephemeral"}` (màxim 4 *breakpoints* per petició).
- **Ordre d'avaluació:** `tools` → `system` → `messages`. Posar *breakpoints* a les eines i al *system prompt* evita invalidar-los quan canvia l'historial.
- **Llindar mínim:** Si el prefix no arriba al mínim de *tokens* del model (ex. 4.096 *tokens* a Haiku 4.5), l'API ho processa sense memòria cau (`cache_creation_input_tokens == 0` i `cache_read_input_tokens == 0`).

## Estructura en Python (`cache_control`)
```python
response = client.messages.create(
    model=model,
    max_tokens=1000,
    # 1. Es processa primer: eines
    tools=[
        {
            **my_tool_schema,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    # 2. Es processa segon: system prompt
    system=[
        {
            "type": "text",
            "text": long_system_instructions,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    # 3. Es processa tercer: missatges
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": large_static_context,
                    "cache_control": {"type": "ephemeral"},
                },
                {
                    "type": "text",
                    "text": "Quina és la conclusió principal?",
                },
            ],
        }
    ],
)

print(response.usage.cache_creation_input_tokens)
print(response.usage.cache_read_input_tokens)
```
