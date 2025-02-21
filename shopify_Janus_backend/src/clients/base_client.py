"""Base client for API interactions"""
from abc import ABC, abstractmethod
import logging
from typing import Optional, Union

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BaseClient(ABC):
    """Abstract base client"""
    
    @abstractmethod
    def initialize(self):
        """Initialize client connection"""
        pass
    
    @abstractmethod
    def validate_response(self, result: Optional[Union[list, str]]) -> bool:
        """Validate API response"""
        pass 