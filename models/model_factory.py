"""
Model Factory

This module manages all available AI models and provides a unified interface.
"""

import os
from typing import Dict, Optional, Type
from termcolor import cprint
from dotenv import load_dotenv
from pathlib import Path
from .base_model import BaseModel
import random

# Import models only if their dependencies are available
# This allows the factory to work even if some model packages aren't installed

try:
    from .deepseek_model import DeepSeekModel
    DEEPSEEK_AVAILABLE = True
except ImportError:
    DEEPSEEK_AVAILABLE = False
    DeepSeekModel = None

try:
    from .claude_model import ClaudeModel
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    ClaudeModel = None

try:
    from .openai_model import OpenAIModel
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAIModel = None

try:
    from .groq_model import GroqModel
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    GroqModel = None

try:
    from .gemini_model import GeminiModel
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    GeminiModel = None

try:
    from .ollama_model import OllamaModel
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    OllamaModel = None

try:
    from .xai_model import XAIModel
    XAI_AVAILABLE = True
except ImportError:
    XAI_AVAILABLE = False
    XAIModel = None

class ModelFactory:
    """Factory for creating and managing AI models"""
    
    # Map model types to their implementations (only if available)
    MODEL_IMPLEMENTATIONS = {}
    
    if DEEPSEEK_AVAILABLE and DeepSeekModel:
        MODEL_IMPLEMENTATIONS["deepseek"] = DeepSeekModel
    if CLAUDE_AVAILABLE and ClaudeModel:
        MODEL_IMPLEMENTATIONS["claude"] = ClaudeModel
    if OPENAI_AVAILABLE and OpenAIModel:
        MODEL_IMPLEMENTATIONS["openai"] = OpenAIModel
    if GROQ_AVAILABLE and GroqModel:
        MODEL_IMPLEMENTATIONS["groq"] = GroqModel
    if GEMINI_AVAILABLE and GeminiModel:
        MODEL_IMPLEMENTATIONS["gemini"] = GeminiModel
    if OLLAMA_AVAILABLE and OllamaModel:
        MODEL_IMPLEMENTATIONS["ollama"] = OllamaModel
    if XAI_AVAILABLE and XAIModel:
        MODEL_IMPLEMENTATIONS["xai"] = XAIModel
    
    # Default models for each type
    DEFAULT_MODELS = {
        "claude": "claude-3-5-haiku-latest",  # Latest fast Claude model
        "groq": "mixtral-8x7b-32768",        # Fast Mixtral model
        "openai": "gpt-4o",                  # Latest GPT-4 Optimized
        "gemini": "gemini-2.5-flash",        # Fast Gemini 2.5 model
        "deepseek": "deepseek-reasoner",     # Enhanced reasoning model
        "ollama": "llama3.2",                # Meta's Llama 3.2 - balanced performance
        "xai": "grok-4-fast-reasoning"       # xAI's Grok 4 Fast with reasoning (best value: 2M context, cheap!)
    }
    
    def __init__(self):
        # Load environment variables
        project_root = Path(__file__).parent.parent.parent
        env_path = project_root / '.env'
        load_dotenv(dotenv_path=env_path)
        
        self._models: Dict[str, BaseModel] = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all available models"""
        initialized = False
        
        # Try to initialize each model type
        for model_type, key_name in self._get_api_key_mapping().items():
            if api_key := os.getenv(key_name):
                try:
                    if model_type not in self.MODEL_IMPLEMENTATIONS:
                        continue
                    
                    model_class = self.MODEL_IMPLEMENTATIONS[model_type]
                    model_instance = model_class(api_key)
                    
                    if model_instance.is_available():
                        self._models[model_type] = model_instance
                        initialized = True
                except Exception:
                    pass  # Silently skip failed models
        
        if not initialized:
            raise RuntimeError("No AI models available - check your API keys in .env file")
    
    def get_model(self, model_type: str, model_name: Optional[str] = None) -> Optional[BaseModel]:
        """Get a specific model instance"""
        if model_type not in self.MODEL_IMPLEMENTATIONS:
            return None
            
        if model_type not in self._models:
            return None
            
        model = self._models[model_type]
        if model_name and model.model_name != model_name:
            try:
                if model_type == "ollama":
                    model = self.MODEL_IMPLEMENTATIONS[model_type](model_name=model_name)
                else:
                    if api_key := os.getenv(self._get_api_key_mapping()[model_type]):
                        model = self.MODEL_IMPLEMENTATIONS[model_type](api_key, model_name=model_name)
                    else:
                        return None
                
                self._models[model_type] = model
            except Exception:
                return None
            
        return model
    
    def _get_api_key_mapping(self) -> Dict[str, str]:
        """Get mapping of model types to their API key environment variable names"""
        return {
            "claude": "ANTHROPIC_KEY",
            "groq": "GROQ_API_KEY",
            "openai": "OPENAI_KEY",
            "gemini": "GEMINI_KEY",  # Re-enabled with Gemini 2.5 models
            "deepseek": "DEEPSEEK_KEY",
            "xai": "GROK_API_KEY",  # Grok/xAI uses GROK_API_KEY
            # Ollama doesn't need an API key as it runs locally
        }
    
    @property
    def available_models(self) -> Dict[str, list]:
        """Get all available models and their configurations"""
        return {
            model_type: model.AVAILABLE_MODELS
            for model_type, model in self._models.items()
        }
    
    def is_model_available(self, model_type: str) -> bool:
        """Check if a specific model type is available"""
        return model_type in self._models and self._models[model_type].is_available()

    def generate_response(self, system_prompt, user_content, temperature=0.7, max_tokens=None):
        """Generate a response from the model with no caching"""
        try:
            # Add random nonce to prevent caching
            nonce = f"_{random.randint(1, 1000000)}"
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{user_content}{nonce}"}  # Add nonce to force new response
                ],
                temperature=temperature,
                max_tokens=max_tokens if max_tokens else self.max_tokens
            )
            
            return response.choices[0].message
            
        except Exception as e:
            if "503" in str(e):
                raise e  # Let the retry logic handle 503s
            cprint(f"❌ Model error: {str(e)}", "red")
            return None

# Create a singleton instance
model_factory = ModelFactory() 