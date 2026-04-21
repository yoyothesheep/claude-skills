# CONFIG — distribute-social
# Copy this file to CONFIG.md and fill in your values. CONFIG.md is gitignored.

SITE_URL=https://your-site.com
BRAND_VOICE_NOTES=docs/your-tone-guide.md   # path to your tone/voice guide

REDDIT_OUTPUT_PATH=docs/your-output-path/
SUBREDDITS_TIER1=sub1,sub2,sub3
SUBREDDITS_TIER2=sub4,sub5
SUBREDDITS_TIER3=sub6,sub7

# Pipe-separated search query templates — [topic keywords] is substituted at runtime
SEARCH_QUERIES=site:reddit.com/r/sub1 [topic keywords] | site:reddit.com/r/sub2 [topic keywords] | site:reddit.com "[niche phrase]" this week

# Tone per subreddit — pipe-separated: r/subname: tone description
SUBREDDIT_TONES=r/sub1: tone description | r/sub2: tone description

# Thread type → angle map
THREAD_ANGLES=<<END
"[thread pattern]" → [angle: what to lead with, what data to cite, how to place the link]
END

# 2–3 example standalone post titles that reflect your site's voice and topic range
STANDALONE_TITLE_EXAMPLES=Example title 1 | Example title 2

# Optional: additional quote sources for LinkedIn posts
# QUOTE_SOURCE_1=https://example.com/
