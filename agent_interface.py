#!/usr/bin/env python3
"""
Simple interface to test the research paper agent
This can be used to verify the agent is working before using it in ADK dev UI
"""

from agent import process_user_query, research_agent
import os

def main():
    """Simple command-line interface for testing the agent"""
    print("Research Paper Agent - Test Interface")
    print("=" * 40)
    print("Type 'help' for instructions, 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process the user input
            response = process_user_query(user_input)
            print(f"\nAgent: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
