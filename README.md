# ip5-nlp-ch
## 1	Einführung

### 1.1	Zusammenfassung
In dieser Arbeit werden Transkriptionen, die auf der Website www.dindialaekt.ch/ von Benut-zern erfasst wurden, mithilfe von NLP-Tools analysiert und verarbeitet. 

### 1.2	Projektkontext
Im Rahmen des vom Schweizerischen Nationalfods geförderten Agora-Project «Citizen Lingu-istics: Locate that dialect!» ist die Website www.dindialaekt.ch/ entstanden. 
Auf dieser Website können Benutzer unter Anderem folgenden Task erledigen:
*	Transkription schweizerdeutschen Audiofiles
*	Identifizieren von Dialekten mittels Lokalisierung auf einer Karte
*	Übersetzung von schweizerdeutschen zu hochdeutschen Texten
Im Rahmen dieser Arbeit wollen wir aus den so gewonnenen Transkriptionen weitere Informa-tionen gewinnen.
Zu jedem Audiofile gibt es mehrere (etwa 3 bis 7) zusammengehörende Transkriptionen.
Aus den so gewonnenen Transkriptionen sollen nun über Wortalignierung mögliche unter-schiedliche Schreibweisen für schweizerdeutsche Ausdrücke gefunden werden.
Die Aufgabe wird dadurch erschwert, dass viele Transkriptionen unvollständig (Mit Platzhal-tern in Form von *** oder ???) oder gar komplett falsch sind. 

### 1.3	Problemstellung
*	Unbrauchbare Transkriptionen ausfiltern
*	Gute Transkriptionen erkennen
*	*** Auslassungen interpolieren aus guten Transkriptionen
*	Schreibvarianten von Wörtern und Ausdrücken erkennen über String-Alignierung
Daraus ergeben sich uns folgende zwei Fragestellungen:

Welche Tools funktionieren mit unseren Daten?
Natural Language Processing (NLP) ist ein etabliertes Gebiet. Für viele Problemstellungen gibt es Tools und Algorithmen. Viele dieser Tools haben jedoch gewisse Voraussetzungen. Bei-spielsweise benötigen sie einen Textkorpus einer gewissen Grösse oder sie benötigen Wör-terbücher der zu untersuchenden Sprachen. Da es im Schweizerdeutschen keine genormte Rechtschreibung und daher auch keine Wörterbücher gibt, sind uns in der Wahl der Tools einige Grenzen gesetzt. Wir wollen also herausfinden, was für Tools grundsätzlich für unsere Art von Daten verwendbar sind.

Welche und wie viele Daten brauchen wir für gute Resultate?
Die Tools, die wir als «brauchbar» erkennen, werden jedoch auch Grenzen haben. Für die Betreiber der Website ist wichtig zu wissen, dass für eine Audiodatei ein Minimum and Tran-skriptionen vorhanden sein muss, um sinnvolle Analysen damit anzustellen. Konkret wollen wir also herausfinden, wie viele Transkriptionen zur selben Audiodatei vorhanden sein müssen, damit die von uns angewendeten Techniken funktionieren.

### 1.4	Vorgehen
Wir teilen den gesamten Prozess in mehrere Transformationen auf, die teilweise voneinander abhängig sind.


Sätze einer Satzgruppe können nach Qualität bewertet werden. Die macht es möglich, den besten und schlechtesten Satz zu identifizieren. Dieser Vorgang ist nötig, um für das Align-ment unbrauchbare Sätze auszufiltern.
Der Alignierungsprozess generiert aus einer Satzgruppe eine List von Wort/Ausdrucksgruppen, die bedeutungsgleich sind. Der Alignierungsprozess kann ausser-dem eine solche bestehende Liste von Wortgruppen mit den Wörtern einer weiteren Satz-gruppe erweitert werden.
Gefilterte Daten sind für den Alignierungsprozess streng genommen nicht zwingend. Da dies jedoch das Ergebnis verbessert, wird es empfohlen. Der Alignierungsprozess kann ausser-dem den Satzbewertungsprozess verwenden, um das Ergebnis zu verbessern.
Der Interpolationsprozess findet Auslassungen in Form von *** in einem Satz und ersetzt sie mithilfe der anderen Transkriptionen derselben Satzgruppe. Dieser Prozess basiert auf dem Alignierungsprozess. Auch hier empfiehlt es sich, mit gefilterten Satzgruppen zu agieren.

# Voraussetzungen
* Python 3
* PIP
* Bleualign.exe
* Hunalign.exe


Für Bleu- und Hunalign werden Windows Binaries mitgeliefert. Fur andere Platformen müssen diese erst kompiliert werden.
Bleu: https://github.com/emjotde/bleu-champ
Hun: https://github.com/danielvarga/hunalign
Zusätzlich müssen unter src/algorithms/align.py Zeilen 15 und 16 entsprechend angepasst werden.
