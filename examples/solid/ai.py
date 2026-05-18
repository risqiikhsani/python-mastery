from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

# =====================================================================
# 1. PYDANTIC METHOD-SPECIFIC INPUT VALIDATORS
# =====================================================================

class SummarizeInput(BaseModel):
    """Enforces rules specific to the summarize method."""
    text: str = Field(..., min_length=20, description="The content that needs shortening.")

class PoemInput(BaseModel):
    """Enforces rules specific to the write_poem method."""
    topic: str = Field(..., min_length=2, description="What the poem should be about.")
    style: str = Field(default="rhyming", description="The poetic style (e.g., rhyming, free verse,).")

class CodeReviewInput(BaseModel):
    """Enforces rules specific to the review_code method."""
    code: str = Field(..., min_length=5, description="The snippet of code to analyze.")
    language: str = Field(default="Python")


# =====================================================================
# 2. ABSTRACTION (AI Provider Contract)
# =====================================================================

class AIModel(ABC):
    """Abstract contract ensuring all engines accept both System and User instructions."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        pass


# =====================================================================
# 3. INHERITANCE (Concrete AI Engine Strategies)
# =====================================================================

class OpenAIProvider(AIModel):
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        # Real SDK usage would look like: client.chat.completions.create(...)
        print(f"🎬 [Calling OpenAI API - Model: {self.model_name}]")
        return f"(GPT-Generated Output based on system rules: '{system_prompt[:40]}...') -> Processed: '{user_prompt[:30]}...'"


class GoogleGenAIProvider(AIModel):
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        # Real SDK usage would look like: client.models.generate_content(...)
        print(f"🎬 [Calling Google GenAI API - Model: {self.model_name}]")
        return f"(Gemini-Generated Output based on system rules: '{system_prompt[:40]}...') -> Processed: '{user_prompt[:30]}...'"


# =====================================================================
# 4. THE FACADE SERVICE (UsefulService via Composition)
# =====================================================================

class UsefulService:
    """The user-facing toolbox. Hides system prompts and orchestrates execution."""
    
    def __init__(self, ai_engine: AIModel):
        # Composition: UsefulService possesses an AI Engine
        self.ai_engine = ai_engine

    def change_model(self, new_ai_engine: AIModel):
        """Allows swapping underlying AI brains instantly."""
        print(f"\n🔄 Model engine dynamically switched to: {type(new_ai_engine).__name__} ({new_ai_engine.model_name})")
        self.ai_engine = new_ai_engine

    # -----------------------------------------------------------------
    # Premade Tool 1: Summarize
    # -----------------------------------------------------------------
    def summarize(self, text: str) -> str:
        # Validate inputs via Pydantic
        validated = SummarizeInput(text=text)
        
        # Hardcoded, optimized pre-made system prompt
        system_prompt = "You are an elite research assistant. Condense the text into a 3-bullet-point TL;DR summary."
        user_prompt = f"Please summarize this text:\n{validated.text}"
        
        return self.ai_engine.generate(system_prompt, user_prompt)

    # -----------------------------------------------------------------
    # Premade Tool 2: Write Poem
    # -----------------------------------------------------------------
    def write_poem(self, topic: str, style: str = "rhyming") -> str:
        # Validate inputs via Pydantic
        validated = PoemInput(topic=topic, style=style)
        
        system_prompt = f"You are Shakespeare's modern AI reincarnation. Write a beautiful poem strictly using the {validated.style} structure."
        user_prompt = f"Write a deep, creative poem about: {validated.topic}"
        
        return self.ai_engine.generate(system_prompt, user_prompt)

    # -----------------------------------------------------------------
    # Premade Tool 3: Code Review
    # -----------------------------------------------------------------
    def review_code(self, code: str, language: str = "Python") -> str:
        # Validate inputs via Pydantic
        validated = CodeReviewInput(code=code, language=language)
        
        system_prompt = f"You are a Principal Software Engineer. Critically review this {validated.language} code for bugs, performance leaks, and SOLID violations."
        user_prompt = f"Review this code snippet:\n```\n{validated.code}\n```"
        
        return self.ai_engine.generate(system_prompt, user_prompt)


# =====================================================================
# 5. SIMULATION RUNTIME
# =====================================================================

# Create our concrete engines
gpt_4o = OpenAIProvider(model_name="gpt-4o")
gemini_flash = GoogleGenAIProvider(model_name="gemini-2.5-flash")

# Initialize the UsefulService toolbox defaulting to OpenAI
toolbox = UsefulService(ai_engine=gpt_4o)

# --- Task 1: Generate a Summary (Using OpenAI) ---
print("\n--- Running Task 1 ---")
long_article = "Artificial intelligence leverages computers and machines to mimic the problem-solving and decision-making capabilities of the human mind. Over the last decade, deep learning architectures have scaled massively."
summary_result = toolbox.summarize(text=long_article)
print(summary_result)

# --- Task 2: Write a Poem (Using OpenAI) ---
print("\n--- Running Task 2 ---")
poem_result = toolbox.write_poem(topic="Cyberpunk Coffee Shops", style="Haiku")
print(poem_result)

# =================================================================
# USER WANTS TO SWITCH THE MODEL TO GEMINI NOW
# =================================================================
toolbox.change_model(gemini_flash)

# --- Task 3: Review Code (Now flawlessly executed by Google Gemini) ---
print("\n--- Running Task 3 ---")
bad_code_sample = "def calc(x): return x * 1.10" # Very short, but passes our min_length=5 constraint
review_result = toolbox.review_code(code=bad_code_sample, language="Python")
print(review_result)

# --- Task 4: Catching Bad Inputs ---
print("\n--- Running Task 4 (Error Handling Test) ---")
try:
    # This will crash instantly via Pydantic before hitting any AI APIs
    toolbox.write_poem(topic="A")  # ❌ Fails min_length=2 constraint
except Exception as error:
    print(f"🛡️ Pydantic blocked invalid parameters successfully:\n{error}")