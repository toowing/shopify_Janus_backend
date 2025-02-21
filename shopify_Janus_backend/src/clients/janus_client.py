"""Janus API client implementation"""
from gradio_client import Client
import time
from typing import Dict, Union, Optional
from .base_client import BaseClient, logger
from ..config import Config

class JanusClient(BaseClient):
    """Client for interacting with Janus API"""
    
    def __init__(self):
        self.initialize()
    
    def initialize(self):
        """Initialize Gradio client"""
        try:
            logger.debug("Initializing Gradio client...")
            self.client = Client(Config.JANUS_MODEL_ID)
            logger.debug("Gradio client initialized successfully")
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise
    
    def generate_image(self, prompt: str) -> Dict[str, Union[bool, str]]:
        """
        Generate image with retry mechanism for GPU quota issues
        
        Args:
            prompt: Text description for image generation
            
        Returns:
            Dictionary containing generation results
            
        Raises:
            ValueError: For invalid prompts
            Exception: For generation failures
        """
        self._validate_prompt(prompt)
        
        for attempt in range(Config.MAX_RETRIES):
            try:
                return self._attempt_generation(prompt, attempt)
            except Exception as e:
                if not self._handle_error(e, attempt):
                    raise
        
        raise Exception("Maximum retry attempts reached")
    
    def _validate_prompt(self, prompt: str) -> None:
        """Validate input prompt"""
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Invalid prompt: Must be a non-empty string")
    
    def _attempt_generation(self, prompt: str, attempt: int) -> Dict[str, Union[bool, str]]:
        """Attempt to generate image"""
        logger.debug(f"Attempt {attempt + 1}: Starting image generation, prompt: {prompt}")
        
        result = self.client.predict(
            prompt,
            seed=1234,
            guidance=5,
            t2i_temperature=1,
            api_name="/generate_image"
        )
        
        if not self.validate_response(result):
            raise Exception("Empty response from API")
        
        return {
            "success": True,
            "image_url": result[0] if isinstance(result, list) else result,
            "generated_text": prompt
        }
    
    def _handle_error(self, error: Exception, attempt: int) -> bool:
        """
        Handle generation errors
        
        Returns:
            bool: True if error was handled and retry should continue
        """
        error_msg = str(error)
        logger.error(f"Attempt {attempt + 1} failed: {error_msg}")
        
        if "GPU quota" in error_msg:
            if attempt < Config.MAX_RETRIES - 1:
                wait_time = Config.RETRY_DELAY * (attempt + 1)
                logger.info(f"GPU quota exceeded. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                return True
            else:
                raise Exception(
                    "GPU quota exceeded. Please try again later or upgrade your account at "
                    "https://huggingface.co/join"
                )
        return False
    
    def validate_response(self, result: Optional[Union[list, str]]) -> bool:
        """Validate API response"""
        return bool(result) and not (isinstance(result, list) and not result) 