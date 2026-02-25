def start_gateway():
    print("Agent: Hello! How can I help you today?")
    
    while True:
        user_input = input("You: ")
        
        # Check for exit commands
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Agent: Goodbye!")
            break
            
        # This is where the "Brain" logic will eventually go
        response = "I heard you say: " + user_input 
        
        print(f"Agent: {response}")