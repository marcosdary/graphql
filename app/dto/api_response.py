from pydantic import BaseModel

class ApiResponseModel(BaseModel):
    success: bool
    data: None = None
    error: None = None
    
