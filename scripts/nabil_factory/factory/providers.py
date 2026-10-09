from __future__ import annotations

# ==============================================================================
# 3. LLM INFERENCE ENGINE (FAIL-CLOSED)
# ==============================================================================
_AI_PROVIDER_COOLDOWNS: Dict[str, float] = {}
_LAST_LLM_PROVENANCE: Dict[str, Any] = {}


def get_last_llm_provenance() -> Dict[str, Any]:
    """Return metadata for the provider/model that actually answered last."""
    return dict(_LAST_LLM_PROVENANCE)


def _provider_keys() -> Dict[str, Optional[str]]:
    return {
        "openrouter": os.getenv("OPENROUTER_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY"),
    }


def _provider_order(preferred: str, keys: Dict[str, Optional[str]]) -> List[str]:
    """Primary provider first, then configured failover providers, no duplicates."""
    valid = ("groq", "openrouter", "openai")
    if preferred not in ("auto", *valid):
        raise RuntimeError(f"AI_PROVIDER_INVALID: {preferred}")

    if preferred == "auto":
        primary = next(
            (name for name in ("openrouter", "groq", "openai")
             if keys.get(name)), None)
    else:
        primary = preferred

    if not primary or not keys.get(primary):
        raise RuntimeError(
            f"AI_PROVIDER_NOT_CONFIGURED: provider={primary or preferred}")

    raw = os.getenv(
        "NABIL_FACTORY_AI_FAILOVER_PROVIDERS",
        "openrouter,openai,groq",
    )
    requested = [
        token.strip().lower() for token in raw.split(",") if token.strip()
    ]
    invalid = [name for name in requested if name not in valid]
    if invalid:
        raise RuntimeError(
            "AI_PROVIDER_FAILOVER_INVALID: " + ",".join(invalid))

    order = [primary]
    for name in requested:
        if name not in order and keys.get(name):
            order.append(name)
    return order


def _vision_provider_authorized(provider: str, vision_context: Dict[str, Any],
                                require_key: bool = True) -> bool:
    """Check explicit owner consent for one provider/source page."""
    consent_path = ROOT / "data/nabil_vision_consent.json"
    if not consent_path.exists():
        return False
    lesson_id = str(vision_context.get("lesson_id") or "")
    book_id = str(vision_context.get("book_id") or "")
    try:
        pdf_page = int(vision_context.get("pdf_page"))
    except (TypeError, ValueError):
        return False
    try:
        scopes = json.loads(
            consent_path.read_text(encoding="utf-8")
        ).get("approved_scopes", [])
    except Exception:
        return False

    for item in scopes:
        lesson_allowed = (
            item.get("all_lessons") is True
            or item.get("lesson_id") == lesson_id
            or bool(
                item.get("lesson_id_prefix")
                and lesson_id.startswith(item["lesson_id_prefix"])
            )
        )
        book_allowed = (
            item.get("all_books") is True
            or item.get("book_id") in (book_id, "*")
        )
        if (
            lesson_allowed
            and book_allowed
            and item.get("provider") == provider
            and int(item.get("pdf_start_page", 1)) <= pdf_page
            <= int(item.get("pdf_end_page", 1000000))
        ):
            if require_key and not os.getenv(f"{provider.upper()}_API_KEY"):
                return False
            return True
    return False


def _provider_request_config(provider: str, image_base64: Optional[str]):
    keys = _provider_keys()
    api_key = keys.get(provider)
    if not api_key:
        raise RuntimeError(
            f"AI_PROVIDER_NOT_CONFIGURED: provider={provider}")
    if provider == "openrouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
        model = (
            os.getenv("OPENROUTER_VISION_MODEL")
            if image_base64 else None
        ) or os.getenv(
            "OPENROUTER_TEXT_MODEL", "google/gemini-3.6-flash")
    elif provider == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
        model = (
            os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.8-27b")
            if image_base64
            else os.getenv(
                "GROQ_TEXT_MODEL", "llama-3.3-70b-versatile")
        )
    elif provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        model = (
            os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
            if image_base64
            else os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")
        )
    else:
        raise RuntimeError(f"AI_PROVIDER_INVALID: {provider}")
    return api_key, url, model


