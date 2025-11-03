// Глобальные переменные
let audioContext;
let analyser;
let microphone;
let dataArray;
let frequencyArray;
let bufferLength;
let isAudioActive = false;
let animationId;
let spectrumAnimationId;
let debugLog = [];
let maxVolume = 0;
let avgVolume = 0;
let volumeHistory = [];
let detectedNotes = [];

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

// Статистика
let stats = {
    totalSamples: 0,
    detectedFrequencies: 0,
    avgConfidence: 0,
    peakVolume: 0
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    initializePresetSelector();
    initializeSliders();
    setupAudioButton();
    setupTestButton();
    setupClearDebugButton();
    displaySystemInfo();
    registerServiceWorker();
    addDebugLog('✓ Приложение загружено и готово к работе');
});

// Функция отладочного лога
function addDebugLog(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = {
        time: timestamp,
        message: message,
        type: type
    };
    
    debugLog.unshift(logEntry);
    if (debugLog.length > 20) debugLog.pop();
    
    updateDebugDisplay();
    
    // Также в консоль
    const prefix = type === 'error' ? '❌' : type === 'warning' ? '⚠️' : type === 'success' ? '✅' : 'ℹ️';
    console.log(`${prefix} [${timestamp}] ${message}`);
}

// Обновление отображения отладки
function updateDebugDisplay() {
    const debugOutput = document.getElementById('debug-output');
    if (!debugOutput) return;
    
    debugOutput.innerHTML = debugLog.map(log => {
        const icon = log.type === 'error' ? '❌' : 
                    log.type === 'warning' ? '⚠️' : 
                    log.type === 'success' ? '✅' : 'ℹ️';
        const className = `debug-entry debug-${log.type}`;
        return `<div class="${className}">${icon} [${log.time}] ${log.message}</div>`;
    }).join('');
}

// Системная информация
function displaySystemInfo() {
    const systemOutput = document.getElementById('system-output');
    if (!systemOutput) return;
    
    const info = {
        'Браузер': navigator.userAgent.split(' ').pop(),
        'Платформа': navigator.platform,
        'Язык': navigator.language,
        'Онлайн': navigator.onLine ? '✅ Да' : '❌ Нет',
        'Cookies': navigator.cookieEnabled ? '✅ Включены' : '❌ Выключены'
    };
    
    systemOutput.innerHTML = Object.entries(info)
        .map(([key, value]) => `<div><strong>${key}:</strong> ${value}</div>`)
        .join('');
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
    
    addDebugLog(`Загружено пресетов: ${Object.keys(PRESETS).length}`, 'success');
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
    
    addDebugLog(`Пресет загружен: ${presetName}`, 'success');
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
    addDebugLog(`TYPE изменён на: ${selectedPreset.type}`, 'success');
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
    addDebugLog(`Режим изменён на: ${selectedPreset.guitar_bass}`, 'success');
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
        addDebugLog('🎉 Все параметры настроены!', 'success');
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
                addDebugLog('Запрос доступа к микрофону...', 'info');
                await startAudio();
                button.innerHTML = '<i class="fas fa-microphone-slash"></i> Выключить микрофон';
                button.classList.add('active');
                status.className = 'status-on';
                status.innerHTML = '<i class="fas fa-circle"></i> Микрофон активен';
                isAudioActive = true;
                document.getElementById('test-sound').style.display = 'inline-block';
                addDebugLog('✓ Микрофон успешно активирован!', 'success');
            } catch (error) {
                addDebugLog('✗ Ошибка доступа к микрофону: ' + error.message, 'error');
                alert('Ошибка доступа к микрофону:\n' + error.message + '\n\nПроверьте разрешения браузера!');
            }
        } else {
            stopAudio();
            button.innerHTML = '<i class="fas fa-microphone"></i> Включить микрофон';
            button.classList.remove('active');
            status.className = 'status-off';
            status.innerHTML = '<i class="fas fa-circle"></i> Микрофон выключен';
            isAudioActive = false;
            document.getElementById('test-sound').style.display = 'none';
            addDebugLog('Микрофон выключен', 'info');
        }
    });
}

// Настройка кнопки теста звука
function setupTestButton() {
    const button = document.getElementById('test-sound');
    button.addEventListener('click', () => {
        if (!isAudioActive || !audioContext) {
            alert('Сначала включите микрофон!');
            return;
        }
        
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 440; // Нота A4
        gainNode.gain.value = 0.1;
        
        oscillator.start();
        setTimeout(() => oscillator.stop(), 500);
        
        addDebugLog('Тестовый звук: 440 Hz (нота A4)', 'info');
    });
}

