---
name: minimax-text-to-speech
description: Generate speech from text with MiniMax through synchronous HTTP, asynchronous, streaming, or WebSocket workflows across the global and mainland China API regions.
---

# MiniMax Text to Speech

Generate spoken audio from text with the MiniMax T2A APIs. Choose the request style that fits the input length and latency requirement, send the request to the region that issued the API key, and validate every response before reporting or saving audio.

## Core Principle

**Never report audio as generated until the API returns a successful status and audio data or a completed file.**

Do not invent audio, URLs, task identifiers, or completion states. Treat a successful HTTP status as transport success only; the API result is successful only when `base_resp.status_code` is `0` and the operation-specific completion checks also pass.

## When to Use This Skill

Use this skill when the user wants to:

- Turn short text into speech immediately
- Stream generated speech with low latency
- Synthesize long text as an asynchronous task
- Receive speech chunks over a WebSocket connection
- Control the voice, speed, volume, pitch, pronunciation, language, audio format, or audio effects
- Generate MP3, WAV, FLAC, or PCM audio

Do not use this skill to clone or design a voice. Those are separate operations. This skill can use an existing system or custom `voice_id` for synthesis.

## Required Setup

- Store the API key in `MINIMAX_API_KEY`; never put it in a prompt, request body, source file, or log.
- Send `Authorization: Bearer <MINIMAX_API_KEY>`.
- Send `Content-Type: application/json` for HTTP requests.
- Use the API hostname from the same region as the API key.

## Regional Endpoints

| Operation | Global | Mainland China |
|---|---|---|
| Synchronous HTTP | `POST https://api.minimax.io/v1/t2a_v2` | `POST https://api.minimaxi.com/v1/t2a_v2` |
| Asynchronous create | `POST https://api.minimax.io/v1/t2a_async_v2` | `POST https://api.minimaxi.com/v1/t2a_async_v2` |
| Asynchronous query | `POST https://api.minimax.io/v1/query/t2a_async_query_v2` | `POST https://api.minimaxi.com/v1/query/t2a_async_query_v2` |
| WebSocket | `WSS wss://api.minimax.io/ws/v1/t2a_v2` | `WSS wss://api.minimaxi.com/ws/v1/t2a_v2` |

Do not send a key from one region to the other region's hostname.

## Models

Use `speech-2.8-hd` by default unless the user or an existing application configuration requires another supported model.

| Model |
|---|
| `speech-2.8-hd` |
| `speech-2.8-turbo` |
| `speech-2.6-hd` |
| `speech-2.6-turbo` |
| `speech-02-hd` |
| `speech-02-turbo` |
| `speech-01-hd` |
| `speech-01-turbo` |

## Choose an Operation

| Need | Operation |
|---|---|
| A complete response for ordinary text | Synchronous HTTP |
| Incremental audio in an HTTP response | Synchronous HTTP with `stream: true` |
| Long-running generation that can be polled | Asynchronous create, then asynchronous query |
| A persistent low-latency conversation | WebSocket |

Keep one region for the full workflow. In particular, create and query an asynchronous task on the same hostname.

## Synchronous HTTP

Send `POST /v1/t2a_v2`. The required fields are `model` and `text`.

```json
{
  "model": "speech-2.8-hd",
  "text": "Welcome. Your audio is ready.",
  "stream": false,
  "language_boost": "auto",
  "output_format": "hex",
  "voice_setting": {
    "voice_id": "English_expressive_narrator",
    "speed": 1,
    "vol": 1,
    "pitch": 0
  },
  "pronunciation_dict": {
    "tone": []
  },
  "audio_setting": {
    "sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3",
    "channel": 1
  },
  "voice_modify": {
    "pitch": 0,
    "intensity": 0,
    "timbre": 0
  },
  "subtitle_enable": false
}
```

### Request Fields

| Field | Required | Purpose |
|---|---|---|
| `model` | Yes | Selects one of the supported speech models. |
| `text` | Yes | Supplies the text to synthesize. |
| `stream` | No | Requests incremental output when `true`. |
| `language_boost` | No | Selects a language or uses `auto` detection. |
| `output_format` | No | Selects `hex` or `url` for non-streaming output. |
| `voice_setting` | No | Sets `voice_id`, `speed`, `vol`, and `pitch`. |
| `pronunciation_dict` | No | Supplies pronunciation replacements in `tone`. |
| `audio_setting` | No | Sets `sample_rate`, `bitrate`, `format`, and `channel`. |
| `voice_modify` | No | Adjusts pitch, intensity, timbre, and supported sound effects. |
| `subtitle_enable` | No | Requests subtitle data when the selected model and operation support it. |

Only send fields required for the user's request. Preserve any application-level voice and audio defaults instead of silently changing them.

### Parse the Response

For a non-streaming response:

1. Require `base_resp.status_code == 0`. Otherwise surface `base_resp.status_msg` as the API error.
2. Require a non-null `data` object.
3. Require `data.status == 2` before treating synthesis as complete.
4. Read `data.audio` according to `output_format`:
   - For `hex`, decode the hexadecimal string to bytes and write those bytes using the extension selected in `audio_setting.format`.
   - For `url`, download the URL before it expires if the user needs a persistent file.
5. Do not write the literal hexadecimal string into an audio file.

For HTTP streaming, inspect every event's `base_resp.status_code`, decode each non-empty `data.audio` chunk from hexadecimal, append chunks in order, and finish only after the response indicates completion. Streaming output uses hexadecimal audio chunks.