def _parse_rate_limit_wait_seconds(exc, detail: str,
                                   provider_attempt: int) -> float:
    """Return provider-declared wait exactly when available.

    Only use bounded exponential backoff when the provider supplied no
    Retry-After/header/message duration. This prevents a generic floor from
    turning a 1-5 second provider recovery into a needless long pause.
    """
    retry_header = str(exc.headers.get("Retry-After", "")).strip()
    try:
        retry_after = float(retry_header)
    except ValueError:
        retry_after = 0.0
    duration = re.search(
        r"(?i)(?:try again|retry)(?:\s+after|\s+in)?\s+"
        r"(?:(\d+(?:\.\d+)?)\s*h(?:ours?)?\s*)?"
        r"(?:(\d+(?:\.\d+)?)\s*m(?:in(?:utes?)?)?\s*)?"
        r"(?:(\d+(?:\.\d+)?)\s*s(?:ec(?:onds?)?)?)?",
        detail,
    )
    indicated = 0.0
    if duration and any(
            group is not None for group in duration.groups()):
        hours, minutes, seconds = duration.groups()
        indicated = (
            3600 * float(hours or 0)
            + 60 * float(minutes or 0)
            + float(seconds or 0)
        )
    explicit = max(retry_after, indicated)
    if explicit > 0:
        return explicit
    return min(5.0 * (2 ** max(0, provider_attempt - 1)), 120.0)


def _next_provider_or_wait(candidates: List[str],
                           cooldowns: Dict[str, float],
                           now_mono: float):
    """Pure scheduling helper: use an available provider or shortest cooldown."""
    available = [
        p for p in candidates if cooldowns.get(p, 0.0) <= now_mono
    ]
    if available:
        return "provider", available[0], 0.0
    earliest = min(candidates, key=lambda p: cooldowns.get(p, now_mono))
    wait = max(0.0, cooldowns.get(earliest, now_mono) - now_mono)
    return "wait", earliest, wait


def _sanitize_provider_error(exc):
    try:
        raw_body = exc.read(4096).decode("utf-8", errors="replace")
    except OSError:
        raw_body = ""
    content_type = str(
        exc.headers.get("Content-Type", "")
    ).split(";")[0].lower()
    detail, code = "", ""
    if raw_body:
        try:
            upstream = json.loads(raw_body)
            error = (
                upstream.get("error", upstream)
                if isinstance(upstream, dict) else {}
            )
            if isinstance(error, dict):
                detail = str(
                    error.get("message") or error.get("detail") or "")
                code = str(
                    error.get("code") or error.get("type") or "")
            elif isinstance(error, str):
                detail = error
        except ValueError:
            detail = re.sub(r"<[^>]+>", " ", raw_body)
    detail = re.sub(r"\s+", " ", detail).strip()
    code = re.sub(r"\s+", " ", code).strip()
    if not detail:
        detail = (
            "Empty or unrecognized provider response "
            f"(content_type={content_type or 'not-provided'})"
        )
    for secret_name in (
        "OPENROUTER_API_KEY", "OPENAI_API_KEY", "GROQ_API_KEY"
    ):
        secret = os.getenv(secret_name, "")
        if secret and len(secret) >= 8:
            detail = detail.replace(secret, "[REDACTED]")
            code = code.replace(secret, "[REDACTED]")
    detail = re.sub(
        r"(?i)\b(?:sk-or-v1-|sk-)[a-z0-9_-]{8,}",
        "[REDACTED]", detail)
    code = re.sub(
        r"(?i)\b(?:sk-or-v1-|sk-)[a-z0-9_-]{8,}",
        "[REDACTED]", code)
    return detail, code


