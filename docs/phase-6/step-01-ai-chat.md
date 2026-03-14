# Phase 6: AI 채팅 모듈

## 상태: 완료

## 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | /api/v1/ai/chat | AI 채팅 (SSE) |

## 작업 내용

- [x] ai/router.py — SSE 스트리밍 엔드포인트
- [x] ai/service.py — stream_chat() async generator
- [x] providers/base.py — BaseAiProvider 추상 클래스
- [x] providers/anthropic.py — Claude 구현
- [x] providers/openai.py — GPT 구현
- [x] providers/gemini.py — Gemini 구현
- [x] httpx 비동기 호출
