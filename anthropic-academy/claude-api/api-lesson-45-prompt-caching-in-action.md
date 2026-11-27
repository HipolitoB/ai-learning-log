# Lesson 45: Prompt caching in action

**Curs:** Building with the Claude API (Anthropic Academy — Lliçó 45 de 67)  
**Data:** 2026-11-27

## Conceptes clau
- **Clonació segura d'eines (*shallow copy*):** Clonar la llista `tools` (`tools.copy()`) i el seu últim diccionari (`tools_clone[-1].copy()`) abans d'assignar `"cache_control": {"type": "ephemeral"}` evita mutar els esquemes originals si es reordenen o reutilitzen en altres parts del codi.
- **Conversió del *system prompt* a bloc estructurat:** Si `system` arriba com a cadena de text simple (`str`), es transforma en una llista amb un únic bloc `{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}`.
- **Invalidació granular (`tools` → `system` → `messages`):** Modificar un component posterior (ex. el *system prompt*) conserva la lectura en memòria cau dels components anteriors (ex. `tools`) sempre que aquests assoleixin per si sols el llindar mínim de *tokens*.
- **Monitoratge amb `response.usage`:**
  - **1a petició (Cache Miss / Write):** `cache_creation_input_tokens` reflecteix els *tokens* escrits a la memòria cau.
  - **Peticions següents (Cache Hit / Read):** `cache_read_input_tokens` mostra els *tokens* recuperats directament de la memòria cau (reiniciant el comptador de 5 minuts sense cost extra).
  - **Invalidació parcial:** Si canvia `system` però `tools` es manté intacte, l'API combina `cache_read_input_tokens` (eines) i `cache_creation_input_tokens` (nou *system prompt*).

## Implementació en Python (`chat` amb *caching*)
```python
def chat(messages, system=None, temperature=1.0, stop_sequences=[], tools=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if tools:
        tools_clone = tools.copy()
        last_tool = tools_clone[-1].copy()
        last_tool["cache_control"] = {"type": "ephemeral"}
        tools_clone[-1] = last_tool
        params["tools"] = tools_clone

    if system:
        params["system"] = [
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"},
            }
        ]

    return client.messages.create(**params)
```
