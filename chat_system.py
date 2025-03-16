from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class ChatSystem:
    """Handles AI and therapist-patient chat sessions"""

    def __init__(self, temp_db):
        """Encapsulation: Stores database reference & API key privately"""
        self._temp_db = temp_db
        self._google_ai_key = os.getenv("GOOGLE_AI_KEY")  # Get Google Gemini AI key
        self.current_user_id = None  # Tracks active user

        if not self._google_ai_key:
            print("⚠️ Warning: No Google AI key found. Set GOOGLE_AI_KEY in your .env file.")
        else:
            genai.configure(api_key=self._google_ai_key)
            print("✅ Google Gemini AI key loaded successfully.")

    def start_chat(self, user_id, user_role):
        """Start the chat system based on user role"""
        self.current_user_id = user_id  # Track the logged-in user
        if user_role == "patient":
            self._patient_chat_menu(user_id)
        elif user_role == "therapist":
            self._therapist_chat_menu(user_id)

    # PATIENT CHAT

    def _patient_chat_menu(self, user_id):
        """Display patient chat options"""
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
                print("❌ Invalid choice. Please try again.")

    def _start_ai_chat(self):
        """Start AI chat session"""
        print("\n=== AI Chat Session (Google Gemini) ===")
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
        """Get AI response from Google Gemini"""
        if not self._google_ai_key:
            return "⚠️ AI response disabled. Set GOOGLE_AI_KEY in .env."

        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content([msg["content"] for msg in conversation_history])
            return response.text
        except Exception as e:
            return f"⚠️ Error communicating with Google AI: {str(e)}"

    def _show_available_therapists(self, user_id):
        """Show available therapists for chat"""
        therapists = self._temp_db.get_all_therapists()
        if not therapists:
            print("\n❌ No therapists available.")
            return

        print("\nAvailable Therapists:")
        for i, therapist in enumerate(therapists, 1):
            print(f"{i}. {therapist.username}")

        choice = input("\nSelect therapist (number) or 0 to cancel: ")
        if choice.isdigit():
            index = int(choice)
            if 0 < index <= len(therapists):
                self._start_chat_session(user_id, therapists[index - 1].user_id)

    #THERAPIST CHAT SYSTEM

    def _therapist_chat_menu(self, user_id):
        """Therapist dashboard for managing patient chats"""
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
                print("❌ Invalid choice. Try again.")

    def _show_active_chats(self, therapist_id):
        """Display active patient chats for a therapist"""
        active_chats = self._temp_db.get_active_chats(therapist_id)
        if not active_chats:
            print("\n❌ No active chats available.")
            return

        print("\nActive Patient Chats:")
        for i, patient in enumerate(active_chats, 1):
            print(f"{i}. {patient.username}")

        choice = input("\nSelect chat (number) or 0 to cancel: ")
        if choice.isdigit():
            index = int(choice)
            if 0 < index <= len(active_chats):
                self._start_chat_session(active_chats[index - 1].user_id, therapist_id)

    #CHAT SESSION HANDLING

    def _start_chat_session(self, user1_id, user2_id):
        """Handles direct chat sessions between two users"""
        print("\n=== Chat Session Started ===")
        print("Type 'exit' to end chat")
        print("Type 'history' to view recent messages")

        messages = self._temp_db.get_chat_history(user1_id, user2_id, limit=5)
        if messages:
            print("\nRecent messages:")
            for msg in messages:
                sender = "You" if msg.sender_id == self.current_user_id else f"{msg.sender_id}"
                print(f"{sender}: {msg.message}")

        while True:
            message = input("\nYou: ").strip()
            if message.lower() == 'exit':
                break
            elif message.lower() == 'history':
                self._show_chat_history(user1_id, user2_id)
            elif message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._temp_db.save_message(self.current_user_id, user2_id, message, timestamp)
                print("📩 Message sent!")

    def _show_chat_history(self, user1_id, user2_id):
        """Display full chat history between two users"""
        messages = self._temp_db.get_chat_history(user1_id, user2_id)
        if not messages:
            print("\n❌ No messages in chat history.")
            return

        print("\n=== Chat History ===")
        for msg in messages:
            sender = "You" if msg.sender_id == self.current_user_id else f"{msg.sender_id}"
            print(f"[{msg.timestamp}] {sender}: {msg.message}")

    def _view_chat_history(self, user_id):
        """View chat history for the logged-in user"""
        messages = self._temp_db.messages
        if not messages:
            print("\n❌ No chat history found.")
            return

        print("\n=== Chat History ===")
        for msg in messages:
            if msg.sender_id == user_id or msg.receiver_id == user_id:
                sender = "You" if msg.sender_id == user_id else f"{msg.receiver_id}"
                print(f"[{msg.timestamp}] {sender}: {msg.message}")
