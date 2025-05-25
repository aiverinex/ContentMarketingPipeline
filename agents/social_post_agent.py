"""
Social Post Agent for Content Marketing Pipeline
Generates LinkedIn and Twitter/X posts from blog content
"""

import os
import json
from crewai import Agent
from langchain_openai import ChatOpenAI


class SocialPostAgent:
    """Agent responsible for creating social media posts from blog content"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.9
        )
    
    def create_agent(self):
        """Create and return the social post agent"""
        return Agent(
            role="Social Media Content Specialist",
            goal="Transform blog content into engaging, platform-optimized social media posts that drive engagement and traffic",
            backstory="""You are a social media expert with deep understanding of different platform 
            algorithms, audience behaviors, and content formats that drive engagement. You know how to 
            adapt content for LinkedIn's professional audience and Twitter/X's fast-paced, conversational 
            environment. Your posts consistently achieve high engagement rates through strategic use of 
            hashtags, compelling hooks, and platform-specific best practices. You understand the nuances 
            of professional networking on LinkedIn and viral content mechanics on Twitter/X.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )
    
    def generate_linkedin_posts(self, blog_data, num_posts=3, post_style="professional"):
        """
        Generate LinkedIn posts from blog content
        
        Args:
            blog_data (dict): Blog article data
            num_posts (int): Number of LinkedIn posts to generate
            post_style (str): Style of posts (professional, thought-leadership, educational)
            
        Returns:
            dict: Generated LinkedIn posts with metadata
        """
        try:
            headline = blog_data.get('headline', 'Industry Insights')
            key_takeaways = blog_data.get('key_takeaways', [])
            article_content = blog_data.get('article_content', '')
            
            # Extract first paragraph for context
            content_preview = article_content[:300] + "..." if len(article_content) > 300 else article_content
            takeaways_str = "\n".join([f"• {takeaway}" for takeaway in key_takeaways[:3]])
            
            prompt = f"""
            Create {num_posts} engaging LinkedIn posts based on this blog article:
            
            Blog headline: {headline}
            Content preview: {content_preview}
            Key takeaways: {takeaways_str}
            Post style: {post_style}
            
            For each LinkedIn post, create:
            1. Hook opening (1-2 lines that grab attention)
            2. Value-driven body content (3-5 lines)
            3. Call-to-action or engagement question
            4. Relevant hashtags (5-10)
            5. Post type classification (educational, thought-leadership, promotional)
            
            LinkedIn best practices:
            - Keep under 1300 characters for optimal engagement
            - Use line breaks for readability
            - Include emojis strategically
            - End with engagement-driving questions
            - Use professional but conversational tone
            
            Return response in JSON format:
            {{
                "linkedin_posts": [
                    {{
                        "post_content": "Full LinkedIn post text with line breaks",
                        "character_count": 850,
                        "hashtags": ["#hashtag1", "#hashtag2"],
                        "post_type": "educational",
                        "engagement_prediction": "high",
                        "call_to_action": "What's your experience with this?",
                        "posting_tip": "Best time to post this type of content"
                    }}
                ],
                "content_themes": ["theme1", "theme2"],
                "overall_strategy": "Strategic notes for the post series"
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            try:
                result = json.loads(response.content)
                
                # Validate and enhance response
                if not result.get('linkedin_posts'):
                    result['linkedin_posts'] = [{
                        "post_content": f"🚀 Just published: {headline}\n\n{takeaways_str}\n\nWhat are your thoughts?",
                        "character_count": 200,
                        "hashtags": ["#contentmarketing", "#business"],
                        "post_type": "promotional",
                        "engagement_prediction": "medium",
                        "call_to_action": "Share your thoughts below",
                        "posting_tip": "Post during business hours for better reach"
                    }]
                
                return result
                
            except json.JSONDecodeError:
                # Fallback response
                return {
                    "linkedin_posts": [{
                        "post_content": response.content[:1000],
                        "character_count": len(response.content[:1000]),
                        "hashtags": ["#contentmarketing", "#business", "#insights"],
                        "post_type": "general",
                        "engagement_prediction": "medium",
                        "call_to_action": "What do you think?",
                        "posting_tip": "Review and edit before posting"
                    }],
                    "content_themes": ["business insights"],
                    "overall_strategy": "Manual review recommended due to parsing issue",
                    "parsing_note": "Raw content provided"
                }
                
        except Exception as e:
            return {
                "linkedin_posts": [{
                    "post_content": f"Error generating LinkedIn content: {str(e)}",
                    "character_count": 0,
                    "hashtags": ["#error"],
                    "post_type": "error",
                    "engagement_prediction": "none",
                    "call_to_action": "Please try again",
                    "posting_tip": "Check API configuration"
                }],
                "content_themes": ["error"],
                "overall_strategy": "Fix configuration and retry",
                "error": str(e)
            }
    
    def generate_twitter_posts(self, blog_data, num_posts=5, include_threads=True):
        """
        Generate Twitter/X posts from blog content
        
        Args:
            blog_data (dict): Blog article data
            num_posts (int): Number of Twitter posts to generate
            include_threads (bool): Whether to include thread posts
            
        Returns:
            dict: Generated Twitter posts with metadata
        """
        try:
            headline = blog_data.get('headline', 'Industry Insights')
            key_takeaways = blog_data.get('key_takeaways', [])
            
            prompt = f"""
            Create {num_posts} engaging Twitter/X posts based on this blog:
            
            Blog headline: {headline}
            Key takeaways: {', '.join(key_takeaways[:5])}
            Include threads: {include_threads}
            
            Create a mix of:
            1. Single tweets (under 280 characters)
            2. Quote tweets with compelling statistics/insights
            3. Question tweets to drive engagement
            {'4. Thread starter (if include_threads is True)' if include_threads else ''}
            
            Twitter/X best practices:
            - Keep single tweets under 280 characters
            - Use relevant hashtags (2-3 max)
            - Include engaging hooks
            - Use emojis strategically
            - Create conversation starters
            - Mix promotional with value-driven content
            
            Return response in JSON format:
            {{
                "twitter_posts": [
                    {{
                        "tweet_content": "Tweet text with hashtags",
                        "character_count": 156,
                        "post_type": "single_tweet",
                        "hashtags": ["#hashtag1", "#hashtag2"],
                        "engagement_elements": ["question", "emoji", "statistic"],
                        "thread_position": null,
                        "retweet_potential": "high"
                    }}
                ],
                "thread_posts": [
                    {{
                        "thread_content": ["Tweet 1/n", "Tweet 2/n", "Tweet 3/n"],
                        "thread_topic": "Main thread theme",
                        "total_tweets": 3
                    }}
                ],
                "posting_strategy": "Strategy notes for optimal timing and sequence"
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            try:
                result = json.loads(response.content)
                
                # Ensure minimum content if parsing succeeds but content is missing
                if not result.get('twitter_posts'):
                    result['twitter_posts'] = [{
                        "tweet_content": f"🧵 New post: {headline[:100]}... \n\nKey insights inside 👇\n\n#contentmarketing #business",
                        "character_count": 120,
                        "post_type": "single_tweet",
                        "hashtags": ["#contentmarketing", "#business"],
                        "engagement_elements": ["emoji", "call_to_action"],
                        "thread_position": None,
                        "retweet_potential": "medium"
                    }]
                
                return result
                
            except json.JSONDecodeError:
                # Fallback with basic tweets
                fallback_tweets = []
                for i, takeaway in enumerate(key_takeaways[:3]):
                    tweet = f"💡 {takeaway[:200]}{'...' if len(takeaway) > 200 else ''}\n\n#insights #business"
                    fallback_tweets.append({
                        "tweet_content": tweet,
                        "character_count": len(tweet),
                        "post_type": "single_tweet",
                        "hashtags": ["#insights", "#business"],
                        "engagement_elements": ["emoji"],
                        "thread_position": None,
                        "retweet_potential": "medium"
                    })
                
                return {
                    "twitter_posts": fallback_tweets,
                    "thread_posts": [],
                    "posting_strategy": "Manual review recommended - parsing issue occurred",
                    "parsing_note": "Fallback content generated"
                }
                
        except Exception as e:
            return {
                "twitter_posts": [{
                    "tweet_content": f"Error generating Twitter content: {str(e)[:200]}",
                    "character_count": 0,
                    "post_type": "error",
                    "hashtags": ["#error"],
                    "engagement_elements": [],
                    "thread_position": None,
                    "retweet_potential": "none"
                }],
                "thread_posts": [],
                "posting_strategy": "Fix configuration and retry",
                "error": str(e)
            }
    
    def generate_cross_platform_campaign(self, blog_data):
        """
        Generate a coordinated social media campaign across platforms
        
        Args:
            blog_data (dict): Blog article data
            
        Returns:
            dict: Complete cross-platform campaign
        """
        try:
            linkedin_posts = self.generate_linkedin_posts(blog_data, num_posts=2)
            twitter_posts = self.generate_twitter_posts(blog_data, num_posts=3)
            
            campaign = {
                "campaign_theme": blog_data.get('headline', 'Content Marketing Campaign'),
                "linkedin_content": linkedin_posts,
                "twitter_content": twitter_posts,
                "cross_promotion_strategy": {
                    "sequence": "Start with LinkedIn thought leadership, follow with Twitter engagement",
                    "timing": "LinkedIn during business hours, Twitter in evening",
                    "content_adaptation": "Professional tone for LinkedIn, conversational for Twitter",
                    "hashtag_strategy": "Platform-specific hashtags with some overlap for brand consistency"
                },
                "campaign_duration": "1 week",
                "success_metrics": [
                    "Engagement rate by platform",
                    "Click-through rate to blog",
                    "Share/retweet count",
                    "Comment quality and responses"
                ]
            }
            
            return campaign
            
        except Exception as e:
            return {
                "campaign_theme": "Campaign Generation Error",
                "linkedin_content": {"error": str(e)},
                "twitter_content": {"error": str(e)},
                "cross_promotion_strategy": {"note": "Manual campaign planning required"},
                "error": str(e)
            }
