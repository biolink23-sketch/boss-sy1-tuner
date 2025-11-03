import streamlit as st
import numpy as np
try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except:
    AUDIO_AVAILABLE = False
import plotly.graph_objects as go
from scipy import signal
import time

# Конфигурация страницы
st.set_page_config(
    page_title="Boss SY-1 Preset Tuner",
    page_icon="🎸",
    layout="wide"
)

# База данных пресетов
PRESETS = {
    "Classic Lead Synth": {
        "type": "LEAD 1",
        "variation": 3,
        "tone_rate": 7,
        "depth": 5,
        "effect": 8,
        "direct": 3,
        "guitar_bass": "GUITAR",
        "description": "Классический лид-синтезатор для соло"
    },
    "Fat Bass Synth": {
        "type": "BASS",
        "variation": 5,
        "tone_rate": 4,
        "depth": 6,
        "effect": 9,
        "direct": 2,
        "guitar_bass": "BASS",
        "description": "Жирный бас-синтезатор"
    },
    "Analog Pad": {
        "type": "PAD",
        "variation": 2,
        "tone_rate": 6,
        "depth": 7,
        "effect": 7,
        "direct": 4,
        "guitar_bass": "GUITAR",
        "description": "Мягкий аналоговый пад"
    },
    "Vintage Strings": {
        "type": "STR",
        "variation": 4,
        "tone_rate": 5,
        "depth": 5,
        "effect": 8,
        "direct": 5,
        "guitar_bass": "GUITAR",
        "description": "Винтажные струнные"
    },
    "Hammond Organ": {
        "type": "ORGN",
        "variation": 6,
        "tone_rate": 8,
        "depth": 4,
        "effect": 9,
        "direct": 3,
        "guitar_bass": "GUITAR",
        "description": "Классический орган Hammond"
    },
    "Bell Tower": {
        "type": "BELL",
        "variation": 7,
        "tone_rate": 6,
        "depth": 6,
        "effect": 7,
        "direct": 4,
        "guitar_bass": "GUITAR",
        "description": "Колокольный звон"
    },
    "Laser Zap": {
        "type": "SFX 1",
        "variation": 9,
        "tone_rate": 9,
        "depth": 8,
        "effect": 10,
        "direct": 1,
        "guitar_bass": "GUITAR",
        "description": "Лазерные эффекты"
    },
    "Arpeggiator": {
        "type": "SEQ 1",
        "variation": 8,
        "tone_rate": 7,
        "depth": 7,
        "effect": 8,
        "direct": 3,
        "guitar_bass": "GUITAR",
        "description": "Арпеджиатор"
    },
    "Octave Lead": {
        "type": "LEAD 2",
        "variation": 10,
        "tone_rate": 8,
        "depth": 6,
        "effect": 9,
        "direct": 4,
        "guitar_bass": "GUITAR",
        "description": "Лид с октавой вверх"
    },
    "Sub Bass": {
        "type": "BASS",
        "variation": 1,
        "tone_rate": 3,
        "depth": 8,
        "effect": 10,
        "direct": 2,
        "guitar_bass": "BASS",
        "description": "Суб-бас для низких частот"
    },
    "Ambient Pad": {
        "type": "PAD",
        "variation": 11,
        "tone_rate": 5,
        "depth": 9,
        "effect": 6,
        "direct": 5,
        "guitar_bass": "GUITAR",
        "description": "Эмбиент пад для атмосферы"
    },
    "Sci-Fi Sweep": {
        "type": "SFX 2",
        "variation": 6,
        "tone_rate": 10,
        "depth": 9,
        "effect": 9,
        "direct": 2,
        "guitar_bass": "GUITAR",
        "description": "Научно-фантастические свипы"
    }
}

# Маппинг типов на позиции
TYPE_POSITIONS = {
    "LEAD 1": 1,
    "LEAD 2": 2,
    "PAD": 3,
    "BASS": 4,
    "STR": 5,
    "BELL": 6,
    "ORGN": 7,
    "SFX 1": 8,
    "SFX 2": 9,
    "SEQ 1": 10,
    "SEQ 2": 11
}

# Инициализация состояния
if 'current_settings' not in st.session_state:
    st.session_state.current_settings = {
        "type": "LEAD 1",
        "variation": 1,
        "tone_rate": 5,
        "depth": 5,
        "effect": 5,
        "direct": 5,
        "guitar_bass": "GUITAR"
    }

if 'audio_monitoring' not in st.session_state:
    st.session_state.audio_monitoring = False

if 'audio_data' not in st.session_state:
    st.session_state.audio_data = []

# Функция для создания стрелки направления
def create_arrow(current, target, label):
    if current < target:
        arrow = "↻ Вправо"
        color = "#00ff00"
        steps = target - current
    elif current > target:
        arrow = "↺ Влево"
        color = "#ff6b6b"
        steps = current - target
    else:
        arrow = "✓ На месте"
        color = "#4CAF50"
        steps = 0
    
    return arrow, color, steps

