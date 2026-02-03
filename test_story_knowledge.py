#!/usr/bin/env python3
"""
Test script to demonstrate xkcd story loading for AI knowledge
without requiring Google Cloud dependencies
"""

import os
import sys
from pathlib import Path

# Add training directory to path
sys.path.insert(0, str(Path(__file__).parent / 'training'))

print("=" * 60)
print("NetworkBuster AI Training Pipeline - Story Knowledge Demo")
print("=" * 60)

# Load xkcd story knowledge
print("\n📚 Loading xkcd Story Knowledge...")

try:
    from training.xkcd_knowledge_loader import XKCDKnowledgeLoader
    
    story_loader = XKCDKnowledgeLoader('training')
    stories = story_loader.load_stories()
    
    if stories:
        print(f"✅ Loaded {len(stories)} xkcd stories successfully!")
        
        # Get statistics
        stats = story_loader.get_story_statistics(stories)
        print("\n=== Story Statistics ===")
        for key, value in stats.items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        # Format and display sample knowledge
        sample_knowledge = story_loader.format_as_ai_knowledge(stories[:5])
        print("\n=== Sample Knowledge Preview (first 500 chars) ===")
        preview = sample_knowledge[:500] + "..." if len(sample_knowledge) > 500 else sample_knowledge
        print(preview)
        
        # Check if knowledge file exists
        knowledge_file = Path('training/xkcd-ai-knowledge.txt')
        if knowledge_file.exists():
            print(f"\n✅ Knowledge file exists: {knowledge_file}")
            print(f"   Size: {knowledge_file.stat().st_size} bytes")
        else:
            # Save it
            story_loader.save_ai_knowledge(stories, str(knowledge_file))
        
        print("\n🎉 Success! Java and Python are connected via xkcd story knowledge!")
        print("   Java: Loads JSONL → Formats as AI knowledge → Saves to file")
        print("   Python: Loads JSONL or reads formatted file → Uses in AI training")
        
    else:
        print("⚠️  No xkcd stories found in training directory")
        
except Exception as e:
    print(f"❌ Error loading xkcd knowledge: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Demo Complete")
print("=" * 60)
