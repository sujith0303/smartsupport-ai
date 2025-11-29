from gpt4all import GPT4All
import json
from datetime import datetime
import os

# STEP 1: Load GPT4All model
gpt_model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

# STEP 2: IMPROVED Scenarios
scenarios = {
    "product_inquiry": {
        "name": "Product Inquiry",
        "system_prompt": """You are a helpful customer service representative for TechStore, 
an electronics e-commerce company. Answer product questions clearly and enthusiastically.
Keep responses under 100 words. Be friendly and professional. Write ONLY the bot's response, 
nothing else."""
    },
    
    "order_status": {
        "name": "Order Status Check",
        "system_prompt": """You are a customer service agent helping with order tracking.
Acknowledge the order number, provide a realistic status update. Be empathetic and reassuring.
Keep response under 80 words. Write ONLY the bot's single response. Do NOT write a 
conversation with Customer: and Bot: labels. Just give ONE complete answer."""
    },
    
    "return_request": {
        "name": "Return Request",
        "system_prompt": """You are a customer service agent handling returns.
Be understanding and helpful. Explain: 1) Return eligibility (within 30 days) 
2) Return shipping label process 3) Refund timeline (5-7 business days).
Keep under 100 words. Write ONLY ONE complete response. Do NOT cut off mid-sentence."""
    },
    
    "refund_status": {
        "name": "Refund Status",
        "system_prompt": """You are a customer service agent helping with refund inquiries.
Explain refund processing takes 5-7 business days after item is received. 
Offer to check specific status if they provide order number.
Keep under 60 words. Write ONE complete response only."""
    },
    
    "technical_support": {
        "name": "Technical Support",
        "system_prompt": """You are a technical support specialist. Provide 3-4 clear 
troubleshooting steps numbered 1, 2, 3. Be patient but concise. End by offering 
escalation if needed. Keep under 100 words. Write ONE complete response that doesn't 
cut off mid-sentence."""
    },
    
    "shipping_info": {
        "name": "Shipping Information",
        "system_prompt": """You are a customer service agent providing shipping information.
Standard: 5-7 days (free over $50), Express: 2-3 days ($15), Overnight: next day ($25).
Be clear and helpful. Keep under 80 words. Write ONE complete response only."""
    },
    
    "product_recommendation": {
        "name": "Product Recommendation",
        "system_prompt": """You are a sales associate. Based on customer needs and budget, 
recommend 2-3 specific products with brief explanations. Be helpful not pushy. 
Keep under 100 words. Write ONE complete response with actual recommendations."""
    },
    
    "complaint": {
        "name": "Complaint Handling",
        "system_prompt": """You are a customer service manager. Show empathy first. Apologize 
sincerely. Offer 3 solution options: 1) Replacement 2) Full refund 3) Store credit + 20% 
discount. Keep under 100 words. Write ONLY the bot's response naturally. Do NOT include 
stage directions like (Note:) or (pause)."""
    },
    
    "account_issue": {
        "name": "Account Issue",
        "system_prompt": """You are a customer service agent. Provide 3-4 troubleshooting steps: 
1) Check email/spam for verification 2) Clear browser cache 3) Try different browser 
4) We can escalate if needed. Keep under 100 words. Write ONE complete helpful response."""
    },
    
    "general_faq": {
        "name": "General FAQ",
        "system_prompt": """You are a customer service agent. Provide clear information about: 
Return policy (30 days with receipt), Warranty (1 year), Shipping (Free over $50), 
Payment (All major cards). Keep under 50 words. Answer ONLY what was asked. Write ONE 
complete response. Do NOT add extra Customer:/Bot: dialogue."""
    }
}

# Test cases
test_cases = {
    "product_inquiry": "Tell me about your wireless headphones. Do they have noise cancellation?",
    "order_status": "Hi, I'd like to check the status of my order #12345. When will it arrive?",
    "return_request": "I bought a laptop last week but it's not what I expected. Can I return it?",
    "refund_status": "I returned my order 5 days ago. When will I receive my refund?",
    "technical_support": "My new smartphone isn't charging properly. What should I do?",
    "shipping_info": "How long does shipping usually take? Do you have faster options?",
    "product_recommendation": "I'm a college student looking for a laptop for programming. Budget is around $800.",
    "complaint": "I'm very upset! My tablet arrived with a cracked screen. This is unacceptable!",
    "account_issue": "I can't log into my account. I've tried resetting my password but nothing works.",
    "general_faq": "What is your return policy? How long do I have to return items?"
}