def execute_llm_completion(
        prompt: str,
        json_mode: bool = True,
        temperature: float = 0.0,
        image_base64: Optional[str] = None,
        vision_context: Optional[Dict[str, Any]] = None,
        preferred_provider_override: Optional[str] = None,
        excluded_providers: Optional[set] = None,
        operation: str = "provider_call",
        unit_id: Optional[str] = None) -> str:
    """Execute with rate-limit failover while preserving source consent.

    A 429 never sleeps on one provider while another configured, explicitly
    authorized provider is available. If every candidate is cooling down, wait
    only for the shortest cooldown; if that shortest wait is still too long,
    fail fast so durable checkpoints can be resumed later instead of burning a
    Railway session idling.
    """
    global _LAST_LLM_PROVENANCE

    preferred = (
        preferred_provider_override
        or os.getenv("NABIL_FACTORY_AI_PROVIDER", "auto")
    ).strip().lower()
    keys = _provider_keys()
    candidates = _provider_order(preferred, keys)

    # Source images may move between providers ONLY when the owner explicitly
    # approved that exact lesson/book/page for each fallback provider.
    if image_base64:
        if vision_context is None:
            candidates = candidates[:1]
        else:
            candidates = [
                p for p in candidates
                if _vision_provider_authorized(
                    p, vision_context, require_key=True)
            ]
            if not candidates:
                raise RuntimeError(
                    "VISION_SHARING_NOT_AUTHORIZED: no configured provider "
                    "is approved for this source page")
    if excluded_providers:
        excluded = {str(p).strip().lower() for p in excluded_providers}
        candidates = [p for p in candidates if p not in excluded]
        if not candidates:
            raise RuntimeError(
                "AI_PROVIDER_POOL_EXHAUSTED_AFTER_JSON_FAILURES:"
                + ",".join(sorted(excluded)))

    primary = candidates[0]
    progress(
        "AI_PROVIDER_FAILOVER_POOL",
        primary=primary,
        candidates=candidates,
        image_request=bool(image_base64),
        vision_context=vision_context if image_base64 else None,
    )

    max_requests = max(
        3, min(30, int(os.getenv(
            "NABIL_FACTORY_MAX_FAILOVER_REQUESTS", "12"))))
    # A temporary 429 on the last healthy provider must not discard a lesson
    # that has already completed expensive OCR/vision work.  Keep this bounded
    # and configurable; long quota quarantines still lose to the shortest
    # healthy-provider cooldown selected by _next_provider_or_wait().
    max_all_wait = max(
        0.0, min(1800.0, float(os.getenv(
            "NABIL_FACTORY_MAX_ALL_PROVIDER_WAIT_SECONDS", "30"))))
    provider_attempts = {p: 0 for p in candidates}
    permanent_quarantined = set()
    total_requests = 0

    while total_requests < max_requests:
        now_mono = time.monotonic()
        mode, provider, wait_seconds = _next_provider_or_wait(
            candidates, _AI_PROVIDER_COOLDOWNS, now_mono)

        if mode == "wait":
            if wait_seconds > max_all_wait:
                remaining = {
                    p: round(max(
                        0.0,
                        _AI_PROVIDER_COOLDOWNS.get(p, now_mono)
                        - now_mono), 2)
                    for p in candidates
                }
                progress(
                    "AI_ALL_PROVIDERS_COOLING_DOWN_FAIL_FAST",
                    candidates=candidates,
                    remaining_seconds=remaining,
                    shortest_provider=provider,
                    shortest_wait_seconds=round(wait_seconds, 2),
                    max_all_provider_wait_seconds=max_all_wait,
                )
                raise ProviderTransientError(
                    "AI_ALL_PROVIDERS_COOLING_DOWN",
                    retry_after_seconds=max(1, int(math.ceil(wait_seconds))),
                    operation=operation,
                    unit_id=unit_id or operation,
                    reason=(
                        f"shortest_provider={provider} "
                        f"wait_seconds={wait_seconds:.1f}"
                    ),
                    remaining=remaining,
                )
            progress(
                "AI_ALL_PROVIDERS_COOLING_DOWN_WAIT_SHORTEST",
                provider=provider,
                wait_seconds=round(wait_seconds, 2),
                candidates=candidates,
            )
            time.sleep(wait_seconds + 0.25)
            continue

        provider_attempts[provider] += 1
        total_requests += 1
        api_key, url, model = _provider_request_config(
            provider, image_base64)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "NABIL-AI-Lesson-Factory/1.0",
        }
        messages_content = [{"type": "text", "text": prompt}]
        if image_base64:
            messages_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_base64}"
                },
            })
        payload = {
            "model": model,
            "messages": [{
                "role": "user",
                "content": (
                    messages_content if image_base64 else prompt)
            }],
            "temperature": temperature,
            # OpenRouter may otherwise assume a very large provider maximum
            # (for Gemini 3.6 Flash this can be 65k+ output tokens), which can
            # trigger a 402 credit preflight even for a tiny JSON response.
            # Keep factory calls bounded and configurable.
            "max_tokens": max(
                256,
                min(
                    8192,
                    int(os.getenv(
                        "NABIL_FACTORY_VISION_MAX_OUTPUT_TOKENS"
                        if image_base64
                        else "NABIL_FACTORY_TEXT_MAX_OUTPUT_TOKENS",
                        "2048" if image_base64 else "4096",
                    )),
                ),
            ),
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"].strip()
                if content.startswith("```"):
                    content = re.sub(
                        r"^```(?:json)?\s*|\s*```$",
                        "", content, flags=re.I).strip()
                _LAST_LLM_PROVENANCE = {
                    "provider": provider,
                    "model": model,
                    "primary_provider": primary,
                    "used_failover": provider != primary,
                    "request_index": total_requests,
                    "provider_attempt": provider_attempts[provider],
                    "completed_at": now(),
                }
                if provider != primary:
                    progress(
                        "AI_PROVIDER_FAILOVER_SUCCESS",
                        primary=primary,
                        actual_provider=provider,
                        model=model,
                        request_index=total_requests,
                    )
                return content
        except urllib.error.HTTPError as exc:
            detail, code = _sanitize_provider_error(exc)
            if exc.code == 429:
                terminal_quota_tokens = (
                    "credit_balance_exhausted",
                    "insufficient_quota",
                    "billing_hard_limit_reached",
                    "billing_not_active",
                    "payment_required",
                )
                combined_error = (code + " " + detail).casefold()
                if any(token in combined_error
                       for token in terminal_quota_tokens):
                    quarantine_seconds = 86400.0
                    _AI_PROVIDER_COOLDOWNS[provider] = (
                        time.monotonic() + quarantine_seconds)
                    permanent_quarantined.add(provider)
                    ready_alternatives = [
                        p for p in candidates
                        if p != provider
                        and _AI_PROVIDER_COOLDOWNS.get(p, 0.0)
                        <= time.monotonic()
                    ]
                    progress(
                        "AI_PROVIDER_QUOTA_EXHAUSTED_FAILOVER",
                        provider=provider,
                        model=model,
                        provider_attempt=provider_attempts[provider],
                        total_requests=total_requests,
                        quarantine_seconds=quarantine_seconds,
                        ready_alternatives=ready_alternatives,
                        provider_code=code[:80],
                    )
                    if len(permanent_quarantined) >= len(candidates):
                        raise ProviderUnavailableError(
                            "ALL_AUTHORISED_PROVIDERS_QUARANTINED",
                            operation=operation,
                            unit_id=unit_id or operation,
                            reason="billing_or_credit_exhausted",
                        )
                    continue

                cooldown = _parse_rate_limit_wait_seconds(
                    exc, detail, provider_attempts[provider])
                max_provider_wait = max(
                    30.0, min(3600.0, float(os.getenv(
                        "NABIL_FACTORY_MAX_RATE_LIMIT_WAIT_SECONDS",
                        "1800"))))
                if cooldown > max_provider_wait:
                    # Treat a very long provider cooldown as unavailable for
                    # this run; the other providers still get an immediate try.
                    cooldown = max_provider_wait
                _AI_PROVIDER_COOLDOWNS[provider] = (
                    time.monotonic() + cooldown)
                next_now = time.monotonic()
                ready_alternatives = [
                    p for p in candidates
                    if p != provider
                    and _AI_PROVIDER_COOLDOWNS.get(p, 0.0) <= next_now
                ]
                progress(
                    "AI_PROVIDER_RATE_LIMIT_FAILOVER",
                    provider=provider,
                    model=model,
                    provider_attempt=provider_attempts[provider],
                    total_requests=total_requests,
                    cooldown_seconds=round(cooldown, 2),
                    ready_alternatives=ready_alternatives,
                    provider_code=code[:80],
                )
                continue

            if exc.code in (408, 425, 500, 502, 503, 504):
                transient_cooldown = _parse_rate_limit_wait_seconds(
                    exc, detail, provider_attempts[provider])
                transient_cooldown = max(
                    1.0, min(120.0, float(transient_cooldown)))
                _AI_PROVIDER_COOLDOWNS[provider] = (
                    time.monotonic() + transient_cooldown)
                progress(
                    "AI_PROVIDER_TRANSIENT_FAILOVER",
                    provider=provider,
                    model=model,
                    http_status=exc.code,
                    cooldown_seconds=transient_cooldown,
                    provider_code=code[:80],
                )
                continue

            if exc.code == 402:
                affordable = re.search(
                    r"can only afford\s+(\d+)",
                    detail, re.I)
                if affordable:
                    affordable_tokens = int(affordable.group(1))
                    requested_tokens = int(payload.get("max_tokens") or 0)
                    # OpenRouter credit preflight can reject a request only
                    # because its configured output ceiling is a few tokens
                    # above the currently affordable amount. Do not quarantine
                    # a healthy provider for one hour. Adapt the ceiling with a
                    # safety margin and retry the SAME source unit.
                    if 512 <= affordable_tokens < requested_tokens:
                        adapted_tokens = max(
                            512, min(requested_tokens - 1,
                                     affordable_tokens - 64))
                        env_name = (
                            "NABIL_FACTORY_VISION_MAX_OUTPUT_TOKENS"
                            if image_base64
                            else "NABIL_FACTORY_TEXT_MAX_OUTPUT_TOKENS"
                        )
                        os.environ[env_name] = str(adapted_tokens)
                        progress(
                            "AI_PROVIDER_CREDIT_CAP_ADAPTED",
                            provider=provider,
                            model=model,
                            requested_max_tokens=requested_tokens,
                            affordable_max_tokens=affordable_tokens,
                            adapted_max_tokens=adapted_tokens,
                            image_request=bool(image_base64),
                        )
                        continue

            if exc.code == 402 and "in-flight requests" in detail.casefold():
                transient_cooldown = 3.0
                _AI_PROVIDER_COOLDOWNS[provider] = (
                    time.monotonic() + transient_cooldown)
                progress(
                    "AI_PROVIDER_INFLIGHT_LIMIT_RETRY",
                    provider=provider,
                    model=model,
                    http_status=exc.code,
                    cooldown_seconds=transient_cooldown,
                    detail=detail[:240],
                )
                continue

            if exc.code in (400, 422):
                raise NeedsAttentionError(
                    f"AI_PROVIDER_REQUEST_NEEDS_ATTENTION:http_status={exc.code}",
                    operation=operation,
                    unit_id=unit_id or operation,
                    reason=detail[:360],
                ) from None

            if exc.code in (401, 402, 403, 404):
                quarantine_seconds = 3600.0
                _AI_PROVIDER_COOLDOWNS[provider] = (
                    time.monotonic() + quarantine_seconds)
                permanent_quarantined.add(provider)
                ready_alternatives = [
                    p for p in candidates
                    if p != provider
                    and p not in permanent_quarantined
                    and _AI_PROVIDER_COOLDOWNS.get(p, 0.0)
                    <= time.monotonic()
                ]
                progress(
                    "AI_PROVIDER_UNAVAILABLE_FAILOVER",
                    provider=provider,
                    model=model,
                    http_status=exc.code,
                    quarantine_seconds=quarantine_seconds,
                    ready_alternatives=ready_alternatives,
                    provider_code=code[:80],
                    detail=detail[:240],
                )
                if len(permanent_quarantined) >= len(candidates):
                    raise ProviderUnavailableError(
                        "ALL_AUTHORISED_PROVIDERS_QUARANTINED",
                        operation=operation,
                        unit_id=unit_id or operation,
                        reason=detail[:360],
                    ) from None
                continue

            reason = detail[:360]
            progress(
                "AI_PROVIDER_REQUEST_REJECTED",
                provider=provider,
                model=model,
                http_status=exc.code,
                provider_code=code[:80],
                detail=reason,
            )
            raise NeedsAttentionError(
                "AI_PROVIDER_HTTP_ERROR: "
                f"provider={provider} model={model} "
                f"http_status={exc.code} "
                f"provider_code={code[:80]} detail={reason}",
                operation=operation,
                unit_id=unit_id or operation,
                reason=reason,
            ) from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            _AI_PROVIDER_COOLDOWNS[provider] = time.monotonic() + 10.0
            progress(
                "AI_PROVIDER_NETWORK_FAILOVER",
                provider=provider,
                model=model,
                error_type=type(exc).__name__,
                cooldown_seconds=10.0,
            )
            continue

    now_mono = time.monotonic()
    usable = [p for p in candidates if p not in permanent_quarantined]
    if not usable:
        raise ProviderUnavailableError(
            "AI_PROVIDER_FAILOVER_EXHAUSTED_NO_USABLE_PROVIDER",
            operation=operation,
            unit_id=unit_id or operation,
            reason=f"requests={total_requests}",
        )
    remaining = {
        p: round(max(
            0.0, _AI_PROVIDER_COOLDOWNS.get(p, 0.0) - now_mono), 2)
        for p in usable
    }
    positive_waits = [v for v in remaining.values() if v > 0]
    shortest_wait = min(positive_waits) if positive_waits else 1.0
    raise ProviderTransientError(
        "AI_PROVIDER_FAILOVER_EXHAUSTED",
        retry_after_seconds=max(1, int(math.ceil(shortest_wait))),
        operation=operation,
        unit_id=unit_id or operation,
        reason=f"requests={total_requests}",
        remaining=remaining,
    )
