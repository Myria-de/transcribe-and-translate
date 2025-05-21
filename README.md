# Audio-Dateien transkribieren (Speech-to-Text) und übersetzen

## Audacity 3.x und OpenVINO unter Linux (Ubuntu/Linux Mint)
Erstellen Sie Audacity 3.x (https://github.com/audacity/audacity) mit dem OpenVINO-Plugin (https://github.com/intel/openvino-plugins-ai-audacity) unter Ubuntu/Linux Mint. Dafür verwenden Sie das Bash-Script "build_audacity.sh".

Laden Sie das ZIP-Paket über "Code -> Download ZIP" herunter und entpacken Sie Archiv in Ihr Home-Verzeichnis.

**Wichtig**: Passen Sie im Script hinter "VERSION" die Version des Betriebssystems an. Verwenden Sie "22" für Ubuntu 22.04 oder Linux Mint 21.x. Verwenden Sie "24" für Ubuntu 24.04 oder Linux Mint 22.x.

Das Script lädt die KI-Modelle herunter und speichert Sie in Ihrem Home-Verzeichnis im Ordner "Audacity.bin/lib/openvino-models". Wenn Sie Audacity über das Script neu installieren oder aktualisieren, setzen Sie ein Kommentarzeichen ("#") vor die Zeile "models_install" im unteren Bereich des Scripts. Dann werden die umfangreichen Modelle nicht erneut installiert.

Starten Sie das Script im Download-Verzeichnis mit

```
sh ./build_audacity.sh
```
Das Script verwendet weitestgehend die Anleitung, die unter https://github.com/intel/openvino-plugins-ai-audacity/blob/main/doc/build_doc/linux/README.md zu finden ist.

Hinter "AUDACITY_VERSION" passen Sie bei Bedarf die Audacity-Version an. Getestet habe ich das Script mit Audacity 3.6.4.

All Download URLs im Script sind Stand September 2024. Wenn neuere Versionen verfügbar sind, müssen Sie die Download-Adressen wahrscheinlich anpassen.

Die Installation ist standardmäßig halbwegs portabel. Audacity lässt sich im Home-Verzeichnis aus dem Ordner "Audacity.bin/bin" über das Script "start_audacity.sh" starten. Ein Programmstarter für den Desktop erstellt das Script unter ".local/share/applications/audacity.desktop". Die AI-Modelle werden in den Ordner "Audacity.bin/lib/openvino-models" entpackt.

Nach dem ersten Start von Audacity gehen Sie auf "Bearbeiten -> Einstellungen -> Module". Hinter "mod-openvino" stellen Sie "Aktiviert" ein. Danach starten Sie Audacity neu. 

Zu den Funktionen des OpenVINO-Plugins siehe https://www.audacityteam.org/blog/openvino-ai-effects.

Für die Transkription einer in Audacity geöffneten Audio-Datei markieren Sie die Spur (Strg-A) und gehen auf "Analyse -> OpenVION Whisper Transcription..". Wählen Sie das gewünschte Whisper-Modell und klicken Sie auf "Anwenden". Die Transkription landet in einer Label-Spur. Klicken Sie diese an und gehen Sie auf "Datei -> Andere exportieren -> Textmarken exportieren", um die Transkription in einer Textdatei zu speichern.

**Hinweis**: OpenVINO-Whisper kann zahlreiche Sprachen aus den Audio-Dateien verarbeiten. Die Transkription erfolgt in die jeweilige Sprache der Audiodatei. Im OpenVINO-Plugin kann man auch "translate" einstellen. Der Text wird dann in die englische Sprache übersetzt. Eine Auswahl der Zielsprache ist nicht vorgesehen. Die Sprache der Audio-Datei lässt sich hinter "Source Language" festlegen. Mit "auto" erfolgt die Erkennung automatisch, was bei unseren Tests problemlos funktionierte.

![Audacity_OpenVINO](https://github.com/user-attachments/assets/8b77a212-61f7-491b-bd1c-67aca2ce1da5)
**Zusätzliches Script**: Mit deep-translator (siehe nächster Abschnitt) lässt sich der in Audacity transkribierte Text übersetzen. Die Audacity-Dateien enthalten allerdings Timecodes vpr den einzelnen Sätzen, die die Übersetzung stören können. Das Script "translate_audacity_files.py" entfernt die Timecodes und übersetzt die Dateien. Kommentare im Script erläutern die Konfiguration.
![Audacity_Transcoding](https://github.com/user-attachments/assets/e562d1e6-433d-4d8d-a1fe-709db8abca2c)

## Transkribieren und übersetzen mit Whisper und deep-translator
Wer mehrere Audio-Dateien automatisch transkribieren und übersetzen möchte, verwendet dafür OpenAI-Whisper (https://github.com/openai/whisper) und deep-translator (https://github.com/nidhaloff/deep-translator).

Das **Komplettpaket** für Linux und Windows inklusive vorkompilierter Python-Binärdateien  können Sie über https://tinyurl.com/STTPYS herunterladen.

Die Installation in einer virtuellen Python-Umgebung erfolgt mit dem Script "install-deep-translator.sh". Das Script richtet die nötigen Pakete ein. In der Python-Umgebung erledigt das Script "transcribe_translate.py" die Aufgabe. Öffnen Sie es zuerst in einem Editor und passen Sie die Konfiguration an. Kommentare im Script erläutern die Konfiguration.

Die Variable "Source_Path" legt den Ordner fest, in dem die Audio-Dateien liegen, deren Inhalt Sie in eine schriftliche Form bringen möchten. "Target_Path" gibt den Zielordner für die resultierenden Textdateien an. Weitere Variablen bestimmen die Zielsprache und das Ausagabeformat (in der Regel "txt"). Hinter "WhisperModel" legen Sie das gewünschte OpenAI-Whisper-Model fest. Größere Modelle liefern meist bessere Ergebnisse, erfoldern aber mehr RAM, Platz auf der Festplatte und sind langsamer. Die Voreinstellung "medium" sollte in den meisten Fällen ausreichen.

Für die Übersetzung ist GoogleTranslator vorkonfiguriert. Sie können auch ChatGptTranslator verwenden, was aber einen kostenpflichtigen API-Key erfordert. Zu den Einzelheiten und weiteren Online-Übersetzern siehe https://github.com/nidhaloff/deep-translator.

Starten Sie das Script im Installationsorder ("deep-translator/bin") mit
```
./transcribe_translate.py
```
Beim ersten Start lädt Whisper das konfigurerte Modell herunter. Danach transkribiert das Script die Audio-Dateien aus dem Quellordner und speichert die übersetzten Dateien im Zielordner.





