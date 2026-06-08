import re
from typing import Dict

class SecurityChecker:
    """Check for potential security issues in prompts"""
    
    INJECTION_PATTERNS = [
        r"ignore\s+(previous|above|all)\s+instructions",
        r"disregard\s+(previous|above|all)",
        r"forget\s+(previous|above|all)",
        r"system\s*:\s*you\s+are",
        r"<\s*script\s*>",
        r"<\s*iframe\s*>",
        r"javascript\s*:",
        r"eval\s*\(",
        r"exec\s*\(",
    ]
    
    def check_prompt(self, prompt: str) -> Dict:
        """Check prompt for security issues"""
        issues = []
        risk_level = "low"
        
        prompt_lower = prompt.lower()
        
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, prompt_lower, re.IGNORECASE):
                issues.append(f"Potential prompt injection detected: {pattern}")
                risk_level = "high"
        
        # Check for excessive length
        if len(prompt) > 10000:
            issues.append("Prompt exceeds recommended length")
            risk_level = "medium" if risk_level == "low" else risk_level
        
        # Check for SQL-like commands (if using in RAG context)
        sql_patterns = [r"drop\s+table", r"delete\s+from", r"truncate"]
        for pattern in sql_patterns:
            if re.search(pattern, prompt_lower):
                issues.append(f"Suspicious SQL-like command detected: {pattern}")
                risk_level = "high"
        
        return {
            "is_safe": len(issues) == 0,
            "risk_level": risk_level,
            "issues": issues
        }
    
    def sanitize_input(self, text: str) -> str:
        """Basic input sanitization"""
        # Remove potential HTML/JS tags
        text = re.sub(r"<[^>]+>", "", text)
        # Remove null bytes
        text = text.replace("\x00", "")
        return text.strip()

security_checker = SecurityChecker()
