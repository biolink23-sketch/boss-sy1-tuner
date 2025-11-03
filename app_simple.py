import streamlit as st

# Конфигурация страницы
st.set_page_config(
    page_title="Boss SY-1 Preset Tuner",
    page_icon="🎸",
    layout="wide"
)

# CSS стили
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton > button {
        width: 100%;
        height: 80px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #3498db;
        background-color: white;
        color: #2c3e50;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #3498db;
        color: white;
        transform: scale(1.05);
    }
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: bold;
        color: #3498db;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 10px;
        color: #155724;
        font-size: 18px;
        font-weight: bold;
        margin: 20px 0;
    }
    .warning-box {
        padding: 20px;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 10px;
        color: #721c24;
        font-size: 18px;
        font-weight: bold;
        margin: 20px 0;
    }
    .info-box {
        padding: 20px;
        background-color: #d5f4e6;
        border-left: 4px solid #27ae60;
        border-radius: 10px;
        margin: 20px 0;
    }
    .setting-box {
        padding: 15px;
        background-color: white;
        border-left: 4px solid #3498db;
        border-radius: 10px;
        margin: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .setting-label {
        font-weight: bold;
        font-size: 18px;
        color: #2c3e50;
    }
    .setting-value {
        font-size: 20px;
        font-weight: bold;
        color: white;
        background-color: #3498db;
        padding: 10px 20px;
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# База данных пресетов
PRESETS = {
    "Classic Lead Synth": {
        "desc": "Классический лид-синтезатор для соло",
        "type": "LEAD 1",
        "variation": 3,
        "tone": 7,
        "depth": 5,
        "effect": 8,
        "direct": 3,
        "mode": "GUITAR",
        "good_notes": ["C", "D", "E", "G", "A"]
    },
    "Fat Bass Synth": {
        "desc": "Жирный бас-синтезатор",
        "type": "BASS",
        "variation": 5,
        "tone": 4,
        "depth": 6,
        "effect": 9,
        "direct": 2,
        "mode": "BASS",
        "good_notes": ["E", "A", "D", "G"]
    },
    "Analog Pad": {
        "desc": "Мягкий аналоговый пад",
        "type": "PAD",
        "variation": 2,
        "tone": 6,
        "depth": 7,
        "effect": 7,
        "direct": 4,
        "mode": "GUITAR",
        "good_notes": ["C", "D", "E", "F", "G", "A", "B"]
    },
    "Vintage Strings": {
        "desc": "Винтажные струнные",
        "type": "STR",
        "variation": 4,
        "tone": 5,
        "depth": 5,
        "effect": 8,
        "direct": 5,
        "mode": "GUITAR",
        "good_notes": ["C", "D", "E", "G", "A"]
    },
    "Hammond Organ": {
        "desc": "Классический орган Hammond",
        "type": "ORGN",
        "variation": 6,
        "tone": 8,
        "depth": 4,
        "effect": 9,
        "direct": 3,
        "mode": "GUITAR",
        "good_notes": ["C", "D", "E", "F", "G", "A"]
    },
    "Bell Tower": {
        "desc": "Колокольный звон",
        "type": "BELL",
        "variation": 7,
        "tone": 6,
        "depth": 6,
        "effect": 7,
        "direct": 4,
        "mode": "GUITAR",
        "good_notes": ["C", "E", "G"]
    },
    "Laser Zap": {
        "desc": "Лазерные эффекты",
        "type": "SFX 1",
        "variation": 9,
        "tone": 9,
        "depth": 8,
        "effect": 10,
        "direct": 1,
        "mode": "GUITAR",
        "good_notes": ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    },
    "Arpeggiator": {
        "desc": "Арпеджиатор",
        "type": "SEQ 1",
        "variation": 8,
        "tone": 7,
        "depth": 7,
        "effect": 8,
        "direct": 3,
        "mode": "GUITAR",
        "good_notes": ["C", "D", "E", "G", "A"]
    },
    "Sub Bass": {
        "desc": "Суб-бас для низких частот",
        "type": "BASS",
        "variation": 1,
        "tone": 3,
        "depth": 8,
        "effect": 10,
        "direct": 2,
        "mode": "BASS",
        "good_notes": ["E", "A", "D", "G", "B"]
    },
    "Ambient Pad": {
        "desc": "Эмбиент пад для атмосферы",
        "type": "PAD",
        "variation": 11,
        "tone": 5,
        "depth": 9,
        "effect": 6,
        "direct": 5,
        "mode": "GUITAR",
        "good_notes": ["C", "D", "E", "F", "G", "A", "B"]
    },
    "Sci-Fi Sweep": {
        "desc": "Научно-фантастические свипы",
        "type": "SFX 2",
        "variation": 6,
        "tone": 10,
        "depth": 9,
        "effect": 9,
        "direct": 2,
        "mode": "GUITAR",
        "good_notes": ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    }
}

# Заголовок
st.title("🎸 Boss SY-1 Preset Tuner")
st.markdown("### Простой настройщик пресетов")

# Инструкция
with st.expander("📖 Как использовать", expanded=True):
    st.markdown("""
    **Шаги:**
    1. Выберите пресет из списка ниже
    2. Используйте любой гитарный тюнер (телефон/онлайн)
    3. Сыграйте на гитаре и посмотрите ноту на тюнере
    4. Нажмите эту ноту в приложении
    5. Получите настройки для Boss SY-1!
    """)

# Рекомендованные тюнеры
st.markdown("""
<div class="info-box">
    <h3>🎵 Рекомендуемые тюнеры:</h3>
    <p>
        • <a href="https://tuner-online.com" target="_blank">Tuner Online</a><br>
        • <a href="https://www.musicca.com/guitar-tuner" target="_blank">Musicca Tuner</a><br>
        • <a href="https://www.fender.com/play/tuner" target="_blank">Fender Tuner</a><br>
        • Приложения: GuitarTuna, Pro Guitar Tuner
    </p>
</div>
""", unsafe_allow_html=True)

# Выбор пресета
st.markdown("---")
st.subheader("1️⃣ Выберите пресет")

preset_name = st.selectbox(
    "Пресет:",
    options=[""] + list(PRESETS.keys()),
    format_func=lambda x: "-- Выберите пресет --" if x == "" else x
)

if preset_name:
    preset = PRESETS[preset_name]
    st.info(f"**{preset_name}:** {preset['desc']}")
    
    # Выбор ноты
    st.markdown("---")
    st.subheader("2️⃣ Какую ноту вы играете?")
    st.markdown("*Посмотрите на тюнер и нажмите соответствующую ноту*")
    
    # Кнопки нот
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    cols = [col1, col2, col3, col4, col5, col6]
    
    selected_note = None
    
    for i, note in enumerate(notes):
        col_idx = i % 6
        with cols[col_idx]:
            if st.button(note, key=f"note_{note}"):
                selected_note = note
                st.session_state['selected_note'] = note
    
    # Получаем выбранную ноту из session_state
    if 'selected_note' in st.session_state:
        selected_note = st.session_state['selected_note']
    
    # Анализ ноты
    if selected_note:
        st.markdown("---")
        st.subheader(f"3️⃣ Анализ ноты {selected_note}")
        
        is_good = selected_note in preset['good_notes']
        
        if is_good:
            st.markdown(f"""
            <div class="success-box">
                ✅ Отлично! Нота <strong>{selected_note}</strong> хорошо подходит для пресета "{preset_name}"
            </div>
            """, unsafe_allow_html=True)
            
            st.success("💡 **Совет:** Настройте педаль согласно параметрам ниже и продолжайте играть эту ноту.")
        else:
            st.markdown(f"""
            <div class="warning-box">
                ⚠️ Нота <strong>{selected_note}</strong> не очень подходит для данного пресета
            </div>
            """, unsafe_allow_html=True)
            
            st.warning(f"💡 **Совет:** Попробуйте сыграть одну из этих нот: **{', '.join(preset['good_notes'])}**")
        
        # Настройки педали
        st.markdown("---")
        st.subheader("4️⃣ Настройки Boss SY-1")
        
        settings_col1, settings_col2 = st.columns(2)
        
        with settings_col1:
            st.markdown(f"""
            <div class="setting-box">
                <span class="setting-label">TYPE:</span>
                <span class="setting-value">{preset['type']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="setting-box">
                <span class="setting-label">VARIATION:</span>
                <span class="setting-value">{preset['variation']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="setting-box">
                <span class="setting-label">TONE/RATE:</span>
                <span class="setting-value">{preset['tone']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="setting-box">
                <span class="setting-label">DEPTH:</span>
                <span class="setting-value">{preset['depth']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with settings_col2:
            st.markdown(f"""
            <div class="setting-box">
                <span class="setting-label">EFFECT:</span>
                <span class="setting-value">{preset['effect']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="setting-box">
                <span class="setting-label">DIRECT:</span>
                <span class="setting-value">{preset['direct']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="setting-box">
                <span class="setting-label">MODE:</span>
                <span class="setting-value">{preset['mode']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Визуализация соответствия
        st.markdown("---")
        st.subheader("📊 Визуализация")
        
        viz_col1, viz_col2, viz_col3 = st.columns(3)
        
        with viz_col1:
            st.metric(
                label="Выбранная нота",
                value=selected_note,
                delta="✓ Нажата" if selected_note else None
            )
        
        with viz_col2:
            st.metric(
                label="Соответствие",
                value="✓ Подходит" if is_good else "⚠ Не очень",
                delta="Хорошо" if is_good else "Попробуйте другую",
                delta_color="normal" if is_good else "inverse"
            )
        
        with viz_col3:
            st.metric(
                label="Пресет",
                value=preset_name.split()[0],
                delta=preset['type']
            )
        
        # Все подходящие ноты
        st.markdown("---")
        st.subheader("🎼 Подходящие ноты для этого пресета")
        
        good_notes_cols = st.columns(len(preset['good_notes']))
        for i, note in enumerate(preset['good_notes']):
            with good_notes_cols[i]:
                is_current = (note == selected_note)
                st.button(
                    f"{'🎯 ' if is_current else ''}{note}",
                    key=f"good_note_{note}",
                    disabled=is_current,
                    help=f"{'Вы играете эту ноту!' if is_current else 'Попробуйте сыграть эту ноту'}"
                )

else:
    st.info("👆 Начните с выбора пресета выше")

# Футер
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>🎸 Boss SY-1 Preset Tuner | Простая версия</p>
    <p>Создано для музыкантов с ❤️</p>
</div>
""", unsafe_allow_html=True)
