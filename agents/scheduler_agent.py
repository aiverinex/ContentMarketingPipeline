"""
Scheduler Agent for Content Marketing Pipeline
Suggests optimal posting schedules for maximum engagement
"""

import os
import json
from datetime import datetime, timedelta
from crewai import Agent
from langchain_openai import ChatOpenAI


class SchedulerAgent:
    """Agent responsible for optimizing content posting schedules"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.3  # Lower temperature for more consistent scheduling logic
        )
    
    def create_agent(self):
        """Create and return the scheduler agent"""
        return Agent(
            role="Content Scheduling Strategist",
            goal="Optimize content publishing schedules to maximize reach, engagement, and business impact across different platforms",
            backstory="""You are a data-driven content scheduling expert with deep knowledge of social media 
            algorithms, audience behavior patterns, and optimal posting times across different platforms and 
            industries. You understand how timing affects engagement rates, reach, and conversion metrics. 
            Your scheduling recommendations are based on platform-specific best practices, audience demographics, 
            time zones, and content type performance data. You excel at creating coordinated multi-platform 
            campaigns that maximize cumulative impact while avoiding audience fatigue.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
            memory=True
        )
    
    def generate_posting_schedule(self, content_data, target_audience="B2B professionals", timezone="UTC", campaign_duration=7):
        """
        Generate optimal posting schedule for content campaign
        
        Args:
            content_data (dict): Blog and social media content data
            target_audience (str): Target audience description
            timezone (str): Target timezone for scheduling
            campaign_duration (int): Campaign duration in days
            
        Returns:
            dict: Complete posting schedule with timing recommendations
        """
        try:
            # Get current date for scheduling
            start_date = datetime.now()
            
            # Extract content information
            blog_title = content_data.get('headline', 'Blog Post')
            linkedin_posts = content_data.get('linkedin_content', {}).get('linkedin_posts', [])
            twitter_posts = content_data.get('twitter_content', {}).get('twitter_posts', [])
            
            num_linkedin = len(linkedin_posts)
            num_twitter = len(twitter_posts)
            
            prompt = f"""
            Create an optimal posting schedule for this content campaign:
            
            Blog post: {blog_title}
            LinkedIn posts: {num_linkedin} posts
            Twitter posts: {num_twitter} posts
            Target audience: {target_audience}
            Timezone: {timezone}
            Campaign duration: {campaign_duration} days
            Start date: {start_date.strftime('%Y-%m-%d')}
            
            Consider these factors:
            1. Platform-specific optimal posting times
            2. Audience behavior patterns for {target_audience}
            3. Content type and engagement goals
            4. Avoiding audience fatigue
            5. Building momentum across platforms
            6. Weekend vs weekday performance
            
            For each piece of content, specify:
            - Optimal day of week
            - Optimal time (in {timezone})
            - Rationale for timing choice
            - Expected engagement level
            - Dependencies on other posts
            
            Return response in JSON format:
            {{
                "campaign_overview": {{
                    "start_date": "{start_date.strftime('%Y-%m-%d')}",
                    "end_date": "calculated_end_date",
                    "total_posts": {num_linkedin + num_twitter + 1},
                    "strategy": "Overall campaign strategy"
                }},
                "blog_schedule": {{
                    "publish_date": "YYYY-MM-DD",
                    "publish_time": "HH:MM",
                    "day_of_week": "Monday",
                    "rationale": "Why this timing is optimal",
                    "preparation_deadline": "YYYY-MM-DD HH:MM"
                }},
                "linkedin_schedule": [
                    {{
                        "post_index": 1,
                        "publish_date": "YYYY-MM-DD",
                        "publish_time": "HH:MM",
                        "day_of_week": "Wednesday",
                        "post_type": "thought-leadership",
                        "rationale": "Timing explanation",
                        "expected_engagement": "high"
                    }}
                ],
                "twitter_schedule": [
                    {{
                        "post_index": 1,
                        "publish_date": "YYYY-MM-DD",
                        "publish_time": "HH:MM",
                        "day_of_week": "Friday",
                        "post_type": "engagement",
                        "rationale": "Timing explanation",
                        "expected_engagement": "medium"
                    }}
                ],
                "optimization_tips": [
                    "tip1",
                    "tip2",
                    "tip3"
                ],
                "success_metrics": [
                    "metric1",
                    "metric2"
                ]
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            try:
                result = json.loads(response.content)
                
                # Validate and enhance the schedule
                if not result.get('campaign_overview'):
                    result['campaign_overview'] = {
                        "start_date": start_date.strftime('%Y-%m-%d'),
                        "end_date": (start_date + timedelta(days=campaign_duration)).strftime('%Y-%m-%d'),
                        "total_posts": num_linkedin + num_twitter + 1,
                        "strategy": "Balanced cross-platform content distribution"
                    }
                
                # Add CSV export data
                result['csv_export'] = self._generate_csv_data(result)
                
                return result
                
            except json.JSONDecodeError:
                # Generate fallback schedule
                return self._generate_fallback_schedule(
                    start_date, campaign_duration, num_linkedin, num_twitter, blog_title
                )
                
        except Exception as e:
            return {
                "campaign_overview": {
                    "start_date": datetime.now().strftime('%Y-%m-%d'),
                    "error": str(e),
                    "total_posts": 0,
                    "strategy": "Manual scheduling required due to error"
                },
                "blog_schedule": {},
                "linkedin_schedule": [],
                "twitter_schedule": [],
                "optimization_tips": ["Check API configuration", "Retry scheduling"],
                "success_metrics": ["Manual tracking required"],
                "error": str(e)
            }
    
    def _generate_fallback_schedule(self, start_date, duration, num_linkedin, num_twitter, blog_title):
        """Generate a basic fallback schedule when AI parsing fails"""
        
        schedule = {
            "campaign_overview": {
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": (start_date + timedelta(days=duration)).strftime('%Y-%m-%d'),
                "total_posts": num_linkedin + num_twitter + 1,
                "strategy": "Standard weekly distribution - manual optimization recommended"
            },
            "blog_schedule": {
                "publish_date": (start_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                "publish_time": "09:00",
                "day_of_week": "Tuesday",
                "rationale": "Tuesday morning for B2B audience engagement",
                "preparation_deadline": start_date.strftime('%Y-%m-%d 17:00')
            },
            "linkedin_schedule": [],
            "twitter_schedule": [],
            "optimization_tips": [
                "Post blog content early in the week",
                "Schedule LinkedIn during business hours",
                "Use Twitter for evening engagement"
            ],
            "success_metrics": [
                "Engagement rate",
                "Click-through rate",
                "Share count"
            ]
        }
        
        # Add LinkedIn posts (Wednesday and Friday)
        linkedin_days = [3, 5]  # Wednesday, Friday
        for i in range(min(num_linkedin, len(linkedin_days))):
            post_date = start_date + timedelta(days=linkedin_days[i])
            schedule["linkedin_schedule"].append({
                "post_index": i + 1,
                "publish_date": post_date.strftime('%Y-%m-%d'),
                "publish_time": "10:00",
                "day_of_week": post_date.strftime('%A'),
                "post_type": "professional",
                "rationale": "Business hours for professional audience",
                "expected_engagement": "medium"
            })
        
        # Add Twitter posts (spread throughout week)
        twitter_days = [2, 4, 6]  # Tuesday, Thursday, Saturday
        for i in range(min(num_twitter, len(twitter_days))):
            post_date = start_date + timedelta(days=twitter_days[i])
            schedule["twitter_schedule"].append({
                "post_index": i + 1,
                "publish_date": post_date.strftime('%Y-%m-%d'),
                "publish_time": "18:00",
                "day_of_week": post_date.strftime('%A'),
                "post_type": "engagement",
                "rationale": "Evening hours for higher Twitter engagement",
                "expected_engagement": "medium"
            })
        
        schedule['csv_export'] = self._generate_csv_data(schedule)
        
        return schedule
    
    def _generate_csv_data(self, schedule_data):
        """Generate CSV-formatted schedule data"""
        csv_rows = []
        
        # Add blog schedule
        if schedule_data.get('blog_schedule'):
            blog = schedule_data['blog_schedule']
            csv_rows.append({
                "Content_Type": "Blog Post",
                "Platform": "Website",
                "Publish_Date": blog.get('publish_date', ''),
                "Publish_Time": blog.get('publish_time', ''),
                "Day_of_Week": blog.get('day_of_week', ''),
                "Expected_Engagement": "High",
                "Notes": blog.get('rationale', '')
            })
        
        # Add LinkedIn schedule
        for post in schedule_data.get('linkedin_schedule', []):
            csv_rows.append({
                "Content_Type": f"LinkedIn Post {post.get('post_index', '')}",
                "Platform": "LinkedIn",
                "Publish_Date": post.get('publish_date', ''),
                "Publish_Time": post.get('publish_time', ''),
                "Day_of_Week": post.get('day_of_week', ''),
                "Expected_Engagement": post.get('expected_engagement', 'Medium'),
                "Notes": post.get('rationale', '')
            })
        
        # Add Twitter schedule
        for post in schedule_data.get('twitter_schedule', []):
            csv_rows.append({
                "Content_Type": f"Twitter Post {post.get('post_index', '')}",
                "Platform": "Twitter/X",
                "Publish_Date": post.get('publish_date', ''),
                "Publish_Time": post.get('publish_time', ''),
                "Day_of_Week": post.get('day_of_week', ''),
                "Expected_Engagement": post.get('expected_engagement', 'Medium'),
                "Notes": post.get('rationale', '')
            })
        
        return csv_rows
    
    def optimize_posting_frequency(self, audience_data, content_volume, platform="all"):
        """
        Optimize posting frequency based on audience and content volume
        
        Args:
            audience_data (dict): Audience information and preferences
            content_volume (int): Amount of content to schedule
            platform (str): Target platform or "all"
            
        Returns:
            dict: Frequency optimization recommendations
        """
        try:
            prompt = f"""
            Optimize posting frequency for this content campaign:
            
            Audience data: {json.dumps(audience_data)}
            Content volume: {content_volume} pieces
            Target platform: {platform}
            
            Provide recommendations for:
            1. Optimal posting frequency per platform
            2. Spacing between posts to avoid fatigue
            3. Peak engagement windows
            4. Content mix ratios (promotional vs educational vs engaging)
            
            Return response in JSON format:
            {{
                "frequency_recommendations": {{
                    "linkedin": "X posts per week",
                    "twitter": "X posts per day",
                    "blog": "X posts per month"
                }},
                "spacing_guidelines": {{
                    "minimum_hours_between_posts": 4,
                    "optimal_daily_limit": 3,
                    "weekend_adjustment": "reduce by 50%"
                }},
                "engagement_windows": [
                    {{
                        "platform": "LinkedIn",
                        "best_times": ["09:00", "12:00", "17:00"],
                        "best_days": ["Tuesday", "Wednesday", "Thursday"]
                    }}
                ],
                "content_mix_ratio": {{
                    "educational": "60%",
                    "promotional": "20%",
                    "engaging": "20%"
                }}
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                return {
                    "frequency_recommendations": {
                        "linkedin": "3-5 posts per week",
                        "twitter": "3-7 posts per day",
                        "blog": "2-4 posts per month"
                    },
                    "spacing_guidelines": {
                        "minimum_hours_between_posts": 4,
                        "optimal_daily_limit": 3,
                        "weekend_adjustment": "reduce by 50%"
                    },
                    "note": "Default recommendations provided - manual optimization suggested"
                }
                
        except Exception as e:
            return {
                "frequency_recommendations": {"error": str(e)},
                "spacing_guidelines": {"error": str(e)},
                "note": "Error occurred during frequency optimization"
            }