// Настройка кнопки очистки отладки
function setupClearDebugButton() {
    const button = document.getElementById('clear-debug');
    button.addEventListener('click', () => {
        debugLog = [];
        updateDebugDisplay();
        addDebugLog('Лог очищен', 'info');
    });
}

// Запуск аудио с выбором устройства
async function startAudio() {
    try {
        // Получаем список устройств
        const devices = await navigator.mediaDevices.enumerateDevices();
        const audioDevices = devices.filter(device => device.kind === 'audioinput');
        
        addDebugLog(`Найдено аудио устройств: ${audioDevices.length}`, 'info');
        
        if (audioDevices.length === 0) {
            throw new Error('Микрофоны не найдены! Подключите микрофон.');
        }
        
        // Показываем список устройств
        audioDevices.forEach((device, index) => {
            const label = device.label || `Микрофон ${index + 1}`;
            addDebugLog(`  ${index + 1}. ${label}`, 'info');
        });
        
        // Если больше одного устройства - даём выбрать
        let selectedDeviceId = null;
        if (audioDevices.length > 1) {
            const deviceList = audioDevices.map((d, i) => 
                `${i + 1}. ${d.label || 'Микрофон ' + (i + 1)}`
            ).join('\n');
            
            const choice = prompt(`Найдено ${audioDevices.length} микрофонов:\n\n${deviceList}\n\nВведите номер (1-${audioDevices.length}):`);
            
            if (choice && !isNaN(choice)) {
                const index = parseInt(choice) - 1;
                if (index >= 0 && index < audioDevices.length) {
                    selectedDeviceId = audioDevices[index].deviceId;
                    addDebugLog(`Выбран: ${audioDevices[index].label}`, 'success');
                }
            }
        }
        
        // Создаём AudioContext
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        
        // МАКСИМАЛЬНАЯ ЧУВСТВИТЕЛЬНОСТЬ
        analyser.fftSize = 8192;
        analyser.smoothingTimeConstant = 0.3;
        analyser.minDecibels = -100;
        analyser.maxDecibels = -10;
        
        bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
        frequencyArray = new Uint8Array(analyser.frequencyBinCount);
        
        addDebugLog(`AudioContext: sampleRate=${audioContext.sampleRate} Hz, FFT=${analyser.fftSize}`, 'success');
        
        // Запрашиваем микрофон
        const constraints = {
            audio: selectedDeviceId ? {
                deviceId: { exact: selectedDeviceId },
                echoCancellation: false,
                noiseSuppression: false,
                autoGainControl: true,
                sampleRate: 48000
            } : {
                echoCancellation: false,
                noiseSuppression: false,
                autoGainControl: true,
                sampleRate: 48000
            }
        };
        
        addDebugLog('Запрос микрофона...', 'info');
        
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        
        // Информация о выбранном устройстве
        const tracks = stream.getAudioTracks();
        if (tracks.length > 0) {
            const settings = tracks[0].getSettings();
            addDebugLog(`✓ Используется: ${tracks[0].label}`, 'success');
            addDebugLog(`Настройки: sampleRate=${settings.sampleRate}, channels=${settings.channelCount}`, 'info');
            
            // Проверяем, что трек активен
            if (tracks[0].readyState !== 'live') {
                throw new Error('Микрофон не активен! readyState=' + tracks[0].readyState);
            }
            
            addDebugLog(`Статус микрофона: ${tracks[0].readyState} (должно быть "live")`, 'info');
        }
        
        // Подключаем микрофон
        microphone = audioContext.createMediaStreamSource(stream);
        
        // Добавляем усилитель
        const gainNode = audioContext.createGain();
        gainNode.gain.value = 5.0; // Усиление x5!
        
        microphone.connect(gainNode);
        gainNode.connect(analyser);
        
        addDebugLog('✓ Микрофон подключен с усилением x5', 'success');
        addDebugLog('💡 ГОВОРИТЕ ГРОМКО или ХЛОПНИТЕ В ЛАДОШИ!', 'warning');
        addDebugLog('💡 Если 0% не меняется - микрофон не работает!', 'warning');
        
        // Сбрасываем статистику
        stats = {
            totalSamples: 0,
            detectedFrequencies: 0,
            avgConfidence: 0,
            peakVolume: 0
        };
        maxVolume = 0;
        volumeHistory = [];
        
        // Запускаем анализ
        detectPitch();
        drawWaveform();
        drawSpectrum();
        
        // Через 3 секунды проверяем, работает ли
        setTimeout(() => {
            if (maxVolume === 0) {
                addDebugLog('⚠️ За 3 секунды не было звука! Проверьте микрофон!', 'error');
                addDebugLog('1. Говорите прямо в микрофон', 'warning');
                addDebugLog('2. Проверьте, не выключен ли микрофон (кнопка mute)', 'warning');
                addDebugLog('3. Зайдите в настройки звука системы', 'warning');
            } else {
                addDebugLog(`✓ Микрофон работает! Пик громкости: ${maxVolume}%`, 'success');
            }
        }, 3000);
        
    } catch (error) {
        addDebugLog('✗ КРИТИЧЕСКАЯ ОШИБКА: ' + error.message, 'error');
        if (error.name === 'NotFoundError') {
            addDebugLog('Микрофон не найден! Подключите микрофон к компьютеру.', 'error');
        } else if (error.name === 'NotAllowedError') {
            addDebugLog('Доступ к микрофону запрещён! Разрешите в настройках браузера.', 'error');
        } else if (error.name === 'NotReadableError') {
            addDebugLog('Микрофон занят другим приложением! Закройте Zoom/Skype/Discord.', 'error');
        }
        throw error;
    }
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
    if (spectrumAnimationId) {
        cancelAnimationFrame(spectrumAnimationId);
    }
    
    // Очищаем canvas
    const waveformCanvas = document.getElementById('waveform');
    const spectrumCanvas = document.getElementById('spectrum');
    if (waveformCanvas) {
        const ctx = waveformCanvas.getContext('2d');
        ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, waveformCanvas.width, waveformCanvas.height);
    }
    if (spectrumCanvas) {
        const ctx = spectrumCanvas.getContext('2d');
        ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, spectrumCanvas.width, spectrumCanvas.height);
    }
    
    addDebugLog(`Статистика сессии: обработано ${stats.totalSamples} сэмплов, распознано ${stats.detectedFrequencies} частот, пик ${stats.peakVolume}%`, 'info');
}

