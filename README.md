# Audio-Dateien transkribieren und übersetzen

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


## Transkribieren und übersetzen mit Whisper und deep-translator
Wer Audio-Dateien automatisch trankribieren und übersetzen möchte verwendet dafür OpenAI-Whisper (https://github.com/openai/whisper) und deep-translator (https://github.com/nidhaloff/deep-translator).

Die Installation in einer virtuellen Ptyhon-Umgebung erfolgt mit dem Script "install-deep-translator.sh". Das Script richtet die nötigen Pakete ein. In der Python-Umgebung erledigt das Script "transcribe_translate.py" die Aufgabe. Öffnen Sie es zuerst in einem Editor und passen Sie die Konfiguration an.







