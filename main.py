import genanki
import random
import things

from cached_property import cached_property
from genanki import Model
from genanki import Note
from genanki import Deck
from genanki import Package



model_id = random.randrange(1 << 30, 1 << 31)



CSS = """.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
.cloze {
 font-weight: bold;
 color: blue;
}
.nightMode .cloze {
 color: lightblue;
}
"""

MY_CLOZE_MODEL = genanki.Model(
  998877661,
  'My Cloze Model',
  fields=[
    {'name': 'Text'},
    {'name': 'Extra'},
  ],
  templates=[{
    'name': 'My Cloze Card',
    'qfmt': '{{cloze:Text}}',
    'afmt': '{{cloze:Text}}<br>{{Extra}}',
  },],
  css=CSS,
  model_type=Model.CLOZE)





# Function to allow for generation of notes with simplified cloze tag syntax.
def cloze_replace(string):
    string = string.replace("{{", "{{cloze:")
    i = 1
    while True:
        if "cloze:" in string:
            string = string.replace("cloze:", f"c{i}::", 1)
            i += 1
        else:
            break
    return string


autocomplete_clozes = True

notes_to_add = []
for task in things.tasks("Ay2EzZZfuNB5v9Vzg9ZuQd")["items"]: # the ID here will need to change after the project is re-created. Should eventually give a prompt for the user to give the name
    if "tags" in task.keys() :
        if "clozed" in task["tags"]:
            note_text = task["title"]
    else:
        note_text = cloze_replace(task["title"])
        
    note_extra = task["notes"]
    anki_note = genanki.Note(
        model=MY_CLOZE_MODEL,
        fields=[note_text, note_extra]
    )
    notes_to_add.append(anki_note)
    


anki_deck = genanki.Deck(model_id, "Staging")
anki_package = genanki.Package(anki_deck)


for note in notes_to_add:
    anki_deck.add_note(note)


# Save the deck to a file
anki_package.write_to_file("staging_deck.apkg")

print("Created deck with {} flashcards".format(len(anki_deck.notes)))
