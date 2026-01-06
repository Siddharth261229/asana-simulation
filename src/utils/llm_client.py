import random

class MockLLM:
    """
    Simulates an LLM to ensure the code is runnable without an API key.
    In production, replace this with OpenAI/Anthropic client.
    """
    
    def generate_task_name(self, project_type):
        patterns = {
            "Engineering": [
                "Refactor {} module", "Fix bug in {}", "Update API documentation for {}", 
                "Optimize database queries for {}", "Implement {} unit tests"
            ],
            "Marketing": [
                "Draft copy for {}", "Design assets for {}", "Schedule social posts for {}", 
                "Review analytics for {}", "Sync with partners regarding {}"
            ]
        }
        
        subjects = {
            "Engineering": ["Auth", "Payments", "Dashboard", "Search", "Notifications"],
            "Marketing": ["Q3 Campaign", "Webinar", "Newsletter", "Product Launch", "Case Study"]
        }
        
        ptype = "Engineering" if "Eng" in project_type else "Marketing"
        pattern = random.choice(patterns.get(ptype, patterns["Engineering"]))
        subject = random.choice(subjects.get(ptype, subjects["Engineering"]))
        
        return pattern.format(subject)

    def generate_description(self):
        descriptions = [
            "",  # Empty description
            "Please handle this by EOD.",
            "Refer to the spec doc linked in the channel.\n\nKey requirements:\n- Performance < 200ms\n- Mobile responsive",
            "Customer reported this issue on ticket #4421. Seems urgent."
        ]
        return random.choices(descriptions, weights=[20, 30, 40, 10])[0]

# Singleton instance
llm = MockLLM()