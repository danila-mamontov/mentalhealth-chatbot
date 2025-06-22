# Bot Logic

## 1. Commands
- `/start` - Start the bot
- `/help` - Show help information
- `/survey` - Start a survey
- `/record` - Record a voice message
- `/cancel` - Cancel current action

## TeleBot State Management
The bot now uses TeleBot's built-in finite state machine to track the
conversation flow. States are defined in `states.py` and registered via
`StateMemoryStorage` in `bot.py`. Handlers check the current state to decide
what step to execute next.
For each survey, a single state (`SurveyStates.phq9` or `SurveyStates.wbmms`) is
used. The current question index is stored in memory so handlers simply
increment the index after every answer and send the next question.

## 2. User Flow
### **New User**
1. User sends `/start`
2. Bot replies with a wellcome message: **"Welcome! Do you want to participate in a survey?"** (Yes/No)
3. If **Yes** → Move forward
4. If **No** → Bot ends conversation

### **Returning User**
1. User sends `/start`
2. Bot replies: **"Welcome back! What do you want to do?"**
   - "Take a survey" → Start survey
   - "Exit" → End session

### 3. General Flow
1. User sends \start command
2. Bot sends welcome message
3. Profil creation
   - Bot asks for a consent to participate in a survey (Yes/No)
   - Bot asks for a gender (Male/Female/No answer)
   - Bot ask for an age (from 18 to 99)

4. Main menu with options:
   - Start a survey
   - Open our website with more information

## 3. Survey Flow
1. User selects "Take a survey"
2. Bot asks first question
3. User responds → Move to next question
4. If all questions answered → Show results and save to file
5. Return to Main Menu

## 4. Voice Recording Flow
1. User selects "Record a voice message"
2. Bot prompts: **"Please send a voice message."**
3. User sends audio
   - If length **< 5 sec** → **"Message too short, try again."**
   - If valid → Save file and return to menu

## 5. Available Menus Details
1. Main Menu
   - Start a survey
   - Open Profile
   - Open our website with more information
   - Create a new profile
   - Share your feedback
   - Share our


## 5. Error Handling
- **Unknown Command:** "Sorry, I don't understand that command."
- **Survey Interruption:** "You exited the survey. Type `/survey` to restart."
- **Short Audio:** "Your voice message is too short. Please try again."

## 6. File Structure
```
project_root/
│── bot.py
│── handlers/
│── utils/
│── responses/
│   ├── <user_id>/
│   │   ├── logs.log
│   │   ├── survey_results.csv
│   │   ├── voice_messages/
│── bot_logic.md  # This file
```

