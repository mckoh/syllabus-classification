prompt = """Kannst du die Lehrveranstaltung mit dem Titel **name** auf auf Basis
des DigiComp 2.2 Rahmens einstufen. Du findest diesen Rahmen hier:
https://raw.githubusercontent.com/mckoh/digicomp2-2/refs/heads/main/competences.json.
Kannst du eine Einschätzung vornehmen, welches Kompetenzniveau die Lehrveranstaltung
in den einzelnen Dimensionen des Rahmens unter der Annahme erreicht, dass die einzelnen
Kompetenzstufen aufeinander aufbauen und die unteren Stufen ein Erfüllungskriterium
für das Erreichen der oberen Stufen ist. Nimm bei der Einstufung die Perspektive
eines **role** ein. Diese Rolle zeichnet sich durch folgende Eigenschaften aus:
**description**. Kannst du deine Einstufung als Tabelle
vornehmen mit folgenden Spalten: Kompetenzbereich (inklusive Kompetenz ID),
Dimension, Einstufung, und Begründung. Hier ist der Kompetenzerwerb der
Lehrveranstaltung: **objectives**"""