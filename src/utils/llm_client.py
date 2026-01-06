import random

class MockLLM:
    """
    Simulates an LLM to ensure the code is runnable without an API key.
    Includes logic for Tasks, Descriptions, and rich conversational Comments.
    """
    
    def generate_task_name(self, project_type):
        patterns = {
            "Engineering": [
                "Refactor {} module", "Fix bug in {}", "Update API documentation for {}", 
                "Optimize database queries for {}", "Implement {} unit tests", "Investigate 500 errors in {}"
            ],
            "Marketing": [
                "Draft copy for {}", "Design assets for {}", "Schedule social posts for {}", 
                "Review analytics for {}", "Sync with partners regarding {}", "Finalize budget for {}"
            ],
            "Sales": [
                "Follow up with {}", "Prepare slide deck for {}", "Contract negotiation with {}", 
                "Update CRM record for {}", "Quarterly review with {}"
            ]
        }
        
        subjects = {
            "Engineering": ["Auth Service", "Payments API", "Dashboard", "Search Index", "Notifications", "User Profile"],
            "Marketing": ["Q3 Campaign", "Webinar Series", "Newsletter", "Product Launch", "Case Study", "Holiday Promo"],
            "Sales": ["Enterprise Client", "Q4 Leads", "Mid-market Pipeline", "Renewals", "Strategic Partners"]
        }
        
        # Fallback to Engineering if key not found
        ptype = next((k for k in patterns if k in project_type), "Engineering")
        
        pattern = random.choice(patterns.get(ptype, patterns["Engineering"]))
        subject = random.choice(subjects.get(ptype, subjects["Engineering"]))
        
        return pattern.format(subject)

    def generate_description(self):
        descriptions = [
            "",  # 20% Empty
            "Please handle this by EOD.",
            "As discussed in the standup, we need to address this priority item.",
            "Refer to the spec doc linked in the channel.\n\nKey requirements:\n- Performance < 200ms\n- Mobile responsive",
            "Customer reported this issue on ticket #4421. Seems urgent.",
            "## Acceptance Criteria\n- [ ] Unit tests pass\n- [ ] Documentation updated\n- [ ] Code reviewed",
            "Steps to reproduce:\n1. Login as admin\n2. Navigate to settings\n3. Click 'Delete'\n\nExpected: Confirmation modal\nActual: 404 Error"
        ]
        return random.choices(descriptions, weights=[20, 10, 15, 20, 10, 15, 10])[0]

    def generate_comment(self, project_type):
        """Generates realistic comments based on department context."""
        
        common_comments = [
            "Looking into this now.", 
            "Any updates on this?", 
            "Can we push the deadline to Friday?",
            "Thanks for the update.",
            "I'm blocked on this until the API is ready.",
            "CCing @manager for visibility."
        ]

        engineering_comments = [
            "PR is up for review: github.com/repo/pull/123",
            "Deployed to staging. Please verify.",
            "Found the root cause: memory leak in the worker node.",
            "CI failed on the integration tests, fixing it now.",
            "LGTM!",
            "Can you rebase onto main?",
            "This is blocked by the database migration."
        ]

        marketing_comments = [
            "Attached the updated assets. Let me know what you think.",
            "Copy approved by Legal.",
            "Client requested one small change to the banner color.",
            "Scheduled for Tuesday morning.",
            "Do we have the final budget approval?",
            "The engagement numbers look great on this!"
        ]

        # Determine context
        if "Engineering" in project_type or "Product" in project_type:
            pool = common_comments + engineering_comments
        elif "Marketing" in project_type or "Sales" in project_type:
            pool = common_comments + marketing_comments
        else:
            pool = common_comments

        return random.choice(pool)

# Singleton instance
llm = MockLLM()