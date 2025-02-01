import torch
import accelerate
from torch import cuda, bfloat16
import transformers
from transformers import StoppingCriteria, StoppingCriteriaList
from langchain_community.llms import HuggingFacePipeline
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv,  find_dotenv, dotenv_values
from General.constants import LLMS

# Load confidential from .env file
load_dotenv()
# .env path
EnvPath = ".env"
Secrets = dotenv_values(EnvPath)


def extract_text_from_pdf(pdf_path):
    """
    This function is for knowledge-based QA system in which a document can be uploaded and ask a question.
    :param pdf_path: Path to the required document.
    :return:
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def load_model(llm_model_name: str):
    """
    This function loads the requested LLM Model.
    Steps:
    1. Quantization Config for small GPUs:
        1.1. Config BitsAndBytes to use large models in small GPUs
        1.2. Get the transformers Auto Config from HuggingFace
    2. Load the pre-trained LLM Model
    3. Load the same LLM Tokenizer

    :param llm_model_name: The name of the LLM on HuggingFace Repo
    :return:
    model: Returns the model to make the chat chain
    tokenizer: This will be used together with model to build chat chain
    StopCriteria: this holds the list of words in which model will consider them as the stop point.

    """
    torch.cuda.empty_cache()
    device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
    # set quantization configuration to load large model with less GPU memory
    # this requires the `bitsandbytes` library
    bnb_config = transformers.BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=bfloat16
    )
    # begin initializing HF items, you need an access token
    model_config = transformers.AutoConfig.from_pretrained(
        llm_model_name,
        token=Secrets["HuggingFaceToken"]
    )
    # Without quantization_config, you can not run the model on small GPUs. This quantization config chops the
    # model into the gpu memory size.
    # if we are using QA models directly we do not need to make a chain and thus, we can directly load the
    # model using AutoModel for QA LLMs
    model = transformers.AutoModelForCausalLM.from_pretrained(
        llm_model_name,
        trust_remote_code=True,
        config=model_config,
        quantization_config=bnb_config,
        device_map=device,
        token=Secrets["HuggingFaceToken"],
        cache_dir="./Models/Cache/"
    )

    # enable evaluation mode to allow model inference, this will also be needed for the fine_tuning
    model.eval()

    print(f"Model loaded on {device}")
    tokenizer = transformers.AutoTokenizer.from_pretrained(llm_model_name,
                                                           token=Secrets["HuggingFaceToken"],
                                                           use_fast=False,  # For larger models this is necessary
                                                           device_map="auto",  # This gives error for larger models
                                                           cache_dir="./Models/Cache/"
                                                           )
    stop_list = ['\nHuman:', '\n```\n']

    stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]
    stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]

    # define custom stopping criteria object
    class StopOnTokens(StoppingCriteria):
        def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
            for stop_ids in stop_token_ids:
                if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                    return True
            return False

    stopping_criteria = StoppingCriteriaList([StopOnTokens()])
    return model, tokenizer, stopping_criteria


def build_the_chain(model, tokenizer, pdf_text, stopping_criteria, temperature=0.1):
    """
    This function receives the model, tokenizer, the target document (for knowledge-based QA), stopping_criteria
    and the temperature (to control the auto_generation/randomness) level of the model in the chain.
    :param model:
    :param tokenizer:
    :param pdf_text:
    :param stopping_criteria:
    :param temperature:
    :return:
    chain: this will be used to establish th communication with the client.
    """

    # Establish the text_generation pipline.
    text_generator_pipline = transformers.pipeline(
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,  # langchain expects the full text
        task='text-generation',
        # we pass model parameters here too
        stopping_criteria=stopping_criteria,  # without this model rambles during chat
        temperature=temperature,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
        max_new_tokens=512,  # max number of tokens to generate in the output
        repetition_penalty=1.1  # without this output begins repeating
    )
    # prompt = "What is agent-based modeling."
    # res = generate_text(prompt)
    # print(res[0]["generated_text"])
    llm = HuggingFacePipeline(pipeline=text_generator_pipline)

    # Creating Embeddings and Storing in Vector Store
    # This can be considered as one of the indirect parameters in the all over the chain.
    # using a large model as the embedding layer like LLAMA will make the chain super heavy,
    # based on experiments, "sentence-transformers/all-mpnet-base-v2" acts fine for small tasks.
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {"device": "cuda"}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

    # storing embeddings in the vector store
    # This is used to chop the input target text for limited resources.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    # If loaded using document loader

    # vectorstore = FAISS.from_documents(all_splits, embeddings)
    # Initializing Chain
    if pdf_text != "":
        # all_splits = text_splitter.split_documents(documents)
        all_splits = text_splitter.split_text(pdf_text)
    else:
        # all_splits = text_splitter.split_documents(documents)
        all_splits = [""]

    vectorstore = FAISS.from_texts(all_splits,
                                   embeddings)

    messages = [
        SystemMessagePromptTemplate.from_template("{context} You are a chatbot answering the questions"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
    # Comments
    prompt_template = ChatPromptTemplate.from_messages(messages=messages)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Memory object makes it super heavy in terms of storage.
    chain = ConversationalRetrievalChain.from_llm(llm,
                                                  vectorstore.as_retriever(),
                                                  # memory=memory,
                                                  return_source_documents=False)
    print("new thing")
    return chain, memory


def QA(chain, prompt, chat_history: list):
    """
    This function does the chat using the langchain and the received prompt.
    """
    # Chat with our own chat_history list
    result = chain({"question": prompt, "chat_history": []})
    print(result)
    # If we are using memory in the chain, then we do not need to have chat_history. Otherwise, memory makes it so heavy.
    # result = chain({"question": prompt})
    # print(result["answer"].__dict__)
    chat_history.append([prompt, result["answer"]])
    return result['answer'], chain, chat_history

