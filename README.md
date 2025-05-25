# Content Marketing Pipeline

A production-ready CrewAI-powered workflow that automates content marketing from topic research to scheduling. This project follows the [CrewAI Marketplace Template](https://github.com/crewAIInc/marketplace-crew-template) standards and is compatible with [CrewAI Marketplace](https://marketplace.crewai.com) submission requirements.

## 🎯 Project Purpose

Transform your content marketing process with AI automation. This pipeline:

- **Researches trending topics** in your industry using AI-powered analysis
- **Writes compelling blog articles** (300-600 words) optimized for engagement
- **Generates social media posts** for LinkedIn and Twitter/X platforms
- **Creates optimal posting schedules** to maximize reach and engagement

Perfect for content marketers, social media managers, and businesses looking to scale their content production while maintaining quality.

## 🚀 Features

- **4 Specialized AI Agents** working in harmony
- **Multi-platform content generation** (Blog, LinkedIn, Twitter/X)
- **Intelligent scheduling** with timing optimization
- **Multiple output formats** (JSON, Markdown, CSV, Text)
- **Configurable workflows** for different use cases
- **Production-ready code** with comprehensive error handling

## 📁 Project Structure

```
content-marketing-pipeline/
├── agents/
│   ├── topic_research_agent.py    # AI agent for trending topic research
│   ├── blog_writer_agent.py       # AI agent for blog article writing
│   ├── social_post_agent.py       # AI agent for social media content
│   └── scheduler_agent.py         # AI agent for posting schedule optimization
├── tasks/
│   └── task.py                    # Task definitions for all workflow steps
├── crew/
│   └── crew.py                    # Main crew orchestration and pipeline logic
├── config/
│   └── config.yaml                # Configuration settings and parameters
├── sample_data/
│   └── seed_keywords.txt          # Sample keywords for testing
├── main.py                        # Main entry point and CLI interface
├── README.md                      # This file
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── LICENSE                        # MIT license
└── pyproject.toml                 # Python dependencies
```

## ⚙️ How It Works

The pipeline executes 4 sequential steps:

1. **📊 Topic Research**: AI analyzes seed keywords to identify trending topics with high engagement potential
2. **✍️ Blog Writing**: Creates compelling 300-600 word articles optimized for SEO and readability  
3. **📱 Social Media**: Generates platform-specific posts for LinkedIn (professional) and Twitter/X (conversational)
4. **📅 Scheduling**: Creates optimal posting schedule based on audience behavior and platform algorithms

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd content-marketing-pipeline
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if using the included pyproject.toml:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   ```

### Getting Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key that starts with `sk-`
5. Add it to your `.env` file

## 🚀 Usage

### Basic Usage

Run the pipeline with default settings:
```bash
python main.py
```

### Custom Keywords

Specify your own keywords:
```bash
python main.py --keywords "AI automation, B2B SaaS, productivity tools"
```

### Advanced Options

```bash
python main.py \
  --keywords "fintech, blockchain, digital payments" \
  --audience "financial technology professionals" \
  --word-count 450 \
  --voice "authoritative" \
  --timezone "EST"
```

### Using CrewAI CLI

Test your crew of AI agents:
```bash
crewai run
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--keywords` | Comma-separated seed keywords | Sample keywords from file |
| `--keywords-file` | Path to file with keywords (one per line) | `sample_data/seed_keywords.txt` |
| `--industry-context` | Additional industry context | None |
| `--audience` | Target audience description | "B2B professionals" |
| `--word-count` | Blog article word count (300-600) | 500 |
| `--voice` | Brand voice style | "professional" |
| `--timezone` | Target timezone for scheduling | "UTC" |
| `--quiet` | Reduce output verbosity | False |

## 📤 Output

The pipeline generates comprehensive content marketing materials:

### Files Created
- **`blog_article_[timestamp].md`** - Markdown formatted blog article
- **`blog_article_[timestamp].json`** - Blog article with metadata
- **`social_posts_[timestamp].json`** - LinkedIn and Twitter posts
- **`posting_schedule_[timestamp].csv`** - Calendar-ready posting schedule
- **`complete_campaign_[timestamp].json`** - Full campaign package
- **`campaign_summary_[timestamp].txt`** - Quick overview summary

### Example Output Structure
```json
{
  "blog_article": {
    "headline": "Harnessing AI for Digital Transformation",
    "word_count": 500,
    "reading_time": "3 min read",
    "article_content": "Full markdown content...",
    "key_takeaways": ["insight1", "insight2", "insight3"]
  },
  "social_media": {
    "linkedin_posts": [{"post_content": "...", "hashtags": [...]}],
    "twitter_posts": [{"tweet_content": "...", "character_count": 245}]
  },
  "posting_schedule": {
    "campaign_overview": {"start_date": "2024-05-25", "total_posts": 5},
    "blog_schedule": {"publish_date": "2024-05-26", "publish_time": "09:00"},
    "linkedin_schedule": [...],
    "twitter_schedule": [...]
  }
}
```

## 🎯 Example Input/Output

### Input
```bash
python main.py --keywords "artificial intelligence, machine learning, business automation"
```

### Output
- **Blog**: "The Role of AI in Driving Digital Transformation" (500 words)
- **LinkedIn**: 2 professional posts about AI implementation strategies
- **Twitter**: 3 engaging posts about AI trends and insights  
- **Schedule**: 7-day strategic posting plan with optimal timing

The generated content includes real case studies, actionable insights, and platform-optimized messaging for maximum engagement.

## 🔧 Configuration

Customize the pipeline behavior by editing `config/config.yaml`:

```yaml
content:
  blog:
    default_word_count: 500
    default_brand_voice: "professional"
  social_media:
    linkedin:
      posts_per_campaign: 2
      max_character_count: 1300
    twitter:
      posts_per_campaign: 3
      max_character_count: 280
```

## 🤖 AI Agents

### TopicResearchAgent
- **Role**: Content Topic Research Specialist
- **Goal**: Identify trending topics with high engagement potential
- **Capabilities**: Market analysis, trend identification, SEO scoring

### BlogWriterAgent  
- **Role**: Expert Content Writer
- **Goal**: Create compelling, well-researched blog articles
- **Capabilities**: SEO optimization, brand voice adaptation, structured writing

### SocialPostAgent
- **Role**: Social Media Content Specialist  
- **Goal**: Transform blog content into platform-optimized social posts
- **Capabilities**: Platform-specific formatting, hashtag strategy, engagement optimization

### SchedulerAgent
- **Role**: Content Scheduling Strategist
- **Goal**: Optimize posting schedules for maximum reach and engagement
- **Capabilities**: Audience behavior analysis, timing optimization, campaign coordination

## 📋 Requirements

- Python 3.8+
- OpenAI API access
- Internet connection for API calls

## 🛡️ CrewAI Marketplace Compliance

This project follows the [CrewAI Marketplace Template](https://github.com/crewAIInc/marketplace-crew-template) standards and is ready for submission to [CrewAI Marketplace](https://marketplace.crewai.com).

**Compliance Features:**
- ✅ Standard project structure
- ✅ Comprehensive documentation
- ✅ Environment variable configuration
- ✅ Production-ready error handling
- ✅ Multiple output formats
- ✅ CLI interface with options
- ✅ Example data and configurations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check the [CrewAI Documentation](https://docs.crewai.com)
- Visit [CrewAI Marketplace](https://marketplace.crewai.com)

---

**Ready to transform your content marketing with AI? Get started today!**
