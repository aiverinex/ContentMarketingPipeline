"""
Blog Writer Agent for Content Marketing Pipeline
Creates high-quality blog articles using OpenAI GPT-4o
"""

import os
import json
from crewai import Agent
from langchain_openai import ChatOpenAI


class BlogWriterAgent:
    """Agent responsible for writing engaging blog articles"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.8
        )
    
    def create_agent(self):
        """Create and return the blog writer agent"""
        return Agent(
            role="Expert Content Writer",
            goal="Create compelling, well-researched blog articles that engage readers, provide value, and drive business objectives",
            backstory="""You are a seasoned content writer with expertise in creating engaging, 
            SEO-optimized blog content across various industries. You have a talent for transforming 
            complex topics into accessible, engaging narratives that resonate with target audiences. 
            Your writing style adapts to different brand voices while maintaining clarity, authority, 
            and reader engagement. You understand the importance of structure, flow, and call-to-actions 
            in driving reader engagement and conversions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )
    
    def write_blog_article(self, topic_data, target_word_count=500, brand_voice="professional"):
        """
        Write a complete blog article based on topic research
        
        Args:
            topic_data (dict): Topic information from research agent
            target_word_count (int): Target word count (300-600)
            brand_voice (str): Brand voice style
            
        Returns:
            dict: Complete blog article with metadata
        """
        try:
            # Ensure word count is within specified range
            word_count = max(300, min(600, target_word_count))
            
            topic_title = topic_data.get('title', 'Trending Industry Topic')
            content_angles = topic_data.get('content_angles', [])
            target_audience = topic_data.get('target_audience', 'business professionals')
            
            angles_str = ", ".join(content_angles) if content_angles else "industry insights, practical tips"
            
            prompt = f"""
            Write a compelling blog article with the following specifications:
            
            Topic: {topic_title}
            Target word count: {word_count} words
            Target audience: {target_audience}
            Brand voice: {brand_voice}
            Content angles to include: {angles_str}
            
            Structure the article with:
            1. Engaging headline
            2. Hook opening paragraph
            3. 3-4 main sections with subheadings
            4. Practical insights and actionable tips
            5. Strong conclusion with call-to-action
            
            Make the content:
            - Informative and valuable
            - Engaging and well-structured
            - SEO-friendly with natural keyword integration
            - Actionable with clear takeaways
            
            Return the response in JSON format:
            {{
                "headline": "Compelling Blog Headline",
                "meta_description": "SEO meta description (150-160 chars)",
                "article_content": "Full article content in markdown format",
                "word_count": {word_count},
                "key_takeaways": ["takeaway1", "takeaway2", "takeaway3"],
                "suggested_tags": ["tag1", "tag2", "tag3"],
                "reading_time": "5 min read",
                "call_to_action": "Specific CTA text"
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            try:
                content = response.content
                # Try to extract JSON from the response if it's wrapped in text
                if "```json" in content:
                    start = content.find("```json") + 7
                    end = content.find("```", start)
                    content = content[start:end].strip()
                elif "```" in content:
                    start = content.find("```") + 3
                    end = content.find("```", start)
                    content = content[start:end].strip()
                
                result = json.loads(content)
                
                # Validate and enhance the response
                if not result.get('headline'):
                    result['headline'] = topic_title
                if not result.get('article_content'):
                    result['article_content'] = "Content generation failed. Please try again."
                
                # Calculate estimated reading time if not provided
                if not result.get('reading_time'):
                    estimated_words = result.get('word_count', word_count)
                    reading_minutes = max(1, estimated_words // 200)
                    result['reading_time'] = f"{reading_minutes} min read"
                
                return result
                
            except json.JSONDecodeError:
                # Fallback response if JSON parsing fails
                return {
                    "headline": topic_title,
                    "meta_description": f"Learn about {topic_title} and its impact on {target_audience}",
                    "article_content": response.content,
                    "word_count": word_count,
                    "key_takeaways": ["Manual extraction needed"],
                    "suggested_tags": ["content", "marketing", "business"],
                    "reading_time": "5 min read",
                    "call_to_action": "Learn more about our services",
                    "parsing_note": "Raw content provided due to JSON parsing issue"
                }
                
        except Exception as e:
            return {
                "headline": "Content Generation Error",
                "meta_description": "An error occurred during content generation",
                "article_content": f"Error generating blog content: {str(e)}",
                "word_count": 0,
                "key_takeaways": ["Check API configuration and try again"],
                "suggested_tags": ["error"],
                "reading_time": "0 min read",
                "call_to_action": "Please contact support",
                "error": str(e)
            }
    
    def optimize_for_seo(self, article_data, primary_keyword, secondary_keywords=None):
        """
        Optimize blog article for SEO
        
        Args:
            article_data (dict): Article content and metadata
            primary_keyword (str): Primary SEO keyword
            secondary_keywords (list): List of secondary keywords
            
        Returns:
            dict: SEO-optimized article data
        """
        try:
            secondary_kw = secondary_keywords or []
            secondary_str = ", ".join(secondary_kw) if secondary_kw else ""
            
            prompt = f"""
            Optimize this blog article for SEO:
            
            Current headline: {article_data.get('headline', '')}
            Current meta description: {article_data.get('meta_description', '')}
            Primary keyword: {primary_keyword}
            Secondary keywords: {secondary_str}
            
            Provide SEO optimizations:
            1. Improved headline with primary keyword
            2. Optimized meta description (150-160 characters)
            3. Suggested internal linking opportunities
            4. Keyword density recommendations
            5. Featured snippet optimization suggestions
            
            Return response in JSON format:
            {{
                "optimized_headline": "SEO-optimized headline",
                "optimized_meta_description": "Optimized meta description",
                "keyword_density_target": "1-2%",
                "internal_link_suggestions": ["suggestion1", "suggestion2"],
                "featured_snippet_tips": ["tip1", "tip2"],
                "seo_score": 8
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            try:
                seo_data = json.loads(response.content)
                
                # Apply optimizations to original article data
                optimized_article = article_data.copy()
                optimized_article['headline'] = seo_data.get('optimized_headline', article_data.get('headline'))
                optimized_article['meta_description'] = seo_data.get('optimized_meta_description', article_data.get('meta_description'))
                optimized_article['seo_optimizations'] = seo_data
                
                return optimized_article
                
            except json.JSONDecodeError:
                # Return original data with SEO notes if parsing fails
                article_data['seo_optimizations'] = {
                    "note": "SEO optimization failed - manual review needed",
                    "raw_suggestions": response.content
                }
                return article_data
                
        except Exception as e:
            article_data['seo_optimizations'] = {
                "error": str(e),
                "note": "SEO optimization encountered an error"
            }
            return article_data
