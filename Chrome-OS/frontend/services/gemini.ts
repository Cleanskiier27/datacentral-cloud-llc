import { GoogleGenAI } from '@google/genai';

export const getSEOInsights = async (performanceSummary: string): Promise<string> => {
  try {
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY, vertexai: true });
    
    const prompt = `You are an expert Technical SEO and Search Console analyst. 
Review the following website performance summary and top queries. 
Provide 3 specific, actionable recommendations to improve search traffic and rankings. 
Keep the response concise, professional, and format it with clear bullet points. Do not use markdown bolding (**).

Data:
${performanceSummary}`;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
    });
    
    return response.text || 'No insights generated.';
  } catch (error) {
    console.error('Error generating insights:', error);
    throw new Error('Failed to generate SEO insights. Please check your API key and try again.');
  }
};
