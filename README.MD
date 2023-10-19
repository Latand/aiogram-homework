# FSM Form Guide for Branch `2-fsm`

Hello! In the `2-fsm` branch, you'll create a Telegram bot. This bot will ask users for some information step by step. After users provide all the details, the bot will show them everything they've entered in one message. We'll use pytest to check if your bot works correctly.

## Prerequisites

Before you begin, ensure that you have the necessary Python packages installed. Run the following command:

```bash
pip install -r requirements.txt
```

## Steps to Implement the Form Logic

1. **Initialize Router**: Set up a router in your bot with the name `form_router`.

2. **Begin Form Interaction**: 
    - When a user inputs the command `/form`, prompt them with a message asking for their name.

3. **Collect Name**: 
    - Capture the name input by the user. Once received, prompt the user to enter their email.

4. **Collect Email**: 
    - Capture the email input by the user. After obtaining the email, ask the user to provide their phone number.

5. **Collect Phone Number**: 
    - Capture the phone number input by the user.

6. **Display Collected Data**: 
    - Once all data is collected, send a message back to the user with the following exact format:
      ```
      Hello! You entered the following data:
      
      Name: [User's Name]
      Email: [User's Email]
      Phone: [User's Phone Number]
      ```
      Remember, the text should match the above format exactly. However, the data (inside the brackets) will vary based on user input.

7. **Clear Data**:
    - After displaying the data to the user, ensure that the bot clears this information from its memory.

## Running Tests

Once you've implemented the functionality, it's time to test it:

```bash
pytest .\tests\fsm.py --html=report.html
```

Upon successful completion of the tests, the results will be available in the `report.html` file and also displayed in the console.

> **Note**
> - It's essential that the text format remains consistent with the provided template. Only the user's entered data should vary.
> - The bot's responses and interactions should match the test cases provided in the `fsm.py` file. Ensure your code aligns with the expected outcomes of these tests.

Happy coding!