// Детекция высоты тона
function detectPitch() {
    if (!isAudioActive) return;
    
    stats.totalSamples++;
    
    analyser.getByteTimeDomainData(dataArray);
    
    // Расчёт RMS (громкости)
    let sum = 0;
    for (let i = 0; i < bufferLength; i++) {
        const normalized = (dataArray[i] - 128) / 128;
        sum += normalized * normalized;
    }
    const rms = Math.sqrt(sum / bufferLength);
    const volume = Math.round(rms * 300); // Коэффициент для чувствительности
    
    // Обновляем историю громкости
    volumeHistory.push(volume);
    if (volumeHistory.length > 10) volumeHistory.shift();
    avgVolume = Math.round(volumeHistory.reduce((a, b) => a + b, 0) / volumeHistory.length);
    
    if (volume > maxVolume) {
        maxVolume = volume;
        stats.peakVolume = volume;
    }
    
    // Расчёт в децибелах
    const db = rms > 0 ? 20 * Math.log10(rms) : -Infinity;
    
    // Обновляем индикаторы
    const volumeFill = document.getElementById('volume-fill');
    const volumeText = document.getElementById('volume-text');
    const volumeDb = document.getElementById('volume-db');
    const signalStatus = document.getElementById('signal-status');
    const audioIndicator = document.getElementById('audio-indicator');
    const waveformStatus = document.getElementById('waveform-status');
    
    if (volumeFill && volumeText) {
        const displayVolume = Math.min(volume, 100);
        volumeFill.style.width = `${displayVolume}%`;
        volumeText.textContent = `${volume}%`;
        volumeDb.textContent = db === -Infinity ? '-∞ dB' : `${db.toFixed(1)} dB`;
        
        // Статус сигнала
        if (volume < 1) {
            signalStatus.textContent = '🔇 Нет сигнала - Сыграйте громче!';
            signalStatus.style.color = '#e74c3c';
            audioIndicator.className = 'audio-indicator off';
            waveformStatus.textContent = 'Ожидание звука... Сыграйте на гитаре!';
        } else if (volume < 5) {
            signalStatus.textContent = '🔉 Слабый сигнал - Увеличьте громкость усилителя';
            signalStatus.style.color = '#f39c12';
            audioIndicator.className = 'audio-indicator weak';
            waveformStatus.textContent = 'Сигнал слабый, увеличьте громкость';
        } else if (volume < 15) {
            signalStatus.textContent = '🔊 Сигнал хороший - Продолжайте!';
            signalStatus.style.color = '#2ecc71';
            audioIndicator.className = 'audio-indicator good';
            waveformStatus.textContent = 'Сигнал хороший, анализирую...';
        } else {
            signalStatus.textContent = '🔊🔊 Отличный сигнал!';
            signalStatus.style.color = '#27ae60';
            audioIndicator.className = 'audio-indicator excellent';
            waveformStatus.textContent = 'Отличный сигнал!';
        }
    }
    
    // Автокорреляция для определения частоты
    const frequency = autoCorrelate(dataArray, audioContext.sampleRate);
    
    // Порог 0.3% для максимальной чувствительности
    if (frequency > 0 && volume > 0.3) {
        const note = frequencyToNote(frequency);
        const confidence = Math.min(100, Math.round((volume / 20) * 100));
        
        document.getElementById('detected-note').textContent = note;
        document.getElementById('frequency').textContent = `${frequency.toFixed(2)} Hz`;
        document.getElementById('note-confidence').textContent = `Точность: ${confidence}%`;
        
        stats.detectedFrequencies++;
        
        // Добавляем в историю нот
        detectedNotes.push({ note, frequency, volume, time: Date.now() });
        if (detectedNotes.length > 50) detectedNotes.shift();
        
        // Логируем только при изменении ноты
        if (!window.lastNote || window.lastNote !== note) {
            addDebugLog(`♪ ${note} (${frequency.toFixed(1)} Hz, громкость ${volume}%, точность ${confidence}%)`, 'success');
            window.lastNote = note;
            window.lastLogTime = Date.now();
        }
    } else {
        document.getElementById('detected-note').textContent = '--';
        document.getElementById('frequency').textContent = '-- Hz';
        document.getElementById('note-confidence').textContent = 'Точность: --%';
        
        // Логируем проблемы
        if (volume < 0.3 && stats.totalSamples % 50 === 0) {
            addDebugLog(`⚠ Сигнал слишком слабый: ${volume}% (нужно >0.3%). Макс: ${maxVolume}%, Средн: ${avgVolume}%`, 'warning');
        }
        
        if (volume >= 0.3 && frequency <= 0 && stats.totalSamples % 50 === 0) {
            addDebugLog(`⚠ Есть звук (${volume}%), но частота не определена. Возможно, шум или слишком сложный сигнал.`, 'warning');
        }
    }
    
    setTimeout(() => detectPitch(), 30);
}

