from src.states.blogstate import BlogState

class BlogNode:
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            prompt = """You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly"""
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}

    def title_creation_from_transcript(self, state: BlogState):
        transcript = state["transcript"]
        prompt = """You are an expert blog content writer. Use Markdown formatting.
        Based on this YouTube video transcript, generate a creative and SEO friendly blog title.
        Important: Always write in English only, regardless of transcript language.
        
        Transcript: {transcript}"""
        system_message = prompt.format(transcript=transcript[:15000])
        response = self.llm.invoke(system_message)
        return {"blog": {"title": response.content}}

    def content_generation(self, state: BlogState):
        title = state["blog"]["title"]

        if state.get("transcript"):
            prompt = """You are an expert blog writer. Use Markdown formatting.
            Based on this YouTube video transcript, write detailed blog content for the title: {title}
            Do NOT repeat or include the title in the content. Start directly with the introduction.
            Important: Always write in English only, regardless of transcript language.
            
            Transcript: {transcript}"""
            system_message = prompt.format(title=title, transcript=state["transcript"][:3000])

        else:
            prompt = """You are expert blog writer. Use Markdown formatting.
            Generate detailed blog content with detailed breakdown for the {topic}.
            Do NOT include the title in the content. Start directly with the introduction."""
            system_message = prompt.format(topic=state["topic"])

        response = self.llm.invoke(system_message)
        return {"blog": {"title": title, "content": response.content}}