// Глобальные переменные
let audioContext;
let analyser;
let microphone;
let dataArray;
let bufferLength;
let isAudioActive = false;
let animationId;
let debugLog = [];

// Текущие настройки
let currentSettings = {
    type: "LEAD 1",
    variation: 1,
    tone_rate: 5,
    depth: 5,
    effect: 5,
    direct: 5,
    guitar_bass: "GUITAR"
};

let selectedPreset = null;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    initializePresetSelector();
    initializeSliders();
    setupAudioButton();
    registerServiceWorker();
    addDebugLog('Приложение загружено');
});

// Функция отладочного лога
function addDebugLog(message) {
    const timestamp = new Date().toLocaleTimeString();
    debugLog.push(`[${timestamp}] ${message}`);
    if (debugLog.length > 10) debugLog.shift();
    
    const debugOutput = document.getElementById('debug-output');
    if (debugOutput) {
        debugOutput.innerHTML = debugLog.map(log => `<div>${log}</div>`).join('');
    }
    console.log(message);
}

// Инициализация выбора пресетов
function initializePresetSelector() {
    const select = document.getElementById('preset-select');
    
    Object.keys(PRESETS).forEach(presetName => {
        const option = document.createElement('option');
        option.value = presetName;
        option.textContent = presetName;
        select.appendChild(option);
    });
    
    select.addEventListener('change', (e) => {
        if (e.target.value) {
            loadPreset(e.target.value);
        }
    });
    
    addDebugLog('Пресеты загружены: ' + Object.keys(PRESETS).length);
}

// Загрузка пресета
function loadPreset(presetName) {
    selectedPreset = PRESETS[presetName];
    
    document.getElementById('preset-description').innerHTML = `
        <i class="fas fa-info-circle"></i> ${selectedPreset.description}
    `;
    
    document.getElementById('target-type').textContent = selectedPreset.type;
    document.getElementById('target-mode').textContent = selectedPreset.guitar_bass;
    
    document.getElementById('variation-target-val').textContent = selectedPreset.variation;
    document.getElementById('tone-target-val').textContent = selectedPreset.tone_rate;
    document.getElementById('depth-target-val').textContent = selectedPreset.depth;
    document.getElementById('effect-target-val').textContent = selectedPreset.effect;
    document.getElementById('direct-target-val').textContent = selectedPreset.direct;
    
    updateAllKnobs();
    updateProgress();
    
    addDebugLog('Загружен пресет: ' + presetName);
}

// Инициализация слайдеров
function initializeSliders() {
    const sliders = ['variation', 'tone', 'depth', 'effect', 'direct'];
    
    sliders.forEach(param => {
        const slider = document.getElementById(`${param}-slider`);
        slider.addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            const paramKey = param === 'tone' ? 'tone_rate' : param;
            currentSettings[paramKey] = value;
            
            document.getElementById(`${param}-current-val`).textContent = value;
            updateKnob(param, value);
            updateProgress();
        });
    });
}

// Обновление визуализации ручки
function updateKnob(param, currentValue) {
    if (!selectedPreset) return;
    
    const paramKey = param === 'tone' ? 'tone_rate' : param;
    const targetValue = selectedPreset[paramKey];
    const maxValue = param === 'variation' ? 11 : 10;
    
    const currentAngle = ((currentValue / maxValue) * 270) - 135;
    const targetAngle = ((targetValue / maxValue) * 270) - 135;
    
    const currentLine = document.getElementById(`${param}-current`);
    const targetLine = document.getElementById(`${param}-target`);
    
    const currentRad = (currentAngle * Math.PI) / 180;
    const targetRad = (targetAngle * Math.PI) / 180;
    
    const currentX = 100 + 60 * Math.sin(currentRad);
    const currentY = 100 - 60 * Math.cos(currentRad);
    const targetX = 100 + 60 * Math.sin(targetRad);
    const targetY = 100 - 60 * Math.cos(targetRad);
    
    currentLine.setAttribute('x2', currentX);
    currentLine.setAttribute('y2', currentY);
    targetLine.setAttribute('x2', targetX);
    targetLine.setAttribute('y2', targetY);
    
    const arrowElement = document.getElementById(`${param}-arrow`);
    if (currentValue < targetValue) {
        arrowElement.innerHTML = '↻ Вправо';
        arrowElement.style.color = '#2ecc71';
    } else if (currentValue > targetValue) {
        arrowElement.innerHTML = '↺ Влево';
        arrowElement.style.color = '#e74c3c';
    } else {
        arrowElement.innerHTML = '✓ OK';
        arrowElement.style.color = '#27ae60';
    }
}

// Обновление всех ручек
function updateAllKnobs() {
    ['variation', 'tone', 'depth', 'effect', 'direct'].forEach(param => {
        const paramKey = param === 'tone' ? 'tone_rate' : param;
        updateKnob(param, currentSettings[paramKey]);
    });
    
    updateTypeArrow();
    updateModeArrow();
}

