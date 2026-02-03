#!/usr/bin/env python3
"""
xkcd_knowledge_loader.py - Loads xkcd stories as AI training knowledge
Connects Python AI pipeline to xkcd story data
"""

import json
import os
from pathlib import Path
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XKCDKnowledgeLoader:
    """Loads xkcd stories from JSONL files for AI training"""
    
    def __init__(self, training_dir: str = "training"):
        self.training_dir = Path(training_dir)
        
    def load_stories(self) -> List[Dict]:
        """Load all xkcd stories from JSONL files"""
        stories = []
        
        # Find all xkcd JSONL files
        jsonl_files = list(self.training_dir.glob("xkcd-archive-*.jsonl"))
        
        logger.info(f"📚 Loading xkcd stories from {len(jsonl_files)} files...")
        
        for file in jsonl_files:
            stories.extend(self._load_stories_from_file(file))
        
        logger.info(f"✅ Loaded {len(stories)} stories for AI knowledge")
        return stories
    
    def _load_stories_from_file(self, file_path: Path) -> List[Dict]:
        """Load stories from a single JSONL file"""
        stories = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip truncation markers and empty lines
                if not line or "truncated for brevity" in line:
                    continue
                
                try:
                    story = json.loads(line)
                    stories.append(story)
                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️  Failed to parse line: {e}")
        
        return stories
    
    def format_as_ai_knowledge(self, stories: List[Dict]) -> str:
        """Format stories as AI training context"""
        knowledge_lines = ["=== AI TRAINING KNOWLEDGE: XKCD STORIES ===\n"]
        
        for story in stories:
            formatted = self._format_story(story)
            knowledge_lines.append(formatted)
            knowledge_lines.append("")  # Empty line between stories
        
        return "\n".join(knowledge_lines)
    
    def _format_story(self, story: Dict) -> str:
        """Format a single story for AI consumption"""
        transcript = story.get('transcript', '')
        if transcript:
            # Truncate long transcripts
            transcript_preview = transcript[:200] + "..." if len(transcript) > 200 else transcript
        else:
            transcript_preview = "[No transcript]"
        
        return f"""STORY #{story.get('num')}: {story.get('title')}
ALT_TEXT: {story.get('alt', '')}
TRANSCRIPT: {transcript_preview}
SOURCE: {story.get('source_url', '')}
LICENSE: {story.get('license', 'CC BY-NC 2.5')} | {story.get('attribution', 'xkcd — Randall Munroe')}"""
    
    def save_ai_knowledge(self, stories: List[Dict], output_path: str) -> None:
        """Save formatted knowledge to file"""
        knowledge = self.format_as_ai_knowledge(stories)
        
        output_file = Path(output_path)
        output_file.write_text(knowledge, encoding='utf-8')
        
        logger.info(f"💾 AI knowledge saved to: {output_path}")
    
    def get_story_statistics(self, stories: List[Dict]) -> Dict:
        """Get statistics about the loaded stories"""
        stats = {
            'total_stories': len(stories),
            'stories_with_transcripts': sum(1 for s in stories if s.get('transcript')),
            'stories_with_alt_text': sum(1 for s in stories if s.get('alt')),
            'average_title_length': sum(len(s.get('title', '')) for s in stories) / len(stories) if stories else 0,
        }
        return stats


def main():
    """Main entry point - loads stories and prints as AI knowledge"""
    import sys
    
    training_dir = sys.argv[1] if len(sys.argv) > 1 else "training"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "training/xkcd-ai-knowledge.txt"
    
    loader = XKCDKnowledgeLoader(training_dir)
    stories = loader.load_stories()
    
    # Print sample stories
    print("\n=== Sample Stories as AI Knowledge ===")
    for story in stories[:3]:
        print(loader._format_story(story))
        print()
    
    # Save full knowledge base
    loader.save_ai_knowledge(stories, output_file)
    
    # Print statistics
    stats = loader.get_story_statistics(stories)
    print("\n=== Knowledge Statistics ===")
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
