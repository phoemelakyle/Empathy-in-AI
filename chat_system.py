from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class ChatSystem:
    def __init__(self, temp_db):
        self.temp_db = temp_db
        self.google_ai_key = os.getenv("GOOGLE_AI_KEY")  # Get Google Gemini API key

        if not self.google_ai_key:
            print("⚠️ Warning: No Google AI key found. Make sure to set GOOGLE_AI_KEY in your .env file.")
        else:
            genai.configure(api_key=self.google_ai_key)
            print("✅ Google Gemini AI key loaded successfully.")

    def start_chat(self, user_id, user_role):
        """Start the chat system based on user role"""
        self.current_user_id = user_id  # Store current user ID
        if user_role == "patient":
            self._patient_chat_menu(user_id)
        elif user_role == "therapist":
            self._therapist_chat_menu(user_id)

    def _patient_chat_menu(self, user_id):
        """Display available therapists and start chat"""
        while True:
            print("\n=== Patient Chat Menu ===")
            print("1. Chat with AI")
            print("2. Chat with Therapist")
            print("3. View Chat History")
            print("4. Return to Main Menu")
            choice = input("Enter choice: ")

            if choice == "1":
                self._start_ai_chat()
            elif choice == "2":
                self._show_available_therapists(user_id)
            elif choice == "3":
                self._view_chat_history(user_id)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def _start_ai_chat(self):
        """Start a chat session with Google Gemini AI"""
        print("\n=== AI Chat Session (Powered by Google Gemini) ===")
        print("Type 'exit' to end chat")

        conversation_history = []

        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == 'exit':
                break
            elif user_input:
                conversation_history.append({"role": "user", "content": user_input})

                response = self._get_ai_response(conversation_history)
                print(f"\nAI: {response}")

                conversation_history.append({"role": "assistant", "content": response})

    def _get_ai_response(self, conversation_history):
        """Send conversation history to Google Gemini AI and return response"""
        if not self.google_ai_key:
            return "⚠️ AI response is disabled. Please set your Google AI API key."

        try:
            model = genai.GenerativeModel("gemini-2.0-flash")  # ✅ Updated to the correct model name
            response = model.generate_content([msg["content"] for msg in conversation_history])

            return response.text  # Gemini AI returns text directly
        except Exception as e:
            return f"⚠️ Error communicating with Google AI: {str(e)}"

    def _show_available_therapists(self, user_id):
        """Display and select available therapists"""
        therapists = self.temp_db.get_all_therapists()
        if not therapists:
            print("\nNo therapists available at the moment.")
            return

        print("\nAvailable Therapists:")
        for i, therapist in enumerate(therapists, 1):
            print(f"{i}. {therapist.username}")
            
        therapist_choice = input("\nSelect therapist (number) or 0 to cancel: ")
        if therapist_choice.isdigit():
            choice = int(therapist_choice)
            if 0 < choice <= len(therapists):
                selected_therapist = therapists[choice - 1]
                self._start_chat_session(user_id, selected_therapist.user_id)

    def _therapist_chat_menu(self, user_id):
        """Display active patient chats for therapist"""
        while True:
            print("\n=== Therapist Dashboard ===")
            print("1. View Active Chats")
            print("2. View Chat History")
            print("3. Return to Main Menu")
            choice = input("Enter choice: ")

            if choice == "1":
                self._show_active_chats(user_id)
            elif choice == "2":
                self._view_chat_history(user_id)
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def _show_active_chats(self, therapist_id):
        """Display and select active patient chats"""
        active_chats = self.temp_db.get_active_chats(therapist_id)
        if not active_chats:
            print("\nNo active chats at the moment.")
            return

        print("\nActive Patient Chats:")
        for i, patient in enumerate(active_chats, 1):
            print(f"{i}. {patient.username}")

        chat_choice = input("\nSelect chat (number) or 0 to cancel: ")
        if chat_choice.isdigit():
            choice = int(chat_choice)
            if 0 < choice <= len(active_chats):
                selected_patient = active_chats[choice - 1]
                self._start_chat_session(selected_patient.user_id, therapist_id)

    def _start_chat_session(self, patient_id, therapist_id):
        """Start a chat session between patient and therapist"""
        print("\n=== Chat Session Started ===")
        print("Type 'exit' to end chat")
        print("Type 'history' to view recent messages")
        
        # Get user info
        current_user = self.temp_db.users[self.current_user_id]
        other_user_id = therapist_id if self.current_user_id == patient_id else patient_id
        other_user = self.temp_db.users[other_user_id]
        
        # Show recent messages
        messages = self.temp_db.get_chat_history(patient_id, therapist_id, limit=5)
        if messages:
            print("\nRecent messages:")
            for msg in messages:
                sender = "You" if msg.sender_id == self.current_user_id else f"{other_user.username}" if other_user.user_role == "therapist" else other_user.username
                print(f"{sender}: {msg.message}")

        while True:
            message = input("\nYou: ").strip()
            if message.lower() == 'exit':
                break
            elif message.lower() == 'history':
                self._show_chat_history(patient_id, therapist_id, self.current_user_id)
            elif message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.temp_db.save_message(self.current_user_id, other_user_id, message, timestamp)
                print("Message sent!")

    def _show_chat_history(self, patient_id, therapist_id, current_user_id=None):
        """Show chat history between patient and therapist"""
        messages = self.temp_db.get_chat_history(patient_id, therapist_id)
        if not messages:
            print("\nNo messages in chat history.")
            return

        # Get user info
        patient = self.temp_db.users[patient_id]
        therapist = self.temp_db.users[therapist_id]

        print("\n=== Chat History ===")
        for msg in messages:
            if msg.sender_id == current_user_id:
                sender = "You"
            else:
                sender_user = self.temp_db.users[msg.sender_id]
                sender = f"{sender_user.username}" if sender_user.user_role == "therapist" else sender_user.username
            print(f"[{msg.timestamp}] {sender}: {msg.message}")

    def _view_chat_history(self, user_id):
        """View all chat history for a user"""
        messages = self.temp_db.messages
        if not messages:
            print("\nNo chat history found.")
            return

        print("\n=== Chat History ===")
        current_chat_partner = None
        
        # Group messages by conversation partner
        conversations = {}
        for msg in messages:
            if msg.sender_id == user_id:
                other_id = msg.receiver_id
            elif msg.receiver_id == user_id:
                other_id = msg.sender_id
            else:
                continue
                
            other_user = self.temp_db.users.get(other_id)
            if not other_user:
                continue
                
            partner_name = f"{other_user.username}" if other_user.user_role == "therapist" else other_user.username
            if partner_name not in conversations:
                conversations[partner_name] = []
            conversations[partner_name].append(msg)

        # Display conversations sorted by most recent message
        for partner_name, msgs in conversations.items():
            msgs.sort(key=lambda x: x.timestamp)
            print(f"\nConversation with {partner_name}:")
            for msg in msgs:
                sender = "You" if msg.sender_id == user_id else partner_name
                print(f"[{msg.timestamp}] {sender}: {msg.message}")
