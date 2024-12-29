from typing import Annotated

from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.templating import Jinja2Templates
from youtube_transcript_api import YouTubeTranscriptApi

router = APIRouter(prefix="/summary")
templates = Jinja2Templates(directory="templates")

usage_key_words = {"need", "using", "use", "have"}
tool_key_words = {"tool", "ratchet", "millimeter",
                  "drive", "socket", "extension", "hex", "kit"}
process_key_words = {"started", "remove", "disconnect",
                     "connect", "pull", "push", "break", "we", "install", "stopped", "start", "stop"}


def do_the_thing(video_id: str) -> list[str]:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    grouped_lines = []
    transcript_len = len(transcript)

    i = 0
    while i < transcript_len:
        line = transcript[i]
        text = line.get("text", None)
        start = line.get("start", None)
        duration = line.get("duration", None)

        if text is None or start is None or duration is None:
            print("Unable to process line: {line}")
            continue

        group_end = start + duration
        group = [text]
        for j in range(i + 1, transcript_len):
            maybe_next_line = transcript[j]
            maybe_next_line_text = maybe_next_line.get("text", None)
            maybe_next_line_start = maybe_next_line.get("start", None)

            if maybe_next_line_text is None or maybe_next_line_start is None:
                print("Unable to process line: {maybe_next_line}")
                continue

            if group_end < maybe_next_line_start:
                break
            else:
                group.append(maybe_next_line_text)
                i += 1

        grouped_lines.append(" ".join(group))
        i += 1

    used_lines = []
    step_lines = []
    tool_lines = []
    process_lines = []

    for line in grouped_lines:
        words = line.split()
        should_use = False
        for word in words:
            if word in usage_key_words:
                should_use = True
            if word in tool_key_words and line not in tool_lines:
                tool_lines.append(line)
                should_use = True
            if word in process_key_words and line not in process_lines:
                process_lines.append(line)
                should_use = True

        if should_use:
            used_lines.append(line)

    return {
        "tools": tool_lines,
        "steps": process_lines,
        "metadata": {
            "compressionRatio": round((len(used_lines) / len(grouped_lines)) * 100, 2),
        }
    }


@router.get("/")
def summarize(request: Request, v: Annotated[str | None, Query(example="-qbqWL7aP_g", description="YouTube video ID", min_length=1)] = None):
    if v is None or len(v) == 0:
        raise HTTPException(status_code=400, detail="Invalid video ID")

    summary = do_the_thing(v)

    return templates.TemplateResponse(request=request, name="summary.html", context={"video_id": v, "summary": summary})
