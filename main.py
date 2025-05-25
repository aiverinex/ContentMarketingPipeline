#!/usr/bin/env python3
"""
Content Marketing Pipeline - Main Entry Point
A CrewAI-powered workflow for automated content marketing
"""

import os
import sys
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Import our crew and configuration
from crew.crew import ContentMarketingCrew


def load_environment():
    """Load environment variables and validate configuration"""
    # Load .env file if it exists
    load_dotenv()
    
    # Check for required environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ Error: OPENAI_API_KEY environment variable is required")
        print("Please set your OpenAI API key in the .env file or environment")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    print("✅ Environment configured successfully")
    return True


def load_seed_keywords(keyword_source=None):
    """
    Load seed keywords from various sources
    
    Args:
        keyword_source (str): Source of keywords (file path, comma-separated string, or None for default)
        
    Returns:
        list: List of seed keywords
    """
    
    # If no source provided, try to load from sample file
    if not keyword_source:
        try:
            with open('sample_data/seed_keywords.txt', 'r', encoding='utf-8') as f:
                keywords = []
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        keywords.append(line)
                
                # Take first 5 keywords for default run
                return keywords[:5] if keywords else ["business automation", "digital marketing"]
                
        except FileNotFoundError:
            print("⚠️ Warning: sample_data/seed_keywords.txt not found, using default keywords")
            return ["business automation", "digital marketing", "productivity tools"]
    
    # If keyword_source is a file path
    if os.path.isfile(keyword_source):
        try:
            with open(keyword_source, 'r', encoding='utf-8') as f:
                keywords = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        keywords.append(line)
                return keywords if keywords else ["business automation"]
        except Exception as e:
            print(f"❌ Error reading keyword file {keyword_source}: {e}")
            sys.exit(1)
    
    # Otherwise, treat as comma-separated string
    keywords = [kw.strip() for kw in keyword_source.split(',') if kw.strip()]
    return keywords if keywords else ["business automation"]


def print_welcome():
    """Print welcome message and pipeline information"""
    print("=" * 60)
    print("🚀 CONTENT MARKETING PIPELINE")
    print("   Powered by CrewAI & OpenAI GPT-4o")
    print("=" * 60)
    print()
    print("This pipeline will:")
    print("  📊 Research trending topics in your industry")
    print("  ✍️  Write a 300-600 word blog article")
    print("  📱 Create LinkedIn and Twitter/X posts")
    print("  📅 Generate an optimal posting schedule")
    print()


def print_campaign_summary(results):
    """Print a summary of the campaign results"""
    print("\n" + "=" * 60)
    print("📋 CAMPAIGN SUMMARY")
    print("=" * 60)
    
    # Topic research summary
    topic_research = results.get('topic_research', {})
    trending_topics = topic_research.get('trending_topics', [])
    
    if trending_topics:
        print(f"📊 Research: Found {len(trending_topics)} trending topics")
        print(f"   Top topic: {trending_topics[0].get('title', 'N/A')}")
    
    # Blog summary
    blog_data = results.get('blog_article', {})
    if blog_data.get('headline'):
        print(f"✍️  Blog: '{blog_data.get('headline')}'")
        print(f"   Word count: {blog_data.get('word_count', 'N/A')}")
        print(f"   Reading time: {blog_data.get('reading_time', 'N/A')}")
    
    # Social media summary
    social_data = results.get('social_media', {})
    linkedin_count = len(social_data.get('linkedin_posts', {}).get('linkedin_posts', []))
    twitter_count = len(social_data.get('twitter_posts', {}).get('twitter_posts', []))
    
    if linkedin_count or twitter_count:
        print(f"📱 Social Media: {linkedin_count} LinkedIn + {twitter_count} Twitter posts")
    
    # Schedule summary
    schedule_data = results.get('posting_schedule', {})
    campaign_overview = schedule_data.get('campaign_overview', {})
    
    if campaign_overview:
        print(f"📅 Schedule: {campaign_overview.get('start_date')} to {campaign_overview.get('end_date')}")
        print(f"   Total posts: {campaign_overview.get('total_posts', 'N/A')}")
    
    print("\n📁 All results saved to the 'output/' directory")
    print("   • JSON files for detailed data")
    print("   • Markdown file for the blog article")
    print("   • CSV file for the posting schedule")
    print("   • Text summary for quick overview")