// Обновление стрелки TYPE
function updateTypeArrow() {
    if (!selectedPreset) return;
    
    const arrow = document.getElementById('type-arrow');
    if (currentSettings.type === selectedPreset.type) {
        arrow.innerHTML = '<i class="fas fa-check"></i> OK';
        arrow.style.color = '#27ae60';
    } else {
        arrow.innerHTML = '<i class="fas fa-arrow-right"></i> Измените';
        arrow.style.color = '#e74c3c';
    }
}

// Обновление стрелки режима
function updateModeArrow() {
    if (!selectedPreset) return;
    
    const arrow = document.getElementById('mode-arrow');
    if (currentSettings.guitar_bass === selectedPreset.guitar_bass) {
        arrow.innerHTML = '<i class="fas fa-check"></i> OK';
        arrow.style.color = '#27ae60';
    } else {
        arrow.innerHTML = '<i class="fas fa-arrow-right"></i> Переключите';
        arrow.style.color = '#e74c3c';
    }
}

// Подтверждение TYPE
function confirmType() {
    if (!selectedPreset) {
        alert('Сначала выберите пресет!');
        return;
    }
    
    currentSettings.type = selectedPreset.type;
    document.getElementById('current-type').textContent = selectedPreset.type;
    updateTypeArrow();
    updateProgress();
}

// Подтверждение режима
function confirmMode() {
    if (!selectedPreset) {
        alert('Сначала выберите пресет!');
        return;
    }
    
    currentSettings.guitar_bass = selectedPreset.guitar_bass;
    document.getElementById('current-mode').textContent = selectedPreset.guitar_bass;
    updateModeArrow();
    updateProgress();
}

// Обновление прогресса
function updateProgress() {
    if (!selectedPreset) return;
    
    let correctParams = 0;
    const totalParams = 7;
    
    if (currentSettings.type === selectedPreset.type) correctParams++;
    if (currentSettings.guitar_bass === selectedPreset.guitar_bass) correctParams++;
    if (currentSettings.variation === selectedPreset.variation) correctParams++;
    if (currentSettings.tone_rate === selectedPreset.tone_rate) correctParams++;
    if (currentSettings.depth === selectedPreset.depth) correctParams++;
    if (currentSettings.effect === selectedPreset.effect) correctParams++;
    if (currentSettings.direct === selectedPreset.direct) correctParams++;
    
    const percentage = (correctParams / totalParams) * 100;
    
    document.getElementById('progress-fill').style.width = `${percentage}%`;
    document.getElementById('progress-text').textContent = 
        `${correctParams}/${totalParams} параметров настроено (${Math.round(percentage)}%)`;
    
    const completionMessage = document.getElementById('completion-message');
    if (percentage === 100) {
        completionMessage.classList.remove('hidden');
    } else {
        completionMessage.classList.add('hidden');
    }
}

// Настройка кнопки аудио
function setupAudioButton() {
    const button = document.getElementById('start-audio');
    const status = document.getElementById('audio-status');
    
    button.addEventListener('click', async () => {
        if (!isAudioActive) {
            try {
                addDebugLog('Запрос доступа к микрофону...');
                await startAudio();
                button.innerHTML = '<i class="fas fa-microphone-slash"></i> Выключить микрофон';
                status.className = 'status-on';
                status.innerHTML = '<i class="fas fa-circle"></i> Микрофон активен';
                isAudioActive = true;
                addDebugLog('✓ Микрофон активирован');
            } catch (error) {
                addDebugLog('✗ Ошибка: ' + error.message);
                alert('Ошибка доступа к микрофону: ' + error.message);
            }
        } else {
            stopAudio();
            button.innerHTML = '<i class="fas fa-microphone"></i> Включить микрофон';
            status.className = 'status-off';
            status.innerHTML = '<i class="fas fa-circle"></i> Микрофон выключен';
            isAudioActive = false;
            addDebugLog('Микрофон выключен');
        }
    });
}

// Запуск аудио
async function startAudio() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 4096; // Увеличено для лучшей точности
    analyser.smoothingTimeConstant = 0.8;
    
    bufferLength = analyser.frequencyBinCount;
    dataArray = new Uint8Array(bufferLength);
    
    addDebugLog('AudioContext создан, sampleRate: ' + audioContext.sampleRate);
    
    const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
            echoCancellation: false,
            noiseSuppression: false,
            autoGainControl: false
        } 
    });
    
    microphone = audioContext.createMediaStreamSource(stream);
    microphone.connect(analyser);
    
    addDebugLog('Микрофон подключен к анализатору');
    
    detectPitch();
    drawWaveform();
}

// Остановка аудио
function stopAudio() {
    if (microphone) {
        microphone.disconnect();
        microphone = null;
    }
    if (audioContext) {
        audioContext.close();
        audioContext = null;
    }
    if (animationId) {
        cancelAnimationFrame(animationId);
    }
}

