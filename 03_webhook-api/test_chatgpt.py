from openai import ChatCompletion

def summarize_with_chatgpt(input_text: str) -> str:
    task_description = 'Fass folgenden Text zusammen'
    prompt = f'{task_description}:\n{input_text}'
    messages = [{ 'role': 'user', 'content': prompt }]
    response = ChatCompletion.create(
        model='gpt-4',
        messages=messages,
        temperature=0
    )

    return response.choices[0].message['content']

text_to_summarize = '''
Hallo lieber Kunden-Support,
ich wollte er mal nachfragen ob das normal ist, dass ich keine Bestätigung per E-Mail bekommen habe (OrderID: e3b1a770-2a34-4086-91f9-32aa60ba93e4). Dazu bitte ich sie für mich nochmals zu überprüfen ob die angegebene E-Mail, foo.bar@example.de lautet und ob die Lieferadresse hiermit übereinstimmt:
Hauptstraße 2 Teststadt 451123.
Vielen Dank
Mfg Max Mustermann
'''

summarization = summarize_with_chatgpt(text_to_summarize)