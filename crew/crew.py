"""
Main Crew configuration for Content Marketing Pipeline
Orchestrates all agents and tasks in the content marketing workflow
"""

import os
import json
from datetime import datetime
from crewai import Crew, Process
from agents.topic_research_agent import TopicResearchAgent
from agents.blog_writer_agent import BlogWriterAgent
from agents.social_post_agent import SocialPostAgent
from agents.scheduler_agent import SchedulerAgent
from tasks.task import ContentMarketingTasks


class ContentMarketingCrew:
    """Main crew orchestrator for the content marketing pipeline"""
    
    def __init__(self):
        # Initialize all agents
        self.topic_research_agent = TopicResearchAgent()
        self.blog_writer_agent = BlogWriterAgent()
        self.social_post_agent = SocialPostAgent()
        self.scheduler_agent = SchedulerAgent()
        
        # Initialize task manager
        self.task_manager = ContentMarketingTasks()
        
        # Create agent instances
        self.agents = {
            'researcher': self.topic_research_agent.create_agent(),
            'writer': self.blog_writer_agent.create_agent(),
            'social_manager': self.social_post_agent.create_agent(),
            'scheduler': self.scheduler_agent.create_agent()
        }
        
        # Ensure output directory exists
        os.makedirs('output', exist_ok=True)
    
    def run_complete_pipeline(self, seed_keywords, industry_context="", target_audience="B2B professionals", 
                            word_count=500, brand_voice="professional", timezone="UTC"):
        """
        Run the complete content marketing pipeline
        
        Args:
            seed_keywords (list or str): Seed keywords for topic research
            industry_context (str): Additional industry context
            target_audience (str): Target audience description
            word_count (int): Target blog word count (300-600)
            brand_voice (str): Brand voice style
            timezone (str): Target timezone for scheduling
            
        Returns:
            dict: Complete pipeline results
        """
        try:
            print("🚀 Starting Content Marketing Pipeline...")
            
            # Convert seed_keywords to list if string
            if isinstance(seed_keywords, str):
                seed_keywords = [kw.strip() for kw in seed_keywords.split(',')]
            
            # Step 1: Topic Research
            print("📊 Step 1: Researching trending topics...")
            topic_results = self._run_topic_research(seed_keywords, industry_context)
            
            if not topic_results or 'error' in topic_results:
                print("❌ Topic research failed. Check your API configuration.")
                return {"error": "Topic research failed", "details": topic_results}
            
            # Step 2: Blog Writing
            print("✍️ Step 2: Writing blog article...")
            blog_results = self._run_blog_writing(topic_results, word_count, brand_voice)
            
            if not blog_results or 'error' in blog_results:
                print("❌ Blog writing failed.")
                return {"error": "Blog writing failed", "details": blog_results}
            
            # Step 3: Social Media Posts
            print("📱 Step 3: Creating social media posts...")
            social_results = self._run_social_media_creation(blog_results)
            
            if not social_results or 'error' in social_results:
                print("❌ Social media creation failed.")
                return {"error": "Social media creation failed", "details": social_results}
            
            # Step 4: Scheduling
            print("📅 Step 4: Creating posting schedule...")
            
            # Combine all content for scheduling
            complete_content = {
                **blog_results,
                'linkedin_content': social_results.get('linkedin_posts', {}),
                'twitter_content': social_results.get('twitter_posts', {})
            }
            
            schedule_results = self._run_scheduling(complete_content, target_audience, timezone)
            
            if not schedule_results or 'error' in schedule_results:
                print("❌ Scheduling failed.")
                return {"error": "Scheduling failed", "details": schedule_results}
            
            # Step 5: Compile final results
            print("📋 Step 5: Compiling final campaign...")
            final_campaign = self._compile_final_campaign(
                topic_results, blog_results, social_results, schedule_results
            )
            
            # Save complete campaign
            self._save_campaign_files(final_campaign)
            
            print("✅ Content Marketing Pipeline completed successfully!")
            print(f"📁 Results saved to output/ directory")
            
            return final_campaign
            
        except Exception as e:
            error_msg = f"Pipeline execution failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg, "timestamp": datetime.now().isoformat()}
    
    def _run_topic_research(self, seed_keywords, industry_context):
        """Execute topic research phase"""
        try:
            # Use the agent's research method directly for more control
            results = self.topic_research_agent.research_topics(seed_keywords, industry_context)
            
            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"output/topic_research_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"   ✓ Topic research completed. Results saved to {output_file}")
            
            return results
            
        except Exception as e:
            print(f"   ✗ Topic research error: {str(e)}")
            return {"error": str(e)}
    
    def _run_blog_writing(self, topic_results, word_count, brand_voice):
        """Execute blog writing phase"""
        try:
            # Get the top recommended topic
            trending_topics = topic_results.get('trending_topics', [])
            if not trending_topics:
                return {"error": "No trending topics available for blog writing"}
            
            # Use the first topic or recommended focus
            top_topic = trending_topics[0]
            
            # Use the agent's writing method directly
            results = self.blog_writer_agent.write_blog_article(top_topic, word_count, brand_voice)
            
            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"output/blog_article_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            # Also save as markdown file
            if results.get('article_content'):
                md_file = f"output/blog_article_{timestamp}.md"
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {results.get('headline', 'Blog Article')}\n\n")
                    f.write(f"*{results.get('meta_description', '')}*\n\n")
                    f.write(f"{results.get('article_content', '')}\n\n")
                    f.write(f"**Reading time:** {results.get('reading_time', 'Unknown')}\n\n")
                    f.write(f"**Tags:** {', '.join(results.get('suggested_tags', []))}\n")
                
                print(f"   ✓ Blog article completed. Results saved to {output_file} and {md_file}")
            
            return results
            
        except Exception as e:
            print(f"   ✗ Blog writing error: {str(e)}")
            return {"error": str(e)}
    
    def _run_social_media_creation(self, blog_results):
        """Execute social media content creation phase"""
        try:
            # Generate LinkedIn posts
            linkedin_results = self.social_post_agent.generate_linkedin_posts(blog_results, num_posts=2)
            
            # Generate Twitter posts
            twitter_results = self.social_post_agent.generate_twitter_posts(blog_results, num_posts=3)
            
            # Combine results
            social_results = {
                "linkedin_posts": linkedin_results,
                "twitter_posts": twitter_results,
                "campaign_summary": {
                    "total_linkedin_posts": len(linkedin_results.get('linkedin_posts', [])),
                    "total_twitter_posts": len(twitter_results.get('twitter_posts', [])),
                    "content_themes": linkedin_results.get('content_themes', []) + 
                                    twitter_results.get('content_themes', [])
                }
            }
            
            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"output/social_posts_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(social_results, f, indent=2, ensure_ascii=False)
            
            print(f"   ✓ Social media posts completed. Results saved to {output_file}")
            
            return social_results
            
        except Exception as e:
            print(f"   ✗ Social media creation error: {str(e)}")
            return {"error": str(e)}
    
    def _run_scheduling(self, content_data, target_audience, timezone):
        """Execute scheduling phase"""
        try:
            # Use the agent's scheduling method directly
            results = self.scheduler_agent.generate_posting_schedule(
                content_data, target_audience, timezone, campaign_duration=7
            )
            
            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"output/posting_schedule_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            # Save CSV schedule if available
            if results.get('csv_export'):
                csv_file = f"output/posting_schedule_{timestamp}.csv"
                self._save_csv_schedule(results['csv_export'], csv_file)
                print(f"   ✓ Schedule completed. Results saved to {output_file} and {csv_file}")
            else:
                print(f"   ✓ Schedule completed. Results saved to {output_file}")
            
            return results
            
        except Exception as e:
            print(f"   ✗ Scheduling error: {str(e)}")
            return {"error": str(e)}
    
    def _save_csv_schedule(self, csv_data, filename):
        """Save schedule data as CSV file"""
        try:
            import csv
            
            if not csv_data:
                return
            
            # Get field names from first row
            fieldnames = csv_data[0].keys() if csv_data else []
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
                
        except Exception as e:
            print(f"   ⚠️ Warning: Could not save CSV schedule: {str(e)}")
    
    def _compile_final_campaign(self, topic_results, blog_results, social_results, schedule_results):
        """Compile all results into final campaign package"""
        
        campaign = {
            "campaign_metadata": {
                "generated_at": datetime.now().isoformat(),
                "pipeline_version": "1.0.0",
                "status": "completed"
            },
            "topic_research": topic_results,
            "blog_article": blog_results,
            "social_media": social_results,
            "posting_schedule": schedule_results,
            "campaign_summary": {
                "total_content_pieces": (
                    1 +  # blog post
                    len(social_results.get('linkedin_posts', {}).get('linkedin_posts', [])) +
                    len(social_results.get('twitter_posts', {}).get('twitter_posts', []))
                ),
                "estimated_reach": "Varies by audience size and engagement",
                "campaign_duration": schedule_results.get('campaign_overview', {}).get('end_date', 'Unknown'),
                "key_topics": topic_results.get('trending_topics', [])[:3] if topic_results else [],
                "success_metrics": schedule_results.get('success_metrics', [])
            }
        }
        
        return campaign
    
    def _save_campaign_files(self, campaign):
        """Save final campaign in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save complete campaign as JSON
        campaign_file = f"output/complete_campaign_{timestamp}.json"
        with open(campaign_file, 'w', encoding='utf-8') as f:
            json.dump(campaign, f, indent=2, ensure_ascii=False)
        
        # Save campaign summary as text
        summary_file = f"output/campaign_summary_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("CONTENT MARKETING CAMPAIGN SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            
            # Blog info
            blog_data = campaign.get('blog_article', {})
            f.write(f"📝 BLOG ARTICLE\n")
            f.write(f"Headline: {blog_data.get('headline', 'N/A')}\n")
            f.write(f"Word Count: {blog_data.get('word_count', 'N/A')}\n")
            f.write(f"Reading Time: {blog_data.get('reading_time', 'N/A')}\n\n")
            
            # Social media info
            social_data = campaign.get('social_media', {})
            linkedin_count = len(social_data.get('linkedin_posts', {}).get('linkedin_posts', []))
            twitter_count = len(social_data.get('twitter_posts', {}).get('twitter_posts', []))
            
            f.write(f"📱 SOCIAL MEDIA CONTENT\n")
            f.write(f"LinkedIn Posts: {linkedin_count}\n")
            f.write(f"Twitter Posts: {twitter_count}\n\n")
            
            # Schedule info
            schedule_data = campaign.get('posting_schedule', {})
            campaign_overview = schedule_data.get('campaign_overview', {})
            
            f.write(f"📅 POSTING SCHEDULE\n")
            f.write(f"Campaign Start: {campaign_overview.get('start_date', 'N/A')}\n")
            f.write(f"Campaign End: {campaign_overview.get('end_date', 'N/A')}\n")
            f.write(f"Total Posts: {campaign_overview.get('total_posts', 'N/A')}\n\n")
            
            # Success metrics
            metrics = schedule_data.get('success_metrics', [])
            if metrics:
                f.write(f"📊 SUCCESS METRICS\n")
                for metric in metrics:
                    f.write(f"• {metric}\n")
        
        print(f"   ✓ Final campaign saved as {campaign_file} and {summary_file}")
    
    def run_custom_workflow(self, workflow_config):
        """
        Run a custom workflow based on configuration
        
        Args:
            workflow_config (dict): Custom workflow configuration
            
        Returns:
            dict: Workflow results
        """
        try:
            print("🔧 Running custom workflow...")
            
            # Extract configuration
            steps = workflow_config.get('steps', ['research', 'blog', 'social', 'schedule'])
            params = workflow_config.get('parameters', {})
            
            results = {}
            
            # Execute each step based on configuration
            if 'research' in steps:
                seed_keywords = params.get('seed_keywords', ['business', 'technology'])
                industry_context = params.get('industry_context', '')
                results['research'] = self._run_topic_research(seed_keywords, industry_context)
            
            if 'blog' in steps and results.get('research'):
                word_count = params.get('word_count', 500)
                brand_voice = params.get('brand_voice', 'professional')
                results['blog'] = self._run_blog_writing(results['research'], word_count, brand_voice)
            
            if 'social' in steps and results.get('blog'):
                results['social'] = self._run_social_media_creation(results['blog'])
            
            if 'schedule' in steps and results.get('blog'):
                content_data = {**results['blog']}
                if results.get('social'):
                    content_data.update({
                        'linkedin_content': results['social'].get('linkedin_posts', {}),
                        'twitter_content': results['social'].get('twitter_posts', {})
                    })
                
                target_audience = params.get('target_audience', 'B2B professionals')
                timezone = params.get('timezone', 'UTC')
                results['schedule'] = self._run_scheduling(content_data, target_audience, timezone)
            
            print("✅ Custom workflow completed!")
            return results
            
        except Exception as e:
            error_msg = f"Custom workflow failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}
