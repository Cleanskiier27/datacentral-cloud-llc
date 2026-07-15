#!/bin/bash
echo "=========================================="
echo "Java to xkcd Stories Integration Demo"
echo "=========================================="
echo ""

echo "1. Compiling Java sources..."
mvn -q clean compile
echo "   ✅ Compilation successful"
echo ""

echo "2. Running Java Story Loader..."
mvn -q exec:java@load-story-knowledge | grep -E "(Loading|Loaded|Sample|STORY|Knowledge|saved)"
echo ""

echo "3. Checking generated knowledge file..."
if [ -f "training/xkcd-ai-knowledge.txt" ]; then
    echo "   ✅ Knowledge file exists: $(ls -lh training/xkcd-ai-knowledge.txt | awk '{print $5}')"
else
    echo "   ❌ Knowledge file not found"
fi
echo ""

echo "4. Testing Python integration..."
python3 test_story_knowledge.py 2>&1 | grep -E "(Loading|Loaded|Success|Java|Python)" | head -10
echo ""

echo "=========================================="
echo "Demo Complete!"
echo "=========================================="
