package com.networkbuster.ai;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Collectors;

/**
 * StoryKnowledgeLoader - Loads story data (xkcd comics) for AI training
 * Connects Java components to training data stored in JSONL format
 */
public class StoryKnowledgeLoader {
    
    private final Gson gson;
    private final Path trainingDataDir;
    
    public StoryKnowledgeLoader(String trainingDataPath) {
        this.gson = new Gson();
        this.trainingDataDir = Paths.get(trainingDataPath);
    }
    
    /**
     * Load all xkcd stories from JSONL files
     */
    public List<Story> loadStories() throws IOException {
        List<Story> stories = new ArrayList<>();
        
        // Find all JSONL files in training directory
        List<Path> jsonlFiles = Files.walk(trainingDataDir)
            .filter(p -> p.toString().endsWith(".jsonl"))
            .filter(p -> p.getFileName().toString().startsWith("xkcd-archive-"))
            .collect(Collectors.toList());
        
        System.out.println("📚 Loading xkcd stories from " + jsonlFiles.size() + " files...");
        
        for (Path file : jsonlFiles) {
            stories.addAll(loadStoriesFromFile(file));
        }
        
        System.out.println("✅ Loaded " + stories.size() + " stories for AI knowledge");
        return stories;
    }
    
    /**
     * Load stories from a single JSONL file
     */
    private List<Story> loadStoriesFromFile(Path file) throws IOException {
        List<Story> stories = new ArrayList<>();
        
        try (BufferedReader reader = Files.newBufferedReader(file)) {
            String line;
            while ((line = reader.readLine()) != null) {
                // Skip truncation markers and empty lines
                if (line.trim().isEmpty() || line.contains("truncated for brevity")) {
                    continue;
                }
                
                try {
                    JsonObject json = gson.fromJson(line, JsonObject.class);
                    Story story = parseStory(json);
                    stories.add(story);
                } catch (Exception e) {
                    System.err.println("⚠️  Failed to parse line: " + e.getMessage());
                }
            }
        }
        
        return stories;
    }
    
    /**
     * Parse a Story object from JSON
     */
    private Story parseStory(JsonObject json) {
        return new Story(
            json.get("num").getAsInt(),
            json.get("title").getAsString(),
            json.has("alt") && !json.get("alt").isJsonNull() ? json.get("alt").getAsString() : "",
            json.has("transcript") && !json.get("transcript").isJsonNull() ? json.get("transcript").getAsString() : "",
            json.has("img") && !json.get("img").isJsonNull() ? json.get("img").getAsString() : "",
            json.has("license") && !json.get("license").isJsonNull() ? json.get("license").getAsString() : "CC BY-NC 2.5",
            json.has("attribution") && !json.get("attribution").isJsonNull() ? json.get("attribution").getAsString() : "xkcd — Randall Munroe",
            json.has("source_url") && !json.get("source_url").isJsonNull() ? json.get("source_url").getAsString() : ""
        );
    }
    
    /**
     * Format stories as AI training context
     */
    public String formatAsAIKnowledge(List<Story> stories) {
        StringBuilder knowledge = new StringBuilder();
        knowledge.append("=== AI TRAINING KNOWLEDGE: XKCD STORIES ===\n\n");
        
        for (Story story : stories) {
            knowledge.append(story.toAIFormat()).append("\n\n");
        }
        
        return knowledge.toString();
    }
    
    /**
     * Save formatted knowledge to file for Python AI pipeline
     */
    public void saveAIKnowledge(List<Story> stories, String outputPath) throws IOException {
        String knowledge = formatAsAIKnowledge(stories);
        Files.write(Paths.get(outputPath), knowledge.getBytes());
        System.out.println("💾 AI knowledge saved to: " + outputPath);
    }
    
    /**
     * Main entry point - loads stories and prints as AI knowledge
     */
    public static void main(String[] args) {
        try {
            String trainingDir = args.length > 0 ? args[0] : "training";
            String outputFile = args.length > 1 ? args[1] : "training/xkcd-ai-knowledge.txt";
            
            StoryKnowledgeLoader loader = new StoryKnowledgeLoader(trainingDir);
            List<Story> stories = loader.loadStories();
            
            // Print sample stories
            System.out.println("\n=== Sample Stories as AI Knowledge ===");
            stories.stream().limit(3).forEach(s -> System.out.println(s.toAIFormat() + "\n"));
            
            // Save full knowledge base
            loader.saveAIKnowledge(stories, outputFile);
            
            // Print statistics
            System.out.println("\n=== Knowledge Statistics ===");
            System.out.println("Total stories: " + stories.size());
            System.out.println("Stories with transcripts: " + 
                stories.stream().filter(s -> !s.getTranscript().isEmpty()).count());
            System.out.println("Average title length: " + 
                stories.stream().mapToInt(s -> s.getTitle().length()).average().orElse(0));
            
        } catch (Exception e) {
            System.err.println("❌ Error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
    
    /**
     * Story class representing an xkcd comic
     */
    public static class Story {
        private final int num;
        private final String title;
        private final String alt;
        private final String transcript;
        private final String img;
        private final String license;
        private final String attribution;
        private final String sourceUrl;
        
        public Story(int num, String title, String alt, String transcript, 
                    String img, String license, String attribution, String sourceUrl) {
            this.num = num;
            this.title = title;
            this.alt = alt;
            this.transcript = transcript;
            this.img = img;
            this.license = license;
            this.attribution = attribution;
            this.sourceUrl = sourceUrl;
        }
        
        public String toAIFormat() {
            return String.format(
                "STORY #%d: %s\n" +
                "ALT_TEXT: %s\n" +
                "TRANSCRIPT: %s\n" +
                "SOURCE: %s\n" +
                "LICENSE: %s | %s",
                num, title, alt, 
                transcript.isEmpty() ? "[No transcript]" : transcript.substring(0, Math.min(200, transcript.length())) + "...",
                sourceUrl, license, attribution
            );
        }
        
        public int getNum() { return num; }
        public String getTitle() { return title; }
        public String getAlt() { return alt; }
        public String getTranscript() { return transcript; }
        public String getImg() { return img; }
        public String getLicense() { return license; }
        public String getAttribution() { return attribution; }
        public String getSourceUrl() { return sourceUrl; }
    }
}