# Функция для отрисовки ручки управления
def draw_knob(current_value, target_value, max_value, label):
    fig = go.Figure()
    
    # Текущая позиция
    current_angle = (current_value / max_value) * 270 - 135
    target_angle = (target_value / max_value) * 270 - 135
    
    # Окружность ручки
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        marker=dict(size=100, color='#2c3e50'),
        showlegend=False
    ))
    
    # Текущая позиция (красная линия)
    current_x = 0.4 * np.cos(np.radians(current_angle))
    current_y = 0.4 * np.sin(np.radians(current_angle))
    fig.add_trace(go.Scatter(
        x=[0, current_x], y=[0, current_y],
        mode='lines',
        line=dict(color='#e74c3c', width=4),
        name='Текущее'
    ))
    
    # Целевая позиция (зелёная линия)
    target_x = 0.4 * np.cos(np.radians(target_angle))
    target_y = 0.4 * np.sin(np.radians(target_angle))
    fig.add_trace(go.Scatter(
        x=[0, target_x], y=[0, target_y],
        mode='lines',
        line=dict(color='#2ecc71', width=4),
        name='Целевое'
    ))
    
    fig.update_layout(
        title=label,
        xaxis=dict(range=[-0.6, 0.6], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-0.6, 0.6], showgrid=False, zeroline=False, showticklabels=False),
        height=250,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Функция аудио-мониторинга
def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    st.session_state.audio_data.append(indata.copy())

# Заголовок
st.title("🎸 Boss SY-1 Preset Tuner")
st.markdown("### Интерактивный настройщик пресетов для Boss SY-1")

# Боковая панель
with st.sidebar:
    st.header("⚙️ Настройки")
    
    # Выбор пресета
    preset_name = st.selectbox(
        "Выберите пресет:",
        options=list(PRESETS.keys()),
        help="Выберите готовый пресет из библиотеки"
    )
    
    selected_preset = PRESETS[preset_name]
    
    st.info(f"📝 {selected_preset['description']}")
    
    st.markdown("---")
    
    # Текущие настройки педали
    st.subheader("🎛️ Текущие настройки")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.current_settings['effect'] = st.slider(
            "EFFECT", 0, 10, st.session_state.current_settings['effect']
        )
        st.session_state.current_settings['tone_rate'] = st.slider(
            "TONE/RATE", 0, 10, st.session_state.current_settings['tone_rate']
        )
        st.session_state.current_settings['variation'] = st.slider(
            "VARIATION", 1, 11, st.session_state.current_settings['variation']
        )
    
    with col2:
        st.session_state.current_settings['direct'] = st.slider(
            "DIRECT", 0, 10, st.session_state.current_settings['direct']
        )
        st.session_state.current_settings['depth'] = st.slider(
            "DEPTH", 0, 10, st.session_state.current_settings['depth']
        )
        st.session_state.current_settings['guitar_bass'] = st.radio(
            "MODE", ["GUITAR", "BASS"]
        )
    
    st.markdown("---")
    
    # Аудио мониторинг
st.subheader("🎤 Аудио мониторинг")

if AUDIO_AVAILABLE:
    if st.button("▶️ Старт мониторинг" if not st.session_state.audio_monitoring else "⏸️ Стоп мониторинг"):
        st.session_state.audio_monitoring = not st.session_state.audio_monitoring
else:
    st.info("⚠️ Аудио мониторинг доступен только в локальной версии")

# Основная область
tab1, tab2, tab3 = st.tabs(["🎯 Настройка", "📊 Визуализация", "📚 Библиотека пресетов"])

with tab1:
    st.header(f"Настройка пресета: {preset_name}")
    
    # Инструкции по TYPE
    st.subheader("1️⃣ TYPE Selector")
    current_type = st.session_state.current_settings['type']
    target_type = selected_preset['type']
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.metric("Текущий тип", current_type)
    
    with col2:
        if current_type != target_type:
            st.warning(f"⚠️ Поверните TYPE на **{target_type}**")
        else:
            st.success("✅ TYPE установлен правильно")
    
    with col3:
        st.metric("Целевой тип", target_type)
    
    if st.button("✓ TYPE установлен"):
        st.session_state.current_settings['type'] = target_type
        st.rerun()
    
    st.markdown("---")
    
    # Визуализация всех ручек
    st.subheader("2️⃣ Настройка ручек управления")
    
    knobs = [
        ("EFFECT", "effect", 10),
        ("DIRECT", "direct", 10),
        ("TONE/RATE", "tone_rate", 10),
        ("DEPTH", "depth", 10),
        ("VARIATION", "variation", 11)
    ]
    
    cols = st.columns(3)
    
    for idx, (label, key, max_val) in enumerate(knobs):
        with cols[idx % 3]:
            current = st.session_state.current_settings[key]
            target = selected_preset[key]
            
            arrow, color, steps = create_arrow(current, target, label)
            
            st.markdown(f"### {label}")
            st.markdown(f"<h2 style='color: {color};'>{arrow}</h2>", unsafe_allow_html=True)
            st.metric("Текущее", current, delta=f"{steps} шагов" if steps > 0 else "OK")
            st.metric("Целевое", target)
            
            # Визуализация ручки
            fig = draw_knob(current, target, max_val, label)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Guitar/Bass переключатель
    st.subheader("3️⃣ GUITAR/BASS Switch")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.metric("Текущий режим", st.session_state.current_settings['guitar_bass'])
    
    with col2:
        if st.session_state.current_settings['guitar_bass'] != selected_preset['guitar_bass']:
            st.warning(f"⚠️ Переключите на **{selected_preset['guitar_bass']}**")
        else:
            st.success("✅ Режим установлен правильно")
    
    with col3:
        st.metric("Целевой режим", selected_preset['guitar_bass'])
    
    # Прогресс настройки
    st.markdown("---")
    st.subheader("📈 Прогресс настройки")
    
    total_params = 6
    correct_params = sum([
        st.session_state.current_settings['type'] == selected_preset['type'],
        st.session_state.current_settings['variation'] == selected_preset['variation'],
        st.session_state.current_settings['tone_rate'] == selected_preset['tone_rate'],
        st.session_state.current_settings['depth'] == selected_preset['depth'],
        st.session_state.current_settings['effect'] == selected_preset['effect'],
        st.session_state.current_settings['direct'] == selected_preset['direct']
    ])
    
    progress = correct_params / total_params
    st.progress(progress)
    st.markdown(f"**{correct_params}/{total_params}** параметров настроено ({progress*100:.0f}%)")
    
    if progress == 1.0:
        st.balloons()
        st.success("🎉 Пресет настроен идеально! Можете играть!")

