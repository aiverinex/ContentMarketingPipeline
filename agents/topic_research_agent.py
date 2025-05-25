"""
Topic Research Agent for Content Marketing Pipeline
Researches trending topics based on seed keywords using OpenAI GPT-4o
"""

import os
import json
from crewai import Agent
from langchain_openai import ChatOpenAI


class TopicResearchAgent:
    """Agent responsible for researching trending topics in a given industry"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
    
    def create_agent(self):
        """Create and return the topic research agent"""
        return Agent(
            role="Content Topic Research Specialist",
            goal="Research and identify trending topics in specified industries that will drive engagement and provide value to target audiences",
            backstory="""You are an expert content strategist with deep knowledge of market trends, 
            consumer behavior, and digital marketing. You have years of experience identifying viral 
            content opportunities and understanding what resonates with different audiences across 
            various industries. Your research is always data-driven and focuses on topics that 
            balance trending appeal with evergreen value.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )
    
    def research_topics(self, seed_keywords, industry_context=""):
        """
        Research trending topics based on seed keywords
        
        Args:
            seed_keywords (list): List of seed keywords to research
            industry_context (str): Additional context about the industry
            
        Returns:
            dict: Research results with trending topics and insights
        """
        try:
            keywords_str = ", ".join(seed_keywords)
            
            prompt = f"""
            Based on the seed keywords: {keywords_str}
            Industry context: {industry_context}
            
            Research and suggest 3-5 trending content topics that would be valuable for content marketing.
            
            For each topic, provide:
            1. Topic title
            2. Why it's trending
            3. Target audience appeal
            4. Content angle suggestions
            5. SEO potential score (1-10)
            
            Return your response in JSON format with this structure:
            {{
                "trending_topics": [
                    {{
                        "title": "Topic Title",
                        "trending_reason": "Why this topic is trending",
                        "target_audience": "Who would be interested",
                        "content_angles": ["angle1", "angle2", "angle3"],
                        "seo_score": 8,
                        "urgency_level": "high/medium/low"
                    }}
                ],
                "market_insights": "Overall market observations",
                "recommended_focus": "Which topic to prioritize and why"
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            # Parse the JSON response
            try:
                result = json.loads(response.content)
                return result
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "trending_topics": [],
                    "market_insights": response.content,
                    "recommended_focus": "Manual review needed",
                    "error": "Failed to parse structured response"
                }
                
        except Exception as e:
            return {
                "trending_topics": [],
                "market_insights": f"Error occurred during research: {str(e)}",
                "recommended_focus": "Please check API configuration",
                "error": str(e)
            }
    
    def analyze_competition(self, topic, keywords):
        """
        Analyze competition level for a given topic
        
        Args:
            topic (str): The topic to analyze
            keywords (list): Related keywords
            
        Returns:
            dict: Competition analysis results
        """
        try:
            keywords_str = ", ".join(keywords)
            
            prompt = f"""
            Analyze the competition level for this content topic: "{topic}"
            Related keywords: {keywords_str}
            
            Provide analysis on:
            1. Competition level (low/medium/high)
            2. Content gap opportunities
            3. Differentiation strategies
            4. Optimal content format recommendations
            
            Return response in JSON format:
            {{
                "competition_level": "medium",
                "content_gaps": ["gap1", "gap2"],
                "differentiation_strategies": ["strategy1", "strategy2"],
                "recommended_formats": ["blog", "video", "infographic"],
                "success_probability": 7
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                return {
                    "competition_level": "unknown",
                    "content_gaps": [],
                    "differentiation_strategies": [],
                    "recommended_formats": ["blog"],
                    "success_probability": 5,
                    "raw_analysis": response.content
                }
                
        except Exception as e:
            return {
                "competition_level": "unknown",
                "error": str(e),
                "content_gaps": [],
                "differentiation_strategies": [],
                "recommended_formats": ["blog"],
                "success_probability": 1
            }
