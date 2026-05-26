"""
Structured Output Agent for Data Validation

Demonstrates when to use structured outputs with PydanticAI:
- Environment-based model configuration (following main_agent_reference)
- Structured output validation with Pydantic models (result_type specified)
- Data extraction and validation use case
- Professional report generation with consistent formatting
"""

import logging
from dataclasses import dataclass
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Configuration settings for the structured output agent."""
    
    # LLM Configuration
    llm_provider: str = Field(default="openai")
    llm_api_key: str = Field(...)
    llm_model: str = Field(default="gpt-4")
    llm_base_url: str = Field(default="https://api.openai.com/v1")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_llm_model() -> OpenAIModel:
    """Get configured LLM model from environment settings."""
    try:
        settings = Settings()
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )
        return OpenAIModel(settings.llm_model, provider=provider)
    except Exception:
        # For testing without env vars
        import os
        os.environ.setdefault("LLM_API_KEY", "test-key")
        settings = Settings()
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key="test-key"
        )
        return OpenAIModel(settings.llm_model, provider=provider)


@dataclass
class AnalysisDependencies:
    """Dependencies for the analysis agent."""
    report_format: str = "business"  # business, technical, academic
    include_recommendations: bool = True
    session_id: Optional[str] = None


class DataInsight(BaseModel):
    """Individual insight extracted from data."""
    insight: str = Field(description="The key insight or finding")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence level in this insight")
    data_points: List[str] = Field(description="Supporting data points")


class DataAnalysisReport(BaseModel):
    """Structured output for data analysis with validation."""
    
    # Required fields
    summary: str = Field(description="Executive summary of the analysis")
    key_insights: List[DataInsight] = Field(
        min_items=1, 
        max_items=10,
        description="Key insights discovered in the data"
    )
    
    # Validated fields
    confidence_score: float = Field(
        ge=0.0, le=1.0,
        description="Overall confidence in the analysis"
    )
    data_quality: str = Field(
        pattern="^(excellent|good|fair|poor)$",
        description="Assessment of data quality"
    )
    
    # Optional structured fields
    recommendations: Optional[List[str]] = Field(
        default=None,
        description="Actionable recommendations based on findings"
    )
    limitations: Optional[List[str]] = Field(
        default=None,
        description="Limitations or caveats in the analysis"
    )
    
    # Metadata
    analysis_type: str = Field(description="Type of analysis performed")
    data_sources: List[str] = Field(description="Sources of data analyzed")


SYSTEM_PROMPT = """
You are an expert data analyst specializing in extracting structured insights from various data sources.

Your role:
- Analyze provided data with statistical rigor
- Extract meaningful insights and patterns
- Assess data quality and reliability
- Provide actionable recommendations
- Structure findings in a consistent, professional format

Guidelines:
- Be objective and evidence-based in your analysis
- Clearly distinguish between facts and interpretations
- Provide confidence levels for your insights
- Highlight both strengths and limitations of the data
- Ensure all outputs follow the required structured format
"""


# Create structured output agent - NOTE: result_type specified for data validation
structured_agent = Agent(
    get_llm_model(),
    deps_type=AnalysisDependencies,
    result_type=DataAnalysisReport,  # This is when we DO want structured output
    system_prompt=SYSTEM_PROMPT
)


@structured_agent.tool
def analyze_numerical_data(
    ctx: RunContext[AnalysisDependencies],
    data_description: str,
    numbers: List[float]
) -> str:
    """
    Analyze numerical data and provide statistical insights.
    
    Args:
        data_description: Description of what the numbers represent
        numbers: List of numerical values to analyze
    
    Returns:
        Statistical analysis summary
    """
    try:
        if not numbers:
            return "No numerical data provided for analysis."
        
        # Basic statistical calculations
        count = len(numbers)
        total = sum(numbers)
        average = total / count
        minimum = min(numbers)
        maximum = max(numbers)
        
        # Calculate variance and standard deviation
        variance = sum((x - average) ** 2 for x in numbers) / count
        std_dev = variance ** 0.5
        
        # Simple trend analysis
        if count > 1:
            trend = "increasing" if numbers[-1] > numbers[0] else "decreasing"
        else:
            trend = "insufficient data"
        
        analysis = f"""
Statistical Analysis of {data_description}:
- Count: {count} data points
- Average: {average:.2f}
- Range: {minimum:.2f} to {maximum:.2f}  
- Standard Deviation: {std_dev:.2f}
- Overall Trend: {trend}
- Data Quality: {'good' if std_dev < average * 0.5 else 'variable'}
"""
        
        logger.info(f"Analyzed {count} data points for: {data_description}")
        return analysis.strip()
        
    except Exception as e:
        logger.error(f"Error in numerical analysis: {e}")
        return f"Error analyzing numerical data: {str(e)}"


async def analyze_data(
    data_input: str,
    dependencies: Optional[AnalysisDependencies] = None
) -> DataAnalysisReport:
    """
    Analyze data and return structured report.
    
    Args:
        data_input: Raw data or description to analyze
        dependencies: Optional analysis configuration
    
    Returns:
        Structured DataAnalysisReport with validation
    """
    if dependencies is None:
        dependencies = AnalysisDependencies()
    
    result = await structured_agent.run(data_input, deps=dependencies)
    return result.data


def analyze_data_sync(
    data_input: str,
    dependencies: Optional[AnalysisDependencies] = None
) -> DataAnalysisReport:
    """
    Synchronous version of analyze_data.
    
    Args:
        data_input: Raw data or description to analyze
        dependencies: Optional analysis configuration
    
    Returns:
        Structured DataAnalysisReport with validation
    """
    import asyncio
    return asyncio.run(analyze_data(data_input, dependencies))


# Example usage and demonstration
if __name__ == "__main__":
    import asyncio
    
    async def demo_structured_output():
        """Demonstrate structured output validation."""
        print("=== Structured Output Agent Demo ===\n")
        
        # Sample data scenarios
        scenarios = [
            {
                "title": "Sales Performance Data",
                "data": """
                Monthly sales data for Q4 2024:
                October: $125,000
                November: $142,000  
                December: $158,000
                
                Customer satisfaction scores: 4.2, 4.5, 4.1, 4.6, 4.3
                Return rate: 3.2%
                """
            },
            {
                "title": "Website Analytics",
                "data": """
                Website traffic analysis:
                - Daily visitors: 5,200 average
                - Bounce rate: 35%
                - Page load time: 2.1 seconds
                - Conversion rate: 3.8%
                - Mobile traffic: 68%
                """
            }
        ]
        
        for scenario in scenarios:
            print(f"Analysis: {scenario['title']}")
            print(f"Input Data: {scenario['data'][:100]}...")
            
            # Configure for business report
            deps = AnalysisDependencies(
                report_format="business",
                include_recommendations=True
            )
            
            try:
                report = await analyze_data(scenario['data'], deps)
                
                print(f"Summary: {report.summary}")
                print(f"Confidence: {report.confidence_score}")
                print(f"Data Quality: {report.data_quality}")
                print(f"Key Insights: {len(report.key_insights)} found")
                
                for i, insight in enumerate(report.key_insights, 1):
                    print(f"  {i}. {insight.insight} (confidence: {insight.confidence})")
                
                if report.recommendations:
                    print(f"Recommendations: {len(report.recommendations)}")
                    for i, rec in enumerate(report.recommendations, 1):
                        print(f"  {i}. {rec}")
                
                print("=" * 60)
                
            except Exception as e:
                print(f"Analysis failed: {e}")
                print("=" * 60)
    
    # Run the demo
    asyncio.run(demo_structured_output())