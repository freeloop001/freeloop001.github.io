# 多模态 API 示例（Vision）
# 需要安装: pip install openai

from openai import OpenAI
import base64

client = OpenAI()


def encode_image(image_path: str) -> str:
    """将图片编码为 base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_image_from_url(image_url: str, prompt: str = "描述这张图片") -> str:
    """通过 URL 分析图片"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ],
        max_tokens=300
    )

    return response.choices[0].message.content


def analyze_image_from_file(image_path: str, prompt: str = "描述这张图片") -> str:
    """通过本地文件分析图片"""
    # 将图片转为 base64
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    return response.choices[0].message.content


def extract_text_from_image(image_path: str) -> str:
    """从图片中提取文字（OCR）"""
    prompt = "请提取图片中的所有文字内容，保持原有格式。"
    return analyze_image_from_file(image_path, prompt)


def describe_chart(image_path: str) -> str:
    """描述图表内容"""
    prompt = """请详细描述这张图表，包括：
    1. 图表类型（柱状图、折线图、饼图等）
    2. 各数据项的数值
    3. 整体趋势或结论
    """
    return analyze_image_from_file(image_path, prompt)


# 示例使用
if __name__ == "__main__":
    # 示例1：通过 URL 分析图片
    print("=== 通过 URL 分析图片 ===")
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png"

    try:
        result = analyze_image_from_url(
            image_url,
            "这张图片是什么？用一句话描述。"
        )
        print(f"分析结果: {result}")
    except Exception as e:
        print(f"错误: {e}")

    # 示例2：本地文件分析（需要替换为实际图片路径）
    # print("\n=== 本地文件分析 ===")
    # result = analyze_image_from_file("path/to/image.jpg")
    # print(f"分析结果: {result}")

    # 示例3：OCR 文字提取
    # print("\n=== 文字提取 ===")
    # result = extract_text_from_file("path/to/screenshot.png")
    # print(f"提取的文字: {result}")
