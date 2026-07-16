import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import settings
from app.agentic_core.state import SearchState, ParsedIntent


# LLM setup
llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    api_key=settings.LLM_API_KEY,
    temperature=0,
)

SYSTEM_PROMPT = """
Bạn là AI chuyên phân tích yêu cầu tìm sách của người dùng.

Nhiệm vụ: Extract thông tin từ câu query và trả về JSON vói format sau:
{
    "genres": [],        // list thể loại sách, ví dụ: ["trinh thám", "tâm lý"]
    "mood": null,        // tâm trạng/cảm xúc mong muốn, ví dụ: "nhẹ nhàng", "hồi hộp"
    "pages_min": null,   // số trang tối thiểu (integer hoặc null)
    "pages_max": null,   // số trang tối đa (integer hoặc null)
    "language": null     // ngôn ngữ: "vi", "en" hoặc null nếu không xác định
}
Quy tắc:
- Chỉ trả về JSON thuần, không giải thích thêm
- Nếu không xác định được field nào thì để null
- genres phải là tiếng Việt
- "ngắn" → pages_max: 200, "dài" → pages_min: 400
 
Ví dụ:
Query: "tìm truyện trinh thám ngắn thôi"
Output: {"genres": ["trinh thám"], "mood": null, "pages_min": null, "pages_max": 200, "language": null}
 
Query: "sách tâm lý nhẹ nhàng tiếng Anh"
Output: {"genres": ["tâm lý"], "mood": "nhẹ nhàng", "pages_min": null, "pages_max": null, "language": "en"}
"""
async def query_parser_node(state: SearchState) -> dict:
    """
    LangGraph node — nhận SearchState, trả về dict update state.
    Chỉ update field `parsed_intent`, các field khác giữ nguyên.
    """
    try:
        response = await llm.aiinvoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=state["query"]),
        ])

    except:
        pass