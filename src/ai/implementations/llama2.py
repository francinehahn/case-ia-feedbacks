import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from abstract_classes.LLM import LLM
import torch
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline

class Llama2(LLM):
    def __init__(self):
        MODEL_NAME = "TheBloke/Llama-2-13b-Chat-GPTQ"
 
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
        
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, torch_dtype=torch.float16, trust_remote_code=True, device_map="auto"
        )
        
        generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
        generation_config.max_new_tokens = 1024
        generation_config.temperature = 0.0001
        generation_config.top_p = 0.95
        generation_config.do_sample = True
        generation_config.repetition_penalty = 1.15
        
        text_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            generation_config=generation_config,
        )
        
        self.llm = HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0})
    
    def perform_request(self, prompt:list):
        try:
            successful = False
            attempts = 0
            
            while not successful and attempts < 3:
                try:
                    attempts += 1
                    result = self.llm(prompt)
                    successful = True
                except:
                    pass
                
            if not successful:
                raise Exception('LLM error: not possible to perform request.')
            
            return result
        except Exception as e:
            raise Exception(str(e)) from e