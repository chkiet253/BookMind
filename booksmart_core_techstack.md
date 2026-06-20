# BookSmart Platform — Core & Tech Stack

---

## Định nghĩa sản phẩm

**BookSmart** là nền tảng khám phá và nghiên cứu sách cá nhân hóa — không phải app đọc sách. Người dùng vẫn mua sách vật lý hoặc ebook ở nơi khác. Platform giải quyết 3 bài toán:

> *Tìm đúng sách → Hiểu sách trước khi mua → Hiểu bản thân qua quá trình đó*

---

## Core Jobs

### 1. Discovery — Tìm sách đúng với bản thân

Người dùng không cần biết mình muốn gì cụ thể. Có 3 entry point:

**Chat-to-search** (primary)
Người dùng chat tự nhiên: *"Tôi đang stress, muốn đọc gì nhẹ nhàng nhưng không nhảm"* → Semantic Query Parser Agent phân tích intent, mood, implicit constraints → trả về danh sách sách phù hợp với profile.

**Personality-based search**
Nếu đã có profile, hệ thống chủ động gợi ý mà không cần user search. Nếu chưa có profile, hệ thống học dần từ từng tương tác.

**Quote/passage search** (nâng cao)
Người dùng nhập câu văn nhớ mang máng → hệ thống tìm sách chứa câu đó hoặc sách có nội dung tương tự.
- Primary source: corpus quotes từ Goodreads, Wikiquote, blog review
- Vector search trên quote embeddings
- Fallback: semantic search theo chủ đề câu văn đó

---

### 2. Research — Q&A về sách trước khi mua

Người dùng có thể hỏi bất kỳ thứ gì về một cuốn sách cụ thể:

- *"Cuốn này có phù hợp với người mới bắt đầu không?"*
- *"Nội dung có nặng nề không hay nhẹ nhàng?"*
- *"Nhân vật chính có phức tạp không?"*
- *"Phần đầu sách nói về gì?"*

Agent trả lời dựa trên **review scraped + metadata**, không phải full content sách. Cần set expectation rõ với user: đây là tổng hợp từ cộng đồng độc giả, không phải từ tác giả.

Người dùng đọc sách giấy cũng có thể hỏi về phần đang đọc — agent trả lời dựa trên những gì review công khai đã đề cập về phần đó.

---

### 3. Passive Profiling — Hiểu người dùng qua mỗi tương tác

**Ngầm (auto):**
Mỗi search query, mỗi câu hỏi chat, mỗi lần click xem chi tiết, mỗi lần bỏ qua gợi ý → đều là signal. Hệ thống liên tục cập nhật `profile_vector` của user mà không cần user làm gì thêm.

**Chủ động (tùy chọn trong Profile):**
User có thể vào trang Profile → chọn làm bài test psychology, có 3 cấp độ:

| Level | Thời gian | Nội dung |
|-------|-----------|----------|
| Quick | ~5 phút | Sở thích đọc cơ bản, thể loại, mood |
| Standard | ~15 phút | Big Five personality traits |
| Deep | ~30 phút | MBTI + reading psychology + emotional style |

Kết quả được hiển thị lại cho user theo ngôn ngữ dễ hiểu — *"Bạn là người đọc thiên về cảm xúc, thích nhân vật phức tạp, tránh kết thúc bi kịch"* — tạo giá trị hai chiều: user hiểu bản thân hơn, hệ thống có data tốt hơn.

Profile có thể xem và chỉnh sửa bất cứ lúc nào. Hoàn toàn opt-in.

---

## Agent Architecture

```
Query / Chat input
        │
        ▼
┌─────────────────────────┐
│  Semantic Query Parser  │  LLM → extract intent, mood, constraints
│  Agent                  │  + inject user profile vector
└────────────┬────────────┘
             │
     ┌───────┴────────┐
     ▼                ▼
┌─────────┐    ┌──────────────┐
│ Hybrid  │    │ Metadata     │
│Retriever│    │ Filter       │
│(Qdrant) │    │(PostgreSQL)  │
└────┬────┘    └──────┬───────┘
     └────────┬───────┘
              ▼
┌─────────────────────────┐
│  Re-ranker +            │  Cross-encoder + profile boost
│  Personalization Agent  │  + diversity filter
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│  Book Reviewer Agent    │  Tổng hợp review → display
└─────────────────────────┘

Research Q&A:
User question → Reading Assistant Agent
             → RAG trên review corpus + metadata
             → Trả lời + ghi nhận interest signal
```