## Asynchronous Speech

Use the asynchronous workflow when the caller should submit work and poll for completion.

### Create the Task

Send `POST /v1/t2a_async_v2` with `model` and `text`. The operation also accepts `voice_setting`, `audio_setting`, `language_boost`, `pronunciation_dict`, and `voice_modify`.

```json
{
  "model": "speech-2.8-hd",
  "text": "This longer passage will be generated asynchronously.",
  "language_boost": "auto",
  "voice_setting": {
    "voice_id": "English_expressive_narrator",
    "speed": 1,
    "vol": 1,
    "pitch": 0
  },
  "audio_setting": {
    "sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3",
    "channel": 1
  }
}
```

Require `base_resp.status_code == 0`, then retain the returned `task_id`. Do not claim that audio exists merely because task creation succeeded.

### Query the Task

Send `POST /v1/query/t2a_async_query_v2` with the returned identifier:

```json
{
  "task_id": "<TASK_ID>"
}
```

Require `base_resp.status_code == 0`, then inspect the task status. Continue polling while it is processing, stop with an error if it fails or expires, and proceed only after success. When a successful result provides a file identifier, use the corresponding authenticated file-retrieval workflow and save the downloaded bytes before its temporary URL expires.

Use bounded polling with backoff. Preserve `task_id` for diagnostics, but do not expose authorization material.

## WebSocket Speech

Connect to `/ws/v1/t2a_v2` over WSS and include the Bearer authorization header during the handshake.

The event sequence is:

1. Wait for `connected_success` and require `base_resp.status_code == 0`.
2. Send `task_start` with `model`, `voice_setting`, `audio_setting`, and any required language or pronunciation options.
3. Wait for `task_started`.
4. Send one or more `task_continue` events, each carrying `text`.
5. For every received audio event, require `base_resp.status_code == 0`, decode `data.audio` from hexadecimal, and append the bytes in arrival order.
6. Stop receiving the current segment when `is_final` is true.
7. Send `task_finish`, wait for `task_finished`, and close the socket cleanly.

Example client events:

```json
{
  "event": "task_start",
  "model": "speech-2.8-hd",
  "voice_setting": {
    "voice_id": "English_expressive_narrator",
    "speed": 1,
    "vol": 1,
    "pitch": 0
  },
  "audio_setting": {
    "sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3",
    "channel": 1
  }
}
```

```json
{
  "event": "task_continue",
  "text": "Generate this sentence now."
}
```

Treat `task_failed`, a non-zero `base_resp.status_code`, an unexpected close, or a missing final event as failure. Never present partial bytes as a complete file without telling the user that the stream was interrupted.

## Audio Formats

The configured output formats are:

| Format | Handling |
|---|---|
| `mp3` | Write decoded bytes to an `.mp3` file. |
| `wav` | Write decoded bytes to a `.wav` file. |
| `flac` | Write decoded bytes to a `.flac` file. |
| `pcm` | Write raw decoded PCM bytes and preserve sample rate, channel, and sample-width metadata separately. |

Operation-specific format support differs. WebSocket and streaming requests should use a format supported by that transport; asynchronous requests support MP3, WAV, and FLAC. If the service rejects a format, choose another supported format only with the user's consent when that changes the requested deliverable.

## Validation and Error Handling

Before reporting success, verify all applicable conditions:

- `base_resp.status_code` is `0`.
- `data.status` indicates completion when that field is present.
- `data.audio` is non-empty for direct or streamed output.
- All hexadecimal audio data decodes without an error.
- An asynchronous task reaches success and its file is retrieved.
- A WebSocket workflow reaches its final event.
- The saved file is non-empty and uses the requested format.

| Failure | Response |
|---|---|
| Non-zero `base_resp.status_code` | Surface `base_resp.status_msg`; do not parse the payload as successful audio. |
| Null or missing `data` | Report that the service returned no audio result. |
| Invalid hexadecimal audio | Stop; do not save corrupted bytes as completed audio. |
| Asynchronous failure or expiry | Stop polling and report the final task status. |
| Interrupted WebSocket | Preserve partial output only if the user wants it and label it incomplete. |
| Wrong-region authorization | Retry only with the endpoint that matches the API key's region. |

## Recommended Workflow

1. Confirm the text, output format, and desired voice.
2. Choose synchronous HTTP, HTTP streaming, asynchronous generation, or WebSocket.
3. Select the matching regional endpoint.
4. Use `speech-2.8-hd` unless another supported model is explicitly required.
5. Build the smallest request body that satisfies the request.
6. Send the authenticated request without logging the API key.
7. Validate `base_resp.status_code`, the operation status, and the returned audio or file.
8. Decode or download the audio and confirm that the saved file is non-empty.
9. Report the actual file path, format, and whether the result was complete.

## Reference

- Global synchronous HTTP: https://platform.minimax.io/docs/api-reference/speech-t2a-http
- Global asynchronous create: https://platform.minimax.io/docs/api-reference/speech-t2a-async-create
- Global WebSocket: https://platform.minimax.io/docs/api-reference/speech-t2a-websocket
- Mainland China synchronous HTTP: https://platform.minimaxi.com/docs/api-reference/speech-t2a-http
- Mainland China asynchronous create: https://platform.minimaxi.com/docs/api-reference/speech-t2a-async-create
- Mainland China WebSocket: https://platform.minimaxi.com/docs/api-reference/speech-t2a-websocket

**Credit:** Based on the MiniMax text-to-speech API reference.