with tab2:
    st.header("📊 Визуализация настроек")
    
    # Сравнительная таблица
    st.subheader("Сравнение настроек")
    
    comparison_data = {
        "Параметр": ["TYPE", "VARIATION", "TONE/RATE", "DEPTH", "EFFECT", "DIRECT", "MODE"],
        "Текущее": [
            st.session_state.current_settings['type'],
            st.session_state.current_settings['variation'],
            st.session_state.current_settings['tone_rate'],
            st.session_state.current_settings['depth'],
            st.session_state.current_settings['effect'],
            st.session_state.current_settings['direct'],
            st.session_state.current_settings['guitar_bass']
        ],
        "Целевое": [
            selected_preset['type'],
            selected_preset['variation'],
            selected_preset['tone_rate'],
            selected_preset['depth'],
            selected_preset['effect'],
            selected_preset['direct'],
            selected_preset['guitar_bass']
        ]
    }
    
    st.table(comparison_data)
    
    # График сравнения
    st.subheader("График настроек")
    
    params = ['VARIATION', 'TONE/RATE', 'DEPTH', 'EFFECT', 'DIRECT']
    current_values = [st.session_state.current_settings[k.lower().replace('/', '_')] for k in params]
    target_values = [selected_preset[k.lower().replace('/', '_')] for k in params]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=current_values,
        theta=params,
        fill='toself',
        name='Текущие настройки',
        line_color='#e74c3c'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=target_values,
        theta=params,
        fill='toself',
        name='Целевые настройки',
        line_color='#2ecc71'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 11])),
        showlegend=True,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Аудио визуализация
    if st.session_state.audio_monitoring and st.session_state.audio_data:
        st.subheader("🎵 Аудио сигнал")
        
        audio_array = np.concatenate(st.session_state.audio_data[-50:])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=audio_array[:, 0], mode='lines', name='Левый канал'))
        
        fig.update_layout(
            title="Форма волны",
            xaxis_title="Сэмплы",
            yaxis_title="Амплитуда",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("📚 Библиотека пресетов Boss SY-1")
    
    st.markdown("""
    Здесь собраны популярные пресеты для Boss SY-1 от профессиональных музыкантов 
    и сообщества. Выберите пресет на боковой панели для начала настройки.
    """)
    
    # Отображение всех пресетов
    for preset_name, preset_data in PRESETS.items():
        with st.expander(f"🎵 {preset_name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Описание:** {preset_data['description']}")
                st.markdown(f"**Тип:** {preset_data['type']}")
                st.markdown(f"**Режим:** {preset_data['guitar_bass']}")
            
            with col2:
                st.markdown("**Параметры:**")
                st.markdown(f"- VARIATION: {preset_data['variation']}")
                st.markdown(f"- TONE/RATE: {preset_data['tone_rate']}")
                st.markdown(f"- DEPTH: {preset_data['depth']}")
                st.markdown(f"- EFFECT: {preset_data['effect']}")
                st.markdown(f"- DIRECT: {preset_data['direct']}")
    
    st.markdown("---")
    
    # Дополнительные ресурсы
    st.subheader("🔗 Полезные ресурсы")
    
    st.markdown("""
    - [Официальное видео Boss SY-1](https://www.youtube.com/watch?v=suF25zr5uQ4)
    - [Boss SY-1 на официальном сайте](https://www.boss.info/global/products/sy-1/)
    - [Форум пользователей Boss](https://www.boss.info/global/support/)
    - [Reddit: r/guitarpedals](https://www.reddit.com/r/guitarpedals/)
    """)

# Футер
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🎸 Boss SY-1 Preset Tuner | Создано для музыкантов</p>
    <p>Используйте это приложение для точной настройки ваших любимых пресетов</p>
</div>
""", unsafe_allow_html=True)
