"""Day 30: 企业知识库问答系统（命令行版 RAG）"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

SAMPLE_DOCS = [
    "公司年假政策：入职满一年享受5天年假，满三年享受10天年假。",
    "报销流程：填写报销单→部门经理审批→财务部审核→3个工作日内到账。",
    "远程办公规定：每周最多远程2天，需提前在OA系统申请。",
    "考勤制度：上班时间9:00，迟到15分钟以内扣半天年假。",
]


def build_rag_chain():
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.create_documents(SAMPLE_DOCS)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE"),
    )
    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE"),
    )

    template = """基于以下上下文回答问题。如果无法从上下文找到答案，请说"我不知道"。

上下文:
{context}

问题: {question}

回答（请标注引用来源）:"""

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n".join(f"- {d.page_content}" for d in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def main():
    print("📚 企业知识库问答系统")
    chain = build_rag_chain()
    while True:
        q = input("\n请输入问题 (quit退出): ").strip()
        if q.lower() == "quit":
            break
        answer = chain.invoke(q)
        print(f"\n回答: {answer}")


if __name__ == "__main__":
    main()
