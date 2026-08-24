#!/usr/bin/env bash
# Diagnostico de microfone para Linux e macOS.
# Uso: bash verificar_microfone.sh

echo "=== Sistema ==="
uname -srm
echo

if [[ "$(uname -s)" == "Darwin" ]]; then
    echo "=== Dispositivos de entrada (macOS) ==="
    system_profiler SPAudioDataType | grep -A 6 -i "input"
    echo
    echo "Para gravar 5 segundos de teste (precisa do ffmpeg):"
    echo "  ffmpeg -f avfoundation -i \":0\" -t 5 teste_mic.wav"
    exit 0
fi

echo "=== Placas de som detectadas pelo kernel ==="
if [[ -r /proc/asound/cards ]]; then
    cat /proc/asound/cards
else
    echo "Nenhuma placa em /proc/asound (driver de audio ausente ou sem permissao)."
fi
echo

echo "=== Dispositivos de captura (ALSA) ==="
if command -v arecord >/dev/null 2>&1; then
    arecord -l
else
    echo "arecord ausente. Instale: sudo apt install alsa-utils"
fi
echo

echo "=== Fontes do PulseAudio / PipeWire ==="
if command -v pactl >/dev/null 2>&1; then
    pactl list sources short
    echo
    echo "--- Fonte padrao e estado de mudo ---"
    padrao=$(pactl get-default-source 2>/dev/null)
    echo "Padrao: ${padrao:-desconhecida}"
    [[ -n "$padrao" ]] && pactl list sources | grep -A 15 "Name: $padrao" | grep -Ei "mute|volume|state" | head -5
else
    echo "pactl ausente. Instale: sudo apt install pulseaudio-utils"
fi
echo

echo "=== Permissao de acesso aos dispositivos ==="
if [[ -d /dev/snd ]]; then
    ls -l /dev/snd
    id -nG | tr ' ' '\n' | grep -qx audio \
        && echo "OK: usuario esta no grupo 'audio'." \
        || echo "AVISO: usuario fora do grupo 'audio' (sudo usermod -aG audio \$USER)."
else
    echo "/dev/snd nao existe: sem hardware de audio visivel para o sistema."
fi
echo

echo "=== Teste pratico de gravacao ==="
if command -v arecord >/dev/null 2>&1; then
    echo "Gravando 5 segundos... fale algo agora."
    if arecord -d 5 -f cd -t wav /tmp/teste_mic.wav 2>/tmp/teste_mic.err; then
        tamanho=$(stat -c%s /tmp/teste_mic.wav 2>/dev/null || echo 0)
        echo "Arquivo gerado: /tmp/teste_mic.wav (${tamanho} bytes)"
        if (( tamanho > 100000 )); then
            echo "OK: o microfone capturou audio. Ouca com: aplay /tmp/teste_mic.wav"
        else
            echo "AVISO: arquivo muito pequeno; provavelmente nao houve captura real."
        fi
    else
        echo "FALHA ao gravar:"
        cat /tmp/teste_mic.err
    fi
else
    echo "Pulado: arecord nao instalado."
fi