def main():
    """Main entry point for the Content Marketing Pipeline"""
    
    # Set up command line arguments
    parser = argparse.ArgumentParser(
        description="Content Marketing Pipeline - CrewAI powered content automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --keywords "AI automation, B2B SaaS, productivity"
  python main.py --keywords-file custom_keywords.txt --audience "tech startups"
  python main.py --word-count 400 --voice "casual" --timezone "EST"
        """
    )
    
    parser.add_argument(
        '--keywords', '-k',
        type=str,
        help='Comma-separated seed keywords (e.g., "AI, automation, business")'
    )
    
    parser.add_argument(
        '--keywords-file', '-kf',
        type=str,
        help='Path to file containing seed keywords (one per line)'
    )
    
    parser.add_argument(
        '--industry-context', '-i',
        type=str,
        default="",
        help='Additional industry context for topic research'
    )
    
    parser.add_argument(
        '--audience', '-a',
        type=str,
        default="B2B professionals",
        help='Target audience description (default: "B2B professionals")'
    )
    
    parser.add_argument(
        '--word-count', '-w',
        type=int,
        default=500,
        help='Target blog word count, 300-600 (default: 500)'
    )
    
    parser.add_argument(
        '--voice', '-v',
        type=str,
        default="professional",
        choices=['professional', 'casual', 'authoritative', 'friendly', 'technical'],
        help='Brand voice style (default: professional)'
    )
    
    parser.add_argument(
        '--timezone', '-tz',
        type=str,
        default="UTC",
        help='Target timezone for scheduling (default: UTC)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to custom workflow configuration JSON file'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Reduce output verbosity'
    )
    
    args = parser.parse_args()
    
    # Print welcome message unless in quiet mode
    if not args.quiet:
        print_welcome()
    
    try:
        # Load and validate environment
        load_environment()
        
        # Load seed keywords
        keyword_source = args.keywords_file or args.keywords
        seed_keywords = load_seed_keywords(keyword_source)
        
        if not args.quiet:
            print(f"🔍 Using seed keywords: {', '.join(seed_keywords[:3])}{'...' if len(seed_keywords) > 3 else ''}")
            print(f"👥 Target audience: {args.audience}")
            print(f"📝 Blog word count: {args.word_count}")
            print(f"🎯 Brand voice: {args.voice}")
            print(f"🌍 Timezone: {args.timezone}")
            print()
        
        # Validate word count
        if not (300 <= args.word_count <= 600):
            print("❌ Error: Word count must be between 300 and 600")
            sys.exit(1)
        
        # Initialize the crew
        crew = ContentMarketingCrew()
        
        # Run custom workflow if config provided
        if args.config:
            try:
                with open(args.config, 'r', encoding='utf-8') as f:
                    workflow_config = json.load(f)
                
                print(f"🔧 Running custom workflow from {args.config}")
                results = crew.run_custom_workflow(workflow_config)
                
            except FileNotFoundError:
                print(f"❌ Error: Configuration file {args.config} not found")
                sys.exit(1)
            except json.JSONDecodeError as e:
                print(f"❌ Error: Invalid JSON in configuration file: {e}")
                sys.exit(1)
        
        else:
            # Run the complete pipeline with provided parameters
            results = crew.run_complete_pipeline(
                seed_keywords=seed_keywords,
                industry_context=args.industry_context,
                target_audience=args.audience,
                word_count=args.word_count,
                brand_voice=args.voice,
                timezone=args.timezone
            )
        
        # Check for errors
        if results.get('error'):
            print(f"❌ Pipeline failed: {results['error']}")
            if results.get('details'):
                print(f"   Details: {results['details']}")
            sys.exit(1)
        
        # Print summary unless in quiet mode
        if not args.quiet:
            print_campaign_summary(results)
        
        print("\n✅ Content Marketing Pipeline completed successfully!")
        
        # Print quick access info
        if not args.quiet:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            print(f"\n🔗 Quick access:")
            print(f"   Blog article: output/blog_article_{timestamp}.md")
            print(f"   Full campaign: output/complete_campaign_{timestamp}.json")
            print(f"   Schedule: output/posting_schedule_{timestamp}.csv")
    
    except KeyboardInterrupt:
        print("\n❌ Pipeline interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        if not args.quiet:
            import traceback
            print("\nFull error trace:")
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