def get_chatbot_response(scenario_type, customer_message):
    """Get response from chatbot"""
    scenario = scenarios.get(scenario_type)
    if not scenario:
        return "Error: Invalid scenario type"
    
    prompt = f"{scenario['system_prompt']}\n\nCustomer: {customer_message}\n\nBot:"
    try:
        response = gpt_model.generate(prompt, max_tokens=150)
        # Clean up the response
        response = response.strip()
        # Remove any "Customer:" or "Bot:" labels if they appear
        if "Customer:" in response:
            response = response.split("Customer:")[0].strip()
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def generate_all_responses():
    """Generate responses for all test cases"""
    print("🤖 GENERATING CHATBOT RESPONSES...")
    print("="*60 + "\n")
    
    results = {}
    for scenario_type, question in test_cases.items():
        print(f"Scenario: {scenarios[scenario_type]['name']}")
        print(f"Customer: {question}")
        print(f"Generating response...\n")
        
        response = get_chatbot_response(scenario_type, question)
        
        print(f"Bot Response:")
        print(f"   {response}")
        print("\n" + "-"*60 + "\n")
        
        results[scenario_type] = {
            "question": question,
            "response": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    with open('chatbot_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("All responses generated and saved\n")
    return results

def evaluate_response_manual(scenario_type, customer_message, bot_response):
    """Manual quality evaluation based on clear criteria"""
    
    score = 0
    feedback = []
    
    # Check 1: Response length (should be substantial but not too long)
    length = len(bot_response)
    if 50 <= length <= 600:
        score += 2
        feedback.append("✓ Good length")
    elif length < 50:
        score += 0
        feedback.append("✗ Too short")
    else:
        score += 1
        feedback.append("~ Slightly long")
    
    # Check 2: Has professional greeting/acknowledgment
    greetings = ['hi', 'hello', 'thank', 'sorry', 'appreciate']
    if any(g in bot_response.lower()[:50] for g in greetings):
        score += 1.5
        feedback.append("✓ Professional tone")
    
    # Check 3: Provides specific information
    if any(char.isdigit() for char in bot_response) or 'days' in bot_response.lower():
        score += 1.5
        feedback.append("✓ Specific details")
    
    # Check 4: Complete response (doesn't cut off)
    if bot_response.endswith(('.', '!', '?')) and not bot_response.endswith('...'):
        score += 2
        feedback.append("✓ Complete")
    else:
        score += 0
        feedback.append("✗ Incomplete/cut-off")
    
    # Check 5: No errors or weird formatting
    issues = ['error', 'customer:', 'bot:', '(note:', '(pause']
    has_issues = any(issue in bot_response.lower() for issue in issues)
    if not has_issues:
        score += 2
        feedback.append("✓ Clean format")
    else:
        score += 0
        feedback.append("✗ Formatting issues")
    
    # Check 6: Helpful content
    helpful_keywords = ['will', 'can', 'help', 'steps', 'process', 'option', 'solution']
    if any(kw in bot_response.lower() for kw in helpful_keywords):
        score += 1
        feedback.append("✓ Helpful content")
    
    return {
        "overall_score": score,
        "max_score": 10,
        "percentage": (score / 10) * 100,
        "feedback": " | ".join(feedback),
        "length": length
    }

def evaluate_all_responses(results):
    """Evaluate all responses"""
    print("\n🔍 EVALUATING RESPONSE QUALITY...")
    print("="*60 + "\n")
    
    evaluations = {}
    
    for scenario_type, data in results.items():
        evaluation = evaluate_response_manual(
            scenario_type,
            data['question'],
            data['response']
        )
        
        evaluations[scenario_type] = {
            "scenario": scenarios[scenario_type]['name'],
            "question": data['question'],
            "response": data['response'],
            "evaluation": evaluation,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"📊 {scenarios[scenario_type]['name']}")
        print(f"   Score: {evaluation['overall_score']:.1f}/10 ({evaluation['percentage']:.0f}%)")
        print(f"   {evaluation['feedback']}")
        print()
    
    with open('chatbot_evaluations.json', 'w') as f:
        json.dump(evaluations, f, indent=2)
    
    print("All evaluations complete\n")
    return evaluations

def generate_summary_report(evaluations):
    """Generate summary report"""
    print("="*60)
    print("QUALITY EVALUATION SUMMARY")
    print("="*60 + "\n")
    
    scores = [data['evaluation']['overall_score'] for data in evaluations.values()]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    high_performing = [(scenarios[k]['name'], v['evaluation']['overall_score']) 
                       for k, v in evaluations.items() 
                       if v['evaluation']['overall_score'] >= 8]
    
    needs_improvement = [(scenarios[k]['name'], v['evaluation']['overall_score']) 
                         for k, v in evaluations.items() 
                         if v['evaluation']['overall_score'] < 7]
    
    print(f" OVERALL STATISTICS:")
    print(f"   Average Quality Score: {avg_score:.1f}/10 ({(avg_score/10)*100:.0f}%)")
    print(f"   Total Scenarios: {len(scores)}\n")
    
    print(f" HIGH PERFORMING (8+): {len(high_performing)} scenarios")
    if high_performing:
        for name, score in sorted(high_performing, key=lambda x: x[1], reverse=True):
            print(f"   • {name}: {score:.1f}/10")
    else:
        print("   None yet")
    
    print(f"\n  NEEDS IMPROVEMENT (<7): {len(needs_improvement)} scenarios")
    if needs_improvement:
        for name, score in sorted(needs_improvement, key=lambda x: x[1]):
            print(f"   • {name}: {score:.1f}/10")
    else:
        print("   None - All scenarios performing well!")
    
    print("\n" + "="*60)
    
    return {
        "average_score": avg_score,
        "high_performing": high_performing,
        "needs_improvement": needs_improvement
    }

if __name__ == "__main__":
    print("\n SMARTSUPPORT AI - CHATBOT QUALITY ANALYSIS")
    print("="*60 + "\n")
    
    # Generate responses with full display
    results = generate_all_responses()
    
    # Evaluate all responses
    evaluations = evaluate_all_responses(results)
    
    # Generate summary
    summary = generate_summary_report(evaluations)
    
    print("\n ANALYSIS COMPLETE!")
    print("\nGenerated files:")
    print("  • chatbot_test_results.json")
    print("  • chatbot_evaluations.json")
    print(f"\n Final Average Score: {summary['average_score']:.1f}/10 ({(summary['average_score']/10)*100:.0f}%)")
    print("\n" + "="*60 + "\n")