// Детекция высоты тона (улучшенная версия)
function detectPitch() {
    if (!isAudioActive) return;
    
    analyser.getByteTimeDomainData(dataArray);
    
    // Расчёт уровня громкости (RMS)
    let sum = 0;
    for (let i = 0; i < bufferLength; i++) {
        const normalized = (dataArray[i] - 128) / 128;
        sum += normalized * normalized;
    }
    const rms = Math.sqrt(sum / bufferLength);
    const volume = Math.round(rms * 100);
    
    // Обновляем индикатор громкости
    const volumeFill = document.getElementById('volume-fill');
    const volumeText = document.getElementById('volume-text');
    const signalStatus = document.getElementById('signal-status');
    
    if (volumeFill && volumeText) {
        volumeFill.style.width = `${Math.min(volume * 3, 100)}%`;
        volumeText.textContent = `${volume}%`;
        
        if (volume < 1) {
            signalStatus.textContent = '🔇 Нет сигнала';
            signalStatus.style.color = '#e74c3c';
        } else if (volume < 5) {
            signalStatus.textContent = '🔉 Слабый сигнал';
            signalStatus.style.color = '#f39c12';
        } else {
            signalStatus.textContent = '🔊 Сигнал хороший';
            signalStatus.style.color = '#2ecc71';
        }
    }
    
    // Автокорреляция для определения частоты
    const frequency = autoCorrelate(dataArray, audioContext.sampleRate);
    
    if (frequency > 0 && volume > 2) {
        const note = frequencyToNote(frequency);
        document.getElementById('detected-note').textContent = note;
        document.getElementById('frequency').textContent = `${frequency.toFixed(2)} Hz`;
        
        // Логируем только при изменении ноты
        if (!window.lastNote || window.lastNote !== note) {
            addDebugLog(`Нота: ${note}, Частота: ${frequency.toFixed(2)} Hz, Громкость: ${volume}%`);
            window.lastNote = note;
        }
    } else {
        document.getElementById('detected-note').textContent = '--';
        document.getElementById('frequency').textContent = '-- Hz';
        
        if (volume < 2 && !window.lowVolumeLogged) {
            addDebugLog(`Сигнал слишком слабый: ${volume}% (нужно >2%)`);
            window.lowVolumeLogged = true;
        } else if (volume >= 2) {
            window.lowVolumeLogged = false;
        }
    }
    
    setTimeout(() => detectPitch(), 50); // Увеличена частота опроса
}

// Автокорреляция (улучшенный алгоритм)
function autoCorrelate(buffer, sampleRate) {
    const SIZE = buffer.length;
    const MAX_SAMPLES = Math.floor(SIZE / 2);
    let best_offset = -1;
    let best_correlation = 0;
    let rms = 0;
    
    // Расчёт RMS
    for (let i = 0; i < SIZE; i++) {
        const val = (buffer[i] - 128) / 128;
        rms += val * val;
    }
    rms = Math.sqrt(rms / SIZE);
    
    // Если сигнал слишком слабый, выходим
    if (rms < 0.01) return -1;
    
    // Поиск первого пересечения нуля
    let lastCorrelation = 1;
    for (let offset = 1; offset < MAX_SAMPLES; offset++) {
        let correlation = 0;
        
        for (let i = 0; i < MAX_SAMPLES; i++) {
            correlation += Math.abs(((buffer[i] - 128) / 128) - ((buffer[i + offset] - 128) / 128));
        }
        
        correlation = 1 - (correlation / MAX_SAMPLES);
        
        if (correlation > 0.9 && correlation > lastCorrelation) {
            const foundGoodCorrelation = correlation > best_correlation;
            if (foundGoodCorrelation) {
                best_correlation = correlation;
                best_offset = offset;
            }
        }
        
        lastCorrelation = correlation;
    }
    
    if (best_correlation > 0.01 && best_offset > 0) {
        const frequency = sampleRate / best_offset;
        
        // Фильтруем нереалистичные частоты для гитары (82-1200 Hz)
        if (frequency >= 70 && frequency <= 1500) {
            return frequency;
        }
    }
    
    return -1;
}

// Преобразование частоты в ноту
function frequencyToNote(frequency) {
    let closestNote = '';
    let minDiff = Infinity;
    
    for (const [note, frequencies] of Object.entries(NOTE_FREQUENCIES)) {
        for (let octave = 0; octave < frequencies.length; octave++) {
            const diff = Math.abs(frequency - frequencies[octave]);
            if (diff < minDiff) {
                minDiff = diff;
                closestNote = `${note}${octave}`;
            }
        }
    }
    
    return closestNote;
}

// Отрисовка формы волны
function drawWaveform() {
    if (!isAudioActive) return;
    
    const canvas = document.getElementById('waveform');
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    analyser.getByteTimeDomainData(dataArray);
    
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, width, height);
    
    // Сетка
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, height / 2);
    ctx.lineTo(width, height / 2);
    ctx.stroke();
    
    // Форма волны
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#3498db';
    ctx.beginPath();
    
    const sliceWidth = width / bufferLength;
    let x = 0;
    
    for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = v * height / 2;
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
        
        x += sliceWidth;
    }
    
    ctx.lineTo(width, height / 2);
    ctx.stroke();
    
    animationId = requestAnimationFrame(drawWaveform);
}

// Регистрация Service Worker
function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('service-worker.js')
            .then(() => addDebugLog('Service Worker зарегистрирован'))
            .catch(err => addDebugLog('Ошибка Service Worker: ' + err));
    }
}