// Автокорреляция
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
    
    if (rms < 0.001) return -1;
    
    // Ищем корреляцию
    let lastCorrelation = 1;
    for (let offset = 1; offset < MAX_SAMPLES; offset++) {
        let correlation = 0;
        
        for (let i = 0; i < MAX_SAMPLES; i++) {
            correlation += Math.abs(((buffer[i] - 128) / 128) - ((buffer[i + offset] - 128) / 128));
        }
        
        correlation = 1 - (correlation / MAX_SAMPLES);
        
        if (correlation > 0.85 && correlation > lastCorrelation) {
            if (correlation > best_correlation) {
                best_correlation = correlation;
                best_offset = offset;
            }
        }
        
        lastCorrelation = correlation;
    }
    
    if (best_correlation > 0.01 && best_offset > 0) {
        const frequency = sampleRate / best_offset;
        
        // Диапазон для гитары/баса: 70-1500 Hz
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
    ctx.setLineDash([5, 5]);
    
    for (let i = 0; i <= 4; i++) {
        const y = (height / 4) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
    }
    
    ctx.setLineDash([]);
    
    // Центральная линия
    ctx.strokeStyle = '#555';
    ctx.lineWidth = 2;
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

// Отрисовка спектра
function drawSpectrum() {
    if (!isAudioActive) return;
    
    const canvas = document.getElementById('spectrum');
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    analyser.getByteFrequencyData(frequencyArray);
    
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, width, height);
    
    const barWidth = (width / frequencyArray.length) * 2.5;
    let barHeight;
    let x = 0;
    
    for (let i = 0; i < frequencyArray.length; i++) {
        barHeight = (frequencyArray[i] / 255) * height;
        
        const gradient = ctx.createLinearGradient(0, height - barHeight, 0, height);
        gradient.addColorStop(0, '#e74c3c');
        gradient.addColorStop(0.5, '#f39c12');
        gradient.addColorStop(1, '#2ecc71');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(x, height - barHeight, barWidth, barHeight);
        
        x += barWidth + 1;
    }
    
    spectrumAnimationId = requestAnimationFrame(drawSpectrum);
}

// Регистрация Service Worker
function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('service-worker.js')
            .then(() => addDebugLog('Service Worker зарегистрирован', 'success'))
            .catch(err => addDebugLog('Ошибка Service Worker: ' + err, 'error'));
    }
}
