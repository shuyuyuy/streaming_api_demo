from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import asyncio
import time
import json

app = FastAPI(
    title="FastAPI Streaming API Demo",
    description="演示如何使用 FastAPI 实现流式 API",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
async def root():
    return '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastAPI Streaming API Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        main {
            padding: 30px;
        }
        
        .demo-section {
            margin: 30px 0;
            padding: 25px;
            border-radius: 10px;
            background: #f8f9fa;
            border-left: 5px solid #4facfe;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .demo-section:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .demo-section h2 {
            color: #4facfe;
            margin-bottom: 15px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .demo-section h2::before {
            content: "💡";
            font-size: 1.2em;
        }
        
        .controls {
            margin: 20px 0;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        button {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(79, 172, 254, 0.6);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        button:nth-child(2) {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        }
        
        button:nth-child(2):hover {
            box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
        }
        
        input[type="text"] {
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 16px;
            width: 350px;
            transition: all 0.3s ease;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #4facfe;
            box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.2);
        }
        
        .stream-output {
            margin-top: 20px;
            padding: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            height: 250px;
            overflow-y: scroll;
            background: white;
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            line-height: 1.8;
        }
        
        .stream-output::-webkit-scrollbar {
            width: 8px;
        }
        
        .stream-output::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        .stream-output::-webkit-scrollbar-thumb {
            background: #4facfe;
            border-radius: 4px;
        }
        
        .stream-output::-webkit-scrollbar-thumb:hover {
            background: #3a8fe9;
        }
        
        .explanation {
            margin-top: 20px;
            padding: 20px;
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border-radius: 8px;
            border-left: 4px solid #ffc107;
        }
        
        .explanation h3 {
            color: #856404;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        .explanation p {
            color: #856404;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .code-snippet {
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-family: 'Courier New', Courier, monospace;
            font-size: 13px;
            overflow-x: auto;
        }
        
        .code-snippet::-webkit-scrollbar {
            height: 6px;
        }
        
        .code-snippet::-webkit-scrollbar-track {
            background: #4a5568;
            border-radius: 3px;
        }
        
        .code-snippet::-webkit-scrollbar-thumb {
            background: #718096;
            border-radius: 3px;
        }
        
        footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            header h1 {
                font-size: 2em;
            }
            
            main {
                padding: 20px;
            }
            
            input[type="text"] {
                width: 100%;
            }
            
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            
            button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>FastAPI Streaming API 演示</h1>
            <p>探索现代 Web 应用中的实时数据流式传输技术</p>
        </header>
        
        <main>
            <div class="demo-section">
                <h2>1. 简单流式响应</h2>
                <div class="controls">
                    <button onclick="startSimpleStream()">开始简单流式响应</button>
                </div>
                <div class="stream-output" id="simpleOutput"></div>
                <div class="explanation">
                    <h3>🔍 功能说明</h3>
                    <p>服务器每秒生成一条简单消息并流式发送给客户端，共发送 10 条消息。</p>
                    <div class="code-snippet">
# 后端实现核心代码
@app.get("/stream/simple")
async def stream_simple():
    async def generate():
        for i in range(10):
            yield f"Message {i}\n"
            await asyncio.sleep(1)  # 模拟处理延迟
    return StreamingResponse(generate(), media_type="text/plain")
                    </div>
                    <p><strong>技术要点：</strong>使用异步生成器逐段生成数据，通过 StreamingResponse 实现流式传输。</p>
                </div>
            </div>
            
            <div class="demo-section">
                <h2>2. 服务器发送事件 (SSE)</h2>
                <div class="controls">
                    <button onclick="startSSE()">开始SSE流</button>
                    <button onclick="stopSSE()">停止SSE流</button>
                </div>
                <div class="stream-output" id="sseOutput"></div>
                <div class="explanation">
                    <h3>🔍 功能说明</h3>
                    <p>服务器每秒向客户端推送一个 JSON 格式的事件对象，包含消息 ID、内容和时间戳。</p>
                    <div class="code-snippet">
# 后端 SSE 实现
@app.get("/stream/sse")
async def stream_sse():
    async def event_generator():
        for i in range(10):
            event_data = {
                "id": i,
                "message": f"This is message {i}",
                "timestamp": time.time()
            }
            # SSE 格式: data: {JSON}\n\n
            yield f"data: {json.dumps(event_data)}\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
                    </div>
                    <p><strong>技术要点：</strong>遵循 SSE 协议标准，使用 EventSource API 实现客户端接收。</p>
                </div>
            </div>
            
            <div class="demo-section">
                <h2>3. 自定义输入流式响应</h2>
                <div class="controls">
                    <input type="text" id="customInput" placeholder="输入要流式传输的文本">
                    <button onclick="startCustomStream()">开始自定义流</button>
                </div>
                <div class="stream-output" id="customOutput"></div>
                <div class="explanation">
                    <h3>🔍 功能说明</h3>
                    <p>将用户输入的文本按字符逐个流式返回，每个字符间隔 0.2 秒，实现字符级别的流式传输。</p>
                    <div class="code-snippet">
# 后端自定义流实现
@app.get("/stream/custom/{message}")
async def stream_custom(message: str):
    async def generate():
        for i, char in enumerate(message):
            yield f"Character {i+1}: {char}\n"
            await asyncio.sleep(0.2)  # 字符间延迟
    return StreamingResponse(generate(), media_type="text/plain")
                    </div>
                    <p><strong>技术要点：</strong>通过路径参数接收用户输入，实现细粒度的字符级流式传输。</p>
                </div>
            </div>
        </main>
        
        <footer>
            <p>💻 使用 FastAPI + HTML5 + JavaScript 构建 | 🚀 体验实时 Web 技术</p>
        </footer>
    </div>

    <script>
        // 简单流式响应
        async function startSimpleStream() {
            const output = document.getElementById('simpleOutput');
            output.innerHTML = '';
            
            try {
                // 发起 GET 请求
                const response = await fetch('/stream/simple');
                // 获取可读流
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                while (true) {
                    // 读取流数据
                    const { done, value } = await reader.read();
                    if (done) break;
                    
                    // 解码并显示
                    const chunk = decoder.decode(value, { stream: true });
                    output.innerHTML += chunk.replace(/\\n/g, '<br>');
                    output.scrollTop = output.scrollHeight;
                }
            } catch (error) {
                output.innerHTML += `<span style="color: red;">Error: ${error.message}</span>`;
            }
        }
        
        // SSE连接管理
        let eventSource = null;
        
        function startSSE() {
            const output = document.getElementById('sseOutput');
            output.innerHTML = '';
            
            // 关闭现有连接
            if (eventSource) {
                eventSource.close();
            }
            
            // 创建新的 SSE 连接
            eventSource = new EventSource('/stream/sse');
            
            // 处理接收到的消息
            eventSource.onmessage = function(event) {
                try {
                    const data = JSON.parse(event.data);
                    const timeStr = new Date(data.timestamp * 1000).toLocaleTimeString();
                    output.innerHTML += `<strong>[${timeStr}]</strong> ID: ${data.id}, Message: ${data.message}<br>`;
                    output.scrollTop = output.scrollHeight;
                } catch (error) {
                    output.innerHTML += `<span style="color: red;">解析错误: ${error.message}</span><br>`;
                }
            };
            
            // 处理错误
            eventSource.onerror = function(error) {
                output.innerHTML += `<span style="color: red;">SSE Error</span><br>`;
                eventSource.close();
            };
            
            // 处理连接建立
            eventSource.onopen = function() {
                output.innerHTML += `<span style="color: green;">✅ SSE连接已建立</span><br>`;
            };
        }
        
        function stopSSE() {
            if (eventSource) {
                eventSource.close();
                eventSource = null;
                const output = document.getElementById('sseOutput');
                output.innerHTML += `<span style="color: orange;">🔴 SSE连接已关闭</span><br>`;
            }
        }
        
        // 自定义输入流式响应
        async function startCustomStream() {
            const input = document.getElementById('customInput');
            const message = input.value.trim();
            
            if (!message) {
                alert('请输入要流式传输的文本');
                return;
            }
            
            const output = document.getElementById('customOutput');
            output.innerHTML = '';
            
            try {
                // 发送包含自定义文本的请求
                const response = await fetch(`/stream/custom/${encodeURIComponent(message)}`);
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    
                    // 解码并显示
                    const chunk = decoder.decode(value, { stream: true });
                    output.innerHTML += chunk.replace(/\\n/g, '<br>');
                    output.scrollTop = output.scrollHeight;
                }
            } catch (error) {
                output.innerHTML += `<span style="color: red;">Error: ${error.message}</span>`;
            }
        }
    </script>
</body>
</html>
'''

# 简单的流式响应示例
@app.get("/stream/simple")
async def stream_simple():
    async def generate():
        for i in range(10):
            yield f"Message {i}\n"
            await asyncio.sleep(1)
    return StreamingResponse(generate(), media_type="text/plain")

# 服务器发送事件(SSE)示例
@app.get("/stream/sse")
async def stream_sse():
    async def event_generator():
        for i in range(10):
            # 创建SSE格式数据
            event_data = {
                "id": i,
                "message": f"This is message {i}",
                "timestamp": time.time()
            }
            yield f"data: {json.dumps(event_data)}\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# 基于用户输入的流式响应示例
@app.get("/stream/custom/{message}")
async def stream_custom(message: str):
    async def generate():
        for i, char in enumerate(message):
            yield f"Character {i+1}: {char}\n"
            await asyncio.sleep(0.2)
    return StreamingResponse(generate(), media_type="text/plain")
