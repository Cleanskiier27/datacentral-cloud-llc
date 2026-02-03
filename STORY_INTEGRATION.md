# Java to xkcd Stories Integration

This integration connects Java components to xkcd story data for AI training knowledge on the server.

## Overview

The system provides two paths for loading xkcd stories as AI training knowledge:
1. **Java**: Compiles and runs Java code to load, format, and save story knowledge
2. **Python**: Loads stories directly in Python for use in the AI training pipeline

Both paths produce the same formatted output that can be used by the AI training system.

## Components

### Java Story Loader
- **Location**: `src/main/java/com/networkbuster/ai/StoryKnowledgeLoader.java`
- **Purpose**: Loads xkcd JSONL files, parses with GSON, formats as AI knowledge
- **Output**: `training/xkcd-ai-knowledge.txt`

### Python Story Loader
- **Location**: `training/xkcd_knowledge_loader.py`
- **Purpose**: Same functionality as Java, integrated with AI pipeline
- **Output**: Formatted knowledge text or direct use in training

### AI Training Pipeline Integration
- **Location**: `ai-training-pipeline.py`
- **Class**: `XKCDStoryContextLoader`
- **Purpose**: Loads story knowledge into AI training context

## Usage

### Using Java (Maven)

Compile and load stories:
```bash
# Compile Java sources
mvn clean compile

# Run the story knowledge loader
mvn exec:java@load-story-knowledge
```

This will:
1. Load all `xkcd-archive-*.jsonl` files from the `training/` directory
2. Parse and format them as AI training knowledge
3. Save to `training/xkcd-ai-knowledge.txt`
4. Print statistics and sample output

### Using Python

Run the standalone loader:
```bash
python3 training/xkcd_knowledge_loader.py training training/xkcd-ai-knowledge.txt
```

Or use in your Python code:
```python
from training.xkcd_knowledge_loader import XKCDKnowledgeLoader

loader = XKCDKnowledgeLoader('training')
stories = loader.load_stories()
knowledge = loader.format_as_ai_knowledge(stories)
```

### Testing the Integration

Run the test script to verify everything works:
```bash
python3 test_story_knowledge.py
```

## Output Format

Stories are formatted as AI training knowledge:

```
=== AI TRAINING KNOWLEDGE: XKCD STORIES ===

STORY #401: Large Hadron Collider
ALT_TEXT: When charged particles of more than 5 TeV pass through...
TRANSCRIPT: The Large Hadron Collider, CERN...
SOURCE: https://xkcd.com/401/
LICENSE: CC BY-NC 2.5 | xkcd — Randall Munroe

STORY #402: 1,000 Miles North
ALT_TEXT: Twister would've been a much better movie...
TRANSCRIPT: [[Van and truck travel toward mountains]]...
SOURCE: https://xkcd.com/402/
LICENSE: CC BY-NC 2.5 | xkcd — Randall Munroe
```

## Data Flow

```
xkcd JSONL files (training/xkcd-archive-*.jsonl)
         ↓
    ┌────┴────┐
    │         │
  Java      Python
(GSON)    (json lib)
    │         │
    └────┬────┘
         ↓
  Formatted AI Knowledge
(training/xkcd-ai-knowledge.txt)
         ↓
  AI Training Pipeline
(ai-training-pipeline.py)
         ↓
    Server Display
```

## Dependencies

### Java
- Java 17+
- Maven 3.x
- GSON 2.10.1 (added to pom.xml)

### Python
- Python 3.x
- No external dependencies for story loading
- Google Cloud libraries needed only for full AI pipeline

## Adding More Stories

To add more xkcd stories:

1. Run the fetch script to download more comics:
```bash
python3 training/fetch_xkcd.py --start 1 --end 1000 --chunk-size 100 --outdir training
```

2. Reload the knowledge:
```bash
mvn exec:java@load-story-knowledge
```

The system will automatically find and load all `xkcd-archive-*.jsonl` files.

## Integration with AI Training

The knowledge is integrated into the AI training pipeline through the `XKCDStoryContextLoader` class:

```python
# In ai-training-pipeline.py
story_loader = XKCDStoryContextLoader()
story_knowledge = story_loader.get_story_context_for_training(max_stories=100)
```

This provides the AI model with contextual knowledge from xkcd comics during training.

## License

The xkcd stories are used under CC BY-NC 2.5 license, with proper attribution to Randall Munroe.
