import os
from src.generator import MinutesGenerator
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

SAMPLE_TRANSCRIPT = """
[00:00:00] Alex: Alright, let's get started. Thanks everyone for joining the weekly sync. 
First item on the agenda is the website redesign. Sarah, how are we doing on the homepage?
[00:00:15] Sarah: It's mostly done. I just need to fix the responsive layout for mobile. 
I should be finished by Thursday.
[00:00:25] Alex: Great. Make sure to check it on both iOS and Android. 
Next up, the backend migration. Mike?
[00:00:35] Mike: We hit a bit of a snag with the database schema. The old data structure isn't mapping cleanly. 
We decided to write a custom migration script to handle the edge cases.
[00:00:45] Alex: Okay, does that impact the timeline?
[00:00:50] Mike: Yeah, it pushes us back about two days. So we're looking at launch next Monday instead of Friday.
[00:00:58] Alex: That's fine. Quality is more important than rushing. 
Let's officially move the launch date to next Monday, the 25th.
[00:01:10] Sarah: One more thing - we need to approve the budget for the new server instance. 
It's $50 a month.
[00:01:20] Alex: Approved. Go ahead and provision it. 
So action items: Sarah on mobile layout, Mike on migration script. 
I'll update the project board.
[00:01:35] Mike: Sounds good.
[00:01:37] Alex: Thanks everyone, meeting adjourned.
"""

def create_sample():
    print("--- Creating Sample Meeting Minutes ---")
    print("Using dummy transcript...")
    
    try:
        # Initialize generator (picks up API key from .env)
        # Using gemini-flash-latest
        generator = MinutesGenerator(model="gemini-flash-latest")
        minutes = generator.generate_minutes(SAMPLE_TRANSCRIPT)
        
        filename = "sample_minutes.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(minutes)
            
        print(f"\nSuccess! Sample minutes saved to: {filename}")
        print("\n--- Preview ---")
        print(minutes)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_sample()
