"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Existing example schemas (kept for reference / potential reuse)
class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Batman-themed collections
class Batmobile(BaseModel):
    """
    Batmobile collection schema
    Collection name: "batmobile"
    """
    name: str = Field(..., description="Designation or common name")
    year: Optional[int] = Field(None, description="First appearance year")
    media: str = Field(..., description="Where it appears (film, animation, game, comic)")
    title: Optional[str] = Field(None, description="Title of the work, e.g., The Dark Knight")
    driver: Optional[str] = Field(None, description="Primary driver, typically Bruce Wayne/Batman")
    era: Optional[str] = Field(None, description="Era or continuity, e.g., Burtonverse, DCEU")
    universe: Optional[str] = Field(None, description="Film / Animated / Game / TV / Comic")
    description: Optional[str] = Field(None, description="Short description of design and capabilities")
    specs: Optional[List[str]] = Field(default=None, description="Key features/specifications")
    designer: Optional[str] = Field(None, description="Designer or production designer")
    image_url: Optional[HttpUrl] = Field(None, description="Preview image URL")
    source: Optional[str] = Field(None, description="Source or notes")

class Gadget(BaseModel):
    """
    Gadgets collection schema
    Collection name: "gadget"
    """
    name: str = Field(..., description="Gadget name")
    category: str = Field(..., description="Category, e.g., Offensive, Mobility, Utility, Forensics")
    description: str = Field(..., description="What it does")
    first_appearance: Optional[str] = Field(None, description="First notable appearance")
    image_url: Optional[HttpUrl] = Field(None, description="Preview image URL")
