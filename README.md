# Audio-Dateien transkribieren (Speech-to-Text) und übersetzen

## Audacity 3.x und OpenVINO unter Linux (Ubuntu/Linux Mint)
Erstellen Sie Audacity 3.x (https://github.com/audacity/audacity) mit dem OpenVINO-Plugin (https://github.com/intel/openvino-plugins-ai-audacity).

Dafür verwenden Sie das Bash-Script "build_audacity.sh", das Sie in Ihr Home-Verzeichnis kopieren und starten:

```
sh ./build_audacity.sh
```

Passen Sie im Script hinter "VERSION" die Version des Betriebssystems an. Verwenden Sie "22" für Ubuntu 22.04 oder Linux Mint 21.x. Verwenden Sie "24" für Ubuntu 24.04 oder Linux Mint 22.x.

Hinter "AUDACITY_VERSION" passen Sie bei Bedarf die Audacity-Version an. Getestet habe ich das Script mit Audacity 3.6.4.

All Download URLs im Script sind Stand September 2024. Wenn neuere Versionen verfügbar sind, müssen Sie die Download-Adressen wahrscheinlich anpassen.

Die Installation ist standardmäßig halbwegs portabel. Audacity lässt sich aus dem Ordner "audacity/audacity-build/Release/bin" über das Script "start_audacity.sh" starten. Ein Programmstarter für den Desktop erstellt das Script unter ".local/share/applications/audacity.desktop"

Die AI-Modelle müssen im Ordner "/usr/local/lib/openvino-models" liegen. Für den Kopiervorgang werden root-Rechte angefordert.

Nach dem ersten Start von Audacity gehen Sie auf "Bearbeiten -> Einstellungen -> Module". Hinter "mod-openvino" stellen Sie "Aktiviert" ein. Danach starten Sie Audacity neu. 

Zu den Funktionen des OpenVINO-Plugins siehe https://www.audacityteam.org/blog/openvino-ai-effects.

![Audacity_OpenVINO](https://github.com/user-attachments/assets/8b77a212-61f7-491b-bd1c-67aca2ce1da5)

## Transkribieren und übersetzen mit Whisper und deep-translator
Wer Audio-Dateien automatisch transkribieren und übersetzen möchte, verwendet dafür OpenAI-Whisper (https://github.com/openai/whisper) und deep-translator (https://github.com/nidhaloff/deep-translator).

Die Installation in einer virtuellen Python-Umgebung erfolgt mit dem Script "install-deep-translator.sh". Das Script richtet die nötigen Pakete ein. In der Python-Umgebung erledigt das Script "transcribe_translate.py" die Aufgabe. Öffnen Sie es zuerst in einem Editor und passen Sie die Konfiguration an.

Die Variable "Source_Path" legt den Ordner fest, in dem die Audio-Dateien liegen, deren Inhalt Sie in eine schriftliche Form bringen möchten. "Target_Path" gibt den Zielordner für die resultierenden Textdateien an. Weitere Variablen bestimmen die Zielsprache und das Ausagabeformat (in der Regel "txt"). Hinter "WhisperModel" legen Sie das gewünschte OpenAI-Whisper-Model fest. Größere Modelle liefern meist bessere Ergebnisse, erfoldern aber mehr RAM, Platz auf der Festplatte und sind langsamer. Die Voreinstellung "medium" sollte in den meisten Fällen ausreichen.

Für die Übersetzung ist GoogleTranslator vorkonfiguriert. Sie können auch ChatGptTranslator verwenden, was aber einen kostenpflichtigen API-Key erfordert.


Starten Sie das Script im Installationsorder ("deep-translator/bin") mit
```
./transcribe_translate.py
```
Beim ersten Start lädt Whisper das konfigurerte Modell herunter.













