# RAGAs 评估示例
# 用于评估 RAG 系统的质量
# 需要安装: pip install ragas openai

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset


def evaluate_rag_system(questions: list, answers: list, contexts: list, ground_truths: list):
    """
    评估 RAG 系统

    - questions: 用户问题列表
    - answers: RAG 系统生成的答案列表
    - contexts: 检索到的上下文列表
    - ground_truths: 标准答案列表
    """

    # 构建评估数据集
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }

    dataset = Dataset.from_dict(data)

    # 执行评估
    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,        # 答案是否基于上下文
            answer_relevancy,    # 答案与问题的相关性
            context_precision,   # 上下文的相关性
            context_recall       # 上下文的召回率
        ]
    )

    return result


def print_evaluation_results(result):
    """打印评估结果"""
    print("\n=== RAGAs 评估结果 ===")

    metrics = {
        "faithfulness": "忠诚度（答案基于上下文的程度）",
        "answer_relevancy": "答案相关性",
        "context_precision": "上下文精确度",
        "context_recall": "上下文召回率"
    }

    for metric_name, description in metrics.items():
        score = result[metric_name]
        print(f"{description}: {score:.4f}")


# 详细评估示例
def detailed_evaluation():
    """详细评估示例"""

    # 示例数据
    questions = [
        "什么是 Python?",
        "Python 和 Java 有什么区别?"
    ]

    contexts = [
        [
            "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。",
            "Python 以其简洁的语法和强大的功能著称。"
        ],
        [
            "Python 是一种面向对象的编程语言。",
            "Java 也是一种面向对象的编程语言，但需要编译。"
        ]
    ]

    answers = [
        "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。",
        "Python 和 Java 都是面向对象的语言，但 Python 是解释型的，Java 需要编译。"
    ]

    ground_truths = [
        "Python 是一种高级编程语言，简洁易学。",
        "Python 和 Java 都是面向对象的语言，但在类型系统和执行方式上有区别。"
    ]

    # 注意：需要设置 OPENAI_API_KEY
    # import os
    # os.environ["OPENAI_API_KEY"] = "your-api-key"

    # result = evaluate_rag_system(questions, answers, contexts, ground_truths)
    # print_evaluation_results(result)

    print("请设置 OPENAI_API_KEY 后运行完整评估")


# 单指标评估
def evaluate_single_metric():
    """单独评估某个指标"""

    # 可以单独评估每个指标
    from ragas.metrics import faithfulness

    # 准备数据
    question = "Python 是什么?"
    answer = "Python 是一种高级编程语言。"
    context = ["Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。"]

    # 评估 faithfulness
    # score = faithfulness.score(question, answer, context)

    print("单个指标评估示例")
    print("需要安装 ragas 并设置 OPENAI_API_KEY 后运行")


if __name__ == "__main__":
    detailed_evaluation()
