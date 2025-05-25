"""
Task definitions for Content Marketing Pipeline
Defines all tasks that agents will execute in the workflow
"""

from crewai import Task
from datetime import datetime


class ContentMarketingTasks:
    """Container for all content marketing pipeline tasks"""
    
    def __init__(self):
        self.tasks = []
    
    def topic_research_task(self, agent, seed_keywords, industry_context=""):
        """
        Task for researching trending topics
        
        Args:
            agent: TopicResearchAgent instance
            seed_keywords (list): List of seed keywords
            industry_context (str): Additional industry context
            
        Returns:
            Task: CrewAI task for topic research
        """
        keywords_str = ", ".join(seed_keywords) if isinstance(seed_keywords, list) else str(seed_keywords)
        
        task = Task(
            description=f"""
            Research and identify 3-5 trending topics in the industry based on these seed keywords: {keywords_str}
            
            Industry context: {industry_context}
            
            Your research should:
            1. Analyze current market trends and conversations
            2. Identify topics with high engagement potential
            3. Consider SEO opportunities and search volume
            4. Evaluate competition levels for each topic
            5. Suggest content angles that would resonate with the target audience
            
            For each trending topic, provide:
            - Topic title and description
            - Why it's currently trending
            - Target audience appeal and engagement potential
            - Suggested content angles and approaches
            - SEO potential score (1-10)
            - Competition analysis
            - Urgency level (high/medium/low)
            
            Focus on topics that balance trending appeal with evergreen value for long-term content strategy.
            """,
            expected_output="""
            A comprehensive research report containing:
            1. List of 3-5 trending topics with detailed analysis
            2. Market insights and industry observations  
            3. Recommended focus topic with justification
            4. Content strategy recommendations
            5. SEO and competition analysis for each topic
            
            Format: JSON structure with trending_topics array, market_insights, and recommended_focus
            """,
            agent=agent,
            output_file=f"output/topic_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        self.tasks.append(task)
        return task
    
    def blog_writing_task(self, agent, topic_data, word_count=500, brand_voice="professional"):
        """
        Task for writing blog articles
        
        Args:
            agent: BlogWriterAgent instance
            topic_data: Research data from topic research task
            word_count (int): Target word count (300-600)
            brand_voice (str): Brand voice style
            
        Returns:
            Task: CrewAI task for blog writing
        """
        task = Task(
            description=f"""
            Write a compelling, well-researched blog article based on the provided topic research data.
            
            Topic research input: {topic_data}
            Target word count: {word_count} words (must be between 300-600 words)
            Brand voice: {brand_voice}
            
            Your article should:
            1. Have an engaging headline that captures attention
            2. Include a compelling opening hook
            3. Be structured with clear subheadings and logical flow
            4. Provide actionable insights and practical value
            5. Include relevant examples or case studies
            6. End with a strong call-to-action
            7. Be optimized for SEO while maintaining readability
            8. Match the specified brand voice and tone
            
            Requirements:
            - Stay within the 300-600 word count range
            - Use markdown formatting for structure
            - Include meta description (150-160 characters)
            - Suggest relevant tags and categories
            - Provide key takeaways summary
            - Include estimated reading time
            """,
            expected_output="""
            A complete blog article package containing:
            1. SEO-optimized headline
            2. Meta description (150-160 characters)
            3. Full article content in markdown format
            4. Word count and reading time estimate
            5. Key takeaways list (3-5 bullet points)
            6. Suggested tags and categories
            7. Call-to-action text
            
            Format: JSON structure with all components properly formatted
            """,
            agent=agent,
            output_file=f"output/blog_article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        self.tasks.append(task)
        return task
    
    def social_media_task(self, agent, blog_data, platforms=["linkedin", "twitter"]):
        """
        Task for creating social media posts
        
        Args:
            agent: SocialPostAgent instance
            blog_data: Blog article data from blog writing task
            platforms (list): Target social media platforms
            
        Returns:
            Task: CrewAI task for social media content creation
        """
        platforms_str = ", ".join(platforms)
        
        task = Task(
            description=f"""
            Create engaging social media posts for {platforms_str} based on the provided blog article.
            
            Blog article data: {blog_data}
            Target platforms: {platforms}
            
            For LinkedIn posts:
            1. Create 2-3 professional, value-driven posts
            2. Use thought leadership tone and industry insights
            3. Include relevant professional hashtags (5-10)
            4. Keep under 1300 characters for optimal engagement
            5. End with engagement-driving questions or CTAs
            6. Use line breaks and emojis strategically
            
            For Twitter/X posts:
            1. Create 3-5 engaging posts of various types
            2. Include single tweets, quote tweets, and questions
            3. Create one thread starter if appropriate
            4. Keep individual tweets under 280 characters
            5. Use 2-3 relevant hashtags maximum
            6. Include engaging hooks and conversation starters
            
            Content strategy:
            - Mix promotional content with value-driven insights
            - Adapt tone for each platform's audience
            - Create posts that can work independently or as a series
            - Include clear calls-to-action driving traffic to the blog
            - Optimize for each platform's algorithm and best practices
            """,
            expected_output="""
            Complete social media content package containing:
            1. LinkedIn posts (2-3) with character counts, hashtags, and engagement tips
            2. Twitter/X posts (3-5) including single tweets and thread options
            3. Platform-specific optimization notes
            4. Posting strategy recommendations
            5. Hashtag research and suggestions
            6. Expected engagement predictions
            
            Format: JSON structure with separate arrays for each platform
            """,
            agent=agent,
            output_file=f"output/social_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        self.tasks.append(task)
        return task
    
    def scheduling_task(self, agent, content_data, audience="B2B professionals", timezone="UTC"):
        """
        Task for creating posting schedule
        
        Args:
            agent: SchedulerAgent instance
            content_data: All content from previous tasks
            audience (str): Target audience description
            timezone (str): Target timezone for scheduling
            
        Returns:
            Task: CrewAI task for content scheduling
        """
        task = Task(
            description=f"""
            Create an optimal posting schedule for the complete content marketing campaign.
            
            Content data: {content_data}
            Target audience: {audience}
            Timezone: {timezone}
            
            Your scheduling strategy should:
            1. Determine optimal posting times for each platform
            2. Consider audience behavior patterns and platform algorithms
            3. Create a logical sequence that builds momentum
            4. Avoid audience fatigue with proper spacing
            5. Maximize reach and engagement potential
            6. Account for timezone and business hours
            7. Balance promotional and value-driven content
            
            Platform-specific considerations:
            - Blog: Best days for long-form content consumption
            - LinkedIn: Professional audience business hours and networking times
            - Twitter/X: Fast-paced environment with multiple daily opportunities
            
            Schedule requirements:
            1. Specify exact dates and times for each piece of content
            2. Provide rationale for each timing decision
            3. Include preparation deadlines and workflow timing
            4. Suggest monitoring and engagement windows
            5. Create CSV export format for calendar import
            6. Include backup timing options for flexibility
            """,
            expected_output="""
            Comprehensive posting schedule containing:
            1. Campaign overview with start/end dates and strategy
            2. Blog post schedule with optimal timing and rationale
            3. LinkedIn posting schedule with business hour optimization
            4. Twitter/X posting schedule with engagement timing
            5. CSV-formatted schedule for calendar import
            6. Optimization tips and success metrics
            7. Platform-specific best practice recommendations
            
            Format: JSON structure with detailed scheduling data and CSV export
            """,
            agent=agent,
            output_file=f"output/posting_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        self.tasks.append(task)
        return task
    
    def campaign_optimization_task(self, agent, campaign_data):
        """
        Task for optimizing the complete campaign
        
        Args:
            agent: Any agent that can perform optimization analysis
            campaign_data: Complete campaign data from all previous tasks
            
        Returns:
            Task: CrewAI task for campaign optimization
        """
        task = Task(
            description=f"""
            Analyze and optimize the complete content marketing campaign for maximum impact.
            
            Campaign data: {campaign_data}
            
            Your optimization should cover:
            1. Content quality and value proposition analysis
            2. Cross-platform consistency and brand voice
            3. SEO optimization opportunities
            4. Engagement potential assessment
            5. Campaign timing and sequencing refinements
            6. Performance prediction and success metrics
            7. Risk assessment and mitigation strategies
            
            Optimization areas:
            - Headlines and hooks for better click-through rates
            - Content structure and readability improvements
            - Hashtag strategy and keyword optimization
            - Call-to-action effectiveness
            - Platform-specific content adaptations
            - Posting frequency and timing adjustments
            
            Provide actionable recommendations for:
            1. Content improvements before publishing
            2. Alternative posting strategies
            3. A/B testing opportunities
            4. Performance monitoring checkpoints
            5. Campaign success measurement criteria
            """,
            expected_output="""
            Campaign optimization report containing:
            1. Content quality assessment and improvement suggestions
            2. SEO and engagement optimization recommendations
            3. Platform-specific enhancement strategies
            4. Alternative timing and sequencing options
            5. Performance prediction with success metrics
            6. Risk analysis and mitigation strategies
            7. A/B testing recommendations
            8. Campaign monitoring and adjustment guidelines
            
            Format: JSON structure with optimization insights and actionable recommendations
            """,
            agent=agent,
            output_file=f"output/campaign_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        self.tasks.append(task)
        return task
    
    def get_all_tasks(self):
        """Return all created tasks"""
        return self.tasks
    
    def clear_tasks(self):
        """Clear all tasks for a fresh start"""
        self.tasks = []
