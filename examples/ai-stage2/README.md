# AI 开发基础 - 代码示例

本文件夹包含 AI 阶段2（LLM API 调用）的代码示例。

## 目录结构

```
ai-stage2/
├── 01-openai/              # OpenAI API
│   └── openai_basic.py
├── 02-anthropic/          # Claude API
│   └── claude_basic.py
├── 03-domestic-models/    # 国内模型
│   └── domestic_models.py
├── 04-prompt-design/      # Prompt 设计
│   └── prompt_design.py
├── 05-parameters/         # 参数演示
│   └── parameters_demo.py
├── 06-projects/           # 实战项目
│   ├── chat_assistant.py
│   └── model_comparison.py
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install openai anthropic pydantic
```

### 2. 配置 API Key

```bash
# OpenAI
export OPENAI_API_KEY="your-key"

# Anthropic
export ANTHROPIC_API_KEY="your-key"

# 国内模型各自申请 API Key
```

### 3. 运行示例

```bash
# OpenAI 基础示例
python 01-openai/openai_basic.py

# Claude 基础示例
python 02-anthropic/claude_basic.py

# 国内模型示例
python 03-domestic-models/domestic_models.py

# Prompt 设计
python 04-prompt-design/prompt_design.py

# 参数演示
python 05-parameters/parameters_demo.py

# 对话助手
python 06-projects/chat_assistant.py
```

## 环境要求

- Python 3.8+
- API Key（各平台申请）

## 注意事项

1. 大部分示例需要实际的 API Key 才能运行
2. API 调用会产生费用，请注意使用量
3. 国内模型需要各自平台的账号和 API Key
