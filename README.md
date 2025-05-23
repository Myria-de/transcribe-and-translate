# Audio-Dateien transkribieren (Speech-to-Text) und übersetzen
**Inhalt:**

1. [Audacity 3.x und OpenVINO unter Linux (Ubuntu/Linux Mint)](#audacity-3x-und-openvino-unter-linux-ubuntulinux-mint)
2. [Transkribieren und übersetzen mit Whisper und deep-translator (Python-Script)](#transkribieren-und-%C3%BCbersetzen-mit-whisper-und-deep-translator)

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

**Komplettpaket verwenden**
Das Komplettpaket für Linux und Windows inklusive vorkompilierter Python-Binärdateien können Sie über https://tinyurl.com/STTPYS herunterladen. Die Datei ist mit gut 6 GB recht groß, weil zahlreiche Programmbibliotheken enthalten sind. Wenn Sie diesen Download verwenden, müssen Sie die Python-Umgebung nicht selbst erzeugen, wie nachfolgend beschrieben.

Im Ordner "install_python_trans/GUI/Tools/linux" beziehungsweise "install_python_trans/GUI/Tools/windows" liegt das Programm transcribe_and_translate_cli(.exe). Es handelt sich um ein Kommandozeilen-Tool, mit dem sich Audio- und Videodateien transkribieren und übersetzen lassen. Sie können es für die Automatisierung der Prozesse verwenden oder Sie nutzen die grafische Oberfläche aus dem Ordner "install_python_trans/GUI (transcribe_translate, transcribe_translate.exe).

Ein Beispielaufruf sieht so aus:
```
transcribe_translate "file.mp4" -o "Transcribed" --source_lang en --target_lang de --translator "Argos" -f srt
```
Der Start mit 
```
transcribe_translate --help
```
liefert eine Liste der Optionen mit Erklärung.

Die grafische Oberfläche sollte selbsterklärend sein. Sie erwartet die Binärdateien im Unterverzeichnis "Tools/Linux" beziehungsweise "Tools/Windows". Alternativ geben Sie unter "Python-Client-Tool" die selbst kompiliert Datei "python-trans/bin/transcribe_translate_cli" an. Diese startet schneller, arbeitet ansonsten aber genauso schnell wie das kompilierte Komplettpaket.

**Python-Scripts selbst erstellen**

Die Installation in einer virtuellen Python-Umgebung erfolgt mit dem Script "install-python-scripts.sh". Das Script richtet die nötigen Pakete ein.
Sie können dann entweder
 - transcribe_translate_cli nutzen und über Optionen steuern
oder
- transcribe_translate verwenden, das die Optionen aus der Datei " transcribe_translate_config.ini" erhält. Öffnen Sie die INI-Datei in einem Editor und passen Sie die Konfiguration an. Die Kommentare erläutern die Konfiguration.

"Source_Path" legt den Ordner fest, in dem die Audio-/Videodateien liegen, deren Inhalt Sie in eine schriftliche Form bringen möchten. "Target_Path" gibt den Zielordner für die resultierenden Textdateien an. Diese Pfadangaben erfolgen mit vorangestelltem "/", das Script ergänzt später den Pfad zum Home-Verzeichnis, sodass sich beispielsweise "/home/user/python-trans/bin/Subtitle-Demo/ToTranscribe" ergibt. Aus "Source_Path" werden alle darin befindlichen Dateien verarbeitet. Stellen Sie daher sicher, dass sich im Ordner nur geeignete Dateien befinden (MP4, MP3, etc.).

Alternativ verwenden Sie die Variablen "ABS_Source_Path" und "ABS_Target_Path", die Vorrang haben. Tragen Sie den gewünschten absoluten Pfad ein, beispielsweise "/media/user/Laufwerk/ToTranscribe".
Weitere Variablen bestimmen die Zielsprache und das Ausgabeformat, etwa "txt" für ein Manuskript oder "srt" für eine Untertiteldatei. Hinter "WhisperModel" legen Sie das gewünschte OpenAI-Whisper-Model fest. Größere Modelle liefern meist bessere Ergebnisse, erfordern aber mehr (V)RAM sowie Platz auf der Festplatte und sind langsamer. Die Voreinstellung "medium" sollte in den meisten Fällen geeignet sein. Bei der ersten Nutzung laden die Python-Scripte das konfigurierte Whisper-Modell herunter.

Hinter "UseTranslator" geben Sie den gewünschten Übersetzer an. "Argos" arbeitet lokal und ohne Cloud-Dienst, liefert aber nicht immer zufriedenstellende Ergebnisse. Als bessere Alternative bietet sich "GoogleTranslator" an. Sie können auch ChatGptTranslator verwenden, was aber einen kostenpflichtigen API-Key erfordert. Zu den Einzelheiten und weiteren Online-Übersetzern siehe https://github.com/nidhaloff/deep-translator.

**Weitere Ordner und Dateien:**
Der Ordner "build_python_bin" enthält ein Script, mit dem Sie die Python-Binärdateien erstellen können. Das Script verwendet Pyinstaller.
Der Ordner "scripts" enthält den Quellcode der Python-Dateien. Das Bash-Script "build.sh" erzeugt eine Python-Wheel-Datei für die Installation. Dafür muss das Python-Tool Poetry installiert sein.
Im Ordner "Subtitle-Demo" finden Sie das Script "demo.sh". Es transkribiert die englischsprachige Videodatei aus dem Ordner "ToTranscribe", das Ergebnis inklusive deutscher Übersetzung wird im Ordner "Transcribed" gespeichert.