---

## Tech Stack

### Backend

| Layer | Tech | Lý do chọn |
|-------|------|------------|
| API Framework | **FastAPI** | Async native, Python ecosystem, tốt cho AI workload |
| Task Queue | **Celery + Redis** | Scraper chạy async, không block API |
| Auth | **FastAPI + JWT** | Simple, đủ cho MVP |

### Database

| Mục đích | Tech | Ghi chú |
|----------|------|---------|
| Primary data | **PostgreSQL** | Users, books, reviews, test results, profile |
| Vector search | **Qdrant** | Book embeddings, quote embeddings, user vectors |
| Cache / Session | **Redis** | Query cache, session, Celery broker |

### AI / LLM Layer

| Component | Tech | Ghi chú |
|-----------|------|---------|
| Agent orchestration | **LangChain** | Chain, memory, tool calling |
| LLM (dev/local) | **Ollama + Llama 3.2** | Free, chạy local, không tốn cost khi dev |
| LLM (production) | **OpenAI GPT-4o-mini** | Cost-effective, đủ mạnh cho production |
| Embeddings | **text-embedding-3-small** | OpenAI, 1536 dims, rẻ |
| Reranker | **CrossEncoder (sentence-transformers)** | Local, không tốn API call |

### Scraper Pipeline

| Component | Tech | Ghi chú |
|-----------|------|---------|
| Scraper | **Playwright + BeautifulSoup** | Handle JS-rendered pages (Tiki, Fahasa) |
| Scheduler | **Celery Beat** | Cron job scrape định kỳ |
| Rate limiting | **Redis + token bucket** | Tránh bị block |

### Frontend

| Layer | Tech | Lý do chọn |
|-------|------|------------|
| Web | **Next.js 14 (App Router)** | SSR tốt cho SEO, cùng codebase với app |
| Mobile (sau) | **Expo + React Native** | Share logic với web |
| UI Components | **shadcn/ui + Tailwind** | Fast, customizable |
| State | **Zustand** | Nhẹ, đủ cho MVP |
| Chat UI | **Vercel AI SDK** | Stream response, ready-made chat components |

### Infrastructure

| Stage | Setup | Stack |
|-------|-------|-------|
| Local dev | Docker Compose | Tất cả services trong 1 file, 1 lệnh chạy |
| Production MVP | **Railway** hoặc **Render** | Deploy nhanh, free tier đủ test |
| Production scale | **AWS / GCP** | Khi có traffic thật, migrate sau |

---

## Docker Compose Services (Local)

```yaml
services:
  api:          # FastAPI
  worker:       # Celery worker (scraper)
  beat:         # Celery beat (scheduler)
  db:           # PostgreSQL
  qdrant:       # Vector DB
  redis:        # Cache + broker
  ollama:       # Local LLM (dev only)
  frontend:     # Next.js
```

Một lệnh `docker compose up` → toàn bộ hệ thống chạy local.

---

## Data Flow tóm tắt

```
User input (text chat)
    → FastAPI
    → LangChain Agent (LLM: Ollama local / GPT-4o-mini prod)
    → Qdrant (vector search) + PostgreSQL (metadata filter)
    → Re-rank + personalize với profile vector
    → Stream response về frontend

Background:
    Celery Beat → Playwright scraper → PostgreSQL (raw reviews)
    → Embedding pipeline → Qdrant (review vectors)
```

---

## Roadmap MVP

**Phase 1 — Core search (4-6 tuần)**
- Seed database với 500-1000 cuốn sách phổ biến
- Scraper Tiki + Goodreads
- Chat-to-search với Semantic Query Parser
- Basic profile (lưu search history)

**Phase 2 — Research Q&A (2-3 tuần)**
- Review embedding pipeline
- Reading Assistant Agent
- Signal capture từ chat

**Phase 3 — Profiling & personalization (3-4 tuần)**
- Psychology test hub (3 levels)
- Profile vector update logic
- Personalized re-ranking

**Phase 4 — Quote search (sau MVP)**
- Quote corpus scraping
- Passage embedding + search

---

## Thứ gì KHÔNG làm (để giữ focus)

- Không phải app đọc sách — không cần render nội dung sách
- Không bán sách — chỉ link ra Tiki/Fahasa/Goodreads
- Không cần full book content — review + metadata là đủ cho Q&A
- Multimodal input (ảnh bìa) — để Phase 4+
